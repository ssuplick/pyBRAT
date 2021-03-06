# -------------------------------------------------------------------------------
# Name:        Conservation Restoration
# Purpose:     Adds the conservation and restoration model to the BRAT capacity output
#
# Author:      Jordan Gilbert
#
# Created:     09/2016
# Copyright:   (c) Jordan 2016
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import arcpy
import sys
import os
import projectxml
import uuid


def main(projPath, in_network, out_name):

    arcpy.env.overwriteOutput = True

    out_network = os.path.dirname(in_network) + "/" + out_name + ".shp"
    arcpy.CopyFeatures_management(in_network, out_network)

    # check for oPBRC field and delete if exists
    fields = [f.name for f in arcpy.ListFields(out_network)]
    if "oPBRC" in fields:
        arcpy.DeleteField_management(out_network, "oPBRC")

    LowConflict = 0.25
    IntConflict = 0.5
    HighConflict = 0.75

    arcpy.AddField_management(out_network, "oPBRC", "TEXT", "", "", 60)

    with arcpy.da.UpdateCursor(out_network, ["oCC_EX", "oCC_PT", "oPC_Score", "iPC_ModLU", "iPC_HighLU", "oPBRC"]) as cursor:
        for row in cursor:

            if row[0] <= 1.0:  # none or rare existing capacity
                if row[1] <= 1.0:
                    row[5] = "Unsuitable: Naturally Limited"
                elif row[2] > 0.75:
                    row[5] = "Unsuitable: Anthropogenically Limited"
                elif row[1] <= 5.0:
                    row[5] = "Quick Return Restoration Zone"
                elif row[2] > 0.25:
                    row[5] = "Long Term Possibility Restoration Zone"
                elif row[3] + row[4] > 0.5:
                    row[5] = "Long Term Possibility Restoration Zone"
                else:
                    row[5] = "Quick Return Restoration Zone"

            elif row[0] <= 5.0:  # occasional existing capacity
                if row[2] > 0.75:
                    row[5] = "Unsuitable: Anthropogenically Limited"
                elif row[1] > 5.0:
                    row[5] = "Low Hanging Fruit - Potential Restoration/Conservation Zone"
                elif row[2] <= 0.25:
                    row[5] = "Quick Return Restoration Zone"
                elif row[3] + row[4] > 0.5:
                    row[5] = "Long Term Possibility Restoration Zone"
                else:
                    row[5] = "Living with Beaver (Low Source)"

            elif row[0] <= 15.0:  # frequent existing capacity
                if row[2] > 0.75:
                    row[5] = "Unsuitable: Anthropogenically Limited"
                elif row[1] > 15.0:
                    if row[2] <= 0.25:
                        row[5] = "Low Hanging Fruit - Potential Restoration/Conservation Zone"
                    else:
                        row[5] = "Living with Beaver (High Source)"
                elif row[2] <= 0.25:
                    row[5] = "Low Hanging Fruit - Potential Restoration/Conservation Zone"
                elif row[3] + row[4] > 0.5:
                    row[5] = "Long Term Possibility Restoration Zone"
                else:
                    row[5] = "Quick Return Restoration Zone"

            elif row[0] > 15.0:  # pervasive existing capacity
                if row[2] <= 0.25:
                    row[5] = "Low Hanging Fruit - Potential Restoration/Conservation Zone"
                elif row[2] > 0.75:
                    row[5] = "Unsuitable: Anthropogenically Limited"
                elif row[3] + row[4] > 0.5:
                    row[5] = "Living with Beaver (High Source)"
                else:
                    row[5] = "Quick Return Restoration Zone"

            else:
                row[5] = "NOT PREDICTED - Requires Manual Attention"

            cursor.updateRow(row)

    addxmloutput(projPath, in_network, out_network)

    makeLayers(out_network)

    return out_network


def addxmloutput(projPath, in_network, out_network):
    """add the capacity output to the project xml file"""

    # xml file
    xmlfile = projPath + "/project.rs.xml"

    # make sure xml file exists
    if not os.path.exists(xmlfile):
        raise Exception("xml file for project does not exist. Return to table builder tool.")

    # open xml and add output
    exxml = projectxml.ExistingXML(xmlfile)

    realizations = exxml.rz.findall("BRAT")
    for i in range(len(realizations)):
        a = realizations[i].findall(".//Path")
        for j in range(len(a)):
            if os.path.abspath(a[j].text) == os.path.abspath(in_network[in_network.find("02_Analyses"):]):
                outrz = realizations[i]

    exxml.addOutput("BRAT Analysis", "Vector", "BRAT Management Output", out_network[out_network.find("02_Analyses"):],
                    outrz, guid=getUUID())

    exxml.write()



def makeLayers(out_network):
    """
    Writes the layers
    :param out_network: The output network, which we want to make into a layer
    :return:
    """
    arcpy.AddMessage("Making layers...")
    output_folder = os.path.dirname(out_network)

    tribCodeFolder = os.path.dirname(os.path.abspath(__file__))
    symbologyFolder = os.path.join(tribCodeFolder, 'BRATSymbology')
    managementLayer = os.path.join(symbologyFolder, "Management_Zones.lyr")

    makeLayer(output_folder, out_network, "Beaver Management Zones", managementLayer, isRaster=False)


def makeLayer(output_folder, layer_base, new_layer_name, symbology_layer=None, isRaster=False, description="Made Up Description"):
    """
    Creates a layer and applies a symbology to it
    :param output_folder: Where we want to put the layer
    :param layer_base: What we should base the layer off of
    :param new_layer_name: What the layer should be called
    :param symbology_layer: The symbology that we will import
    :param isRaster: Tells us if it's a raster or not
    :param description: The discription to give to the layer file
    :return: The path to the new layer
    """
    new_layer = new_layer_name
    new_layer_file_name = new_layer_name.replace(" ", "")
    new_layer_save = os.path.join(output_folder, new_layer_file_name + ".lyr")

    if isRaster:
        try:
            arcpy.MakeRasterLayer_management(layer_base, new_layer)
        except arcpy.ExecuteError as err:
            if err[0][6:12] == "000873":
                arcpy.AddError(err)
                arcpy.AddMessage("The error above can often be fixed by removing layers or layer packages from the Table of Contents in ArcGIS.")
                raise Exception
            else:
                raise arcpy.ExecuteError(err)

    else:
        arcpy.MakeFeatureLayer_management(layer_base, new_layer)

    if symbology_layer:
        arcpy.ApplySymbologyFromLayer_management(new_layer, symbology_layer)

    arcpy.SaveToLayerFile_management(new_layer, new_layer_save, "RELATIVE")
    new_layer_instance = arcpy.mapping.Layer(new_layer_save)
    new_layer_instance.description = description
    new_layer_instance.save()
    return new_layer_save




def getUUID():
    return str(uuid.uuid4()).upper()


if __name__ == '__main__':
    main(sys.argv[1],
         sys.argv[2],
         sys.argv[3])
