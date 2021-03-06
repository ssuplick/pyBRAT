---
title: Step 4 - iHyd Attributes
weight: 6
---

To add the "iHyd" or hydrologic attributes to the input table you created in the previous step, regressions for predicting stream flow must first be obtained.  This information can be found at https://water.usgs.gov/osw/streamstats/.  Once you have the regressions for both typical low flow and a typical 2-year flood, you must modify the script of the iHyd Attributes tool.  To do so, open the iHyd.py file (found inside the toolbox) in a python text editor.  Pyscripter works well.

For each area that you want to add a regression for a block of code must be added in the appropriate place.

![ihyd_code]({{ site.url }}/assets/images/ihyd_code.PNG)

The code block should follow this format:

elif float(region) == <choose an integer>:  # describe the area using the pound/hash sign in front

​    Qlow = <enter low flow regression here, always referring to drainage area as DAsqm>

​    Q2 = <enter Q2 regression here, always referring to drainage area as DAsqm>

Note that in line 2 and 3 a TAB is used to indent.

As an example, say I want to add a regression for the Bridge Creek watershed in Oregon.  I would add the following block:

elif float(region) == 24: #oregon region 5

​    Qlow = 1.31397 * (10 ** -20.5528) * (DAsqm ** 0.9225) * (16.7 ** 3.1868) * (6810 ** 3.8546)

​    Q2 = 1.06994 * (10 ** -9.3221) * (DAsqm ** 0.9418) * (16.7 ** 2.692) * (6810 ** 1.5663) 

the script would then look like this:

![ihyd_code2]({{ site.url }}/assets/images/ihyd_code2.PNG)

After any necessary regressions have been entered, save the changes to the script, and then update the toolbox in ArcMap by right clicking on it and clicking "refresh".  The iHyd Attributes tool can now be run.

![iHyd]({{ site.url }}/assets/images/iHyd.PNG)

Inputs and Parameters:

- **Input BRAT Network**  - select the network that was created using the BRAT Table tool
- **Select Hydrologic Region** -  enter the integer that was used to identify the regression you want to use.  In the example here we used the number 24.



<div align="center">
	<a class="hollow button" href="{{ site.baseurl }}/Documentation/Tutorials/StepByStep/3.2-BRATBraidHandler"><i class="fa fa-arrow-circle-left"></i> Back to Step 3.2 </a>
	<a class="hollow button" href="{{ site.baseurl }}/Documentation/Tutorials/StepByStep/5-BRATVegetationFIS"><i class="fa fa-arrow-circle-right"></i> Continue to Step 5 </a>
</div>	

------
<div align="center">

	<a class="hollow button" href="{{ site.baseurl }}/Documentation"><i class="fa fa-info-circle"></i> Back to Help </a>
	<a class="hollow button" href="{{ site.baseurl }}/"><img src="{{ site.baseurl }}/assets/images/favicons/favicon-16x16.png">  Back to BRAT Home </a>  
</div>