---
title: Computer Setup & Installation
weight: 2
---
## Python Prerequisites
In order to use the [Beaver Restoration Assessment Tool (BRAT) Toolbox v 3](https://github.com/Riverscapes/pyBRAT/releases/latest), your computer needs to have ArcGIS version 10.4 or later with the Spatial Analyst Extension as well as the scikit-fuzzy python module. Don't panic, even if you've never used a command line, you can follow these instructions. The video will show you how to install a few dependencies ( [NumPy_mkl](https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy) and  [scikit-fuzzy](https://pypi.python.org/pypi/scikit-fuzzy)) that BRAT uses. The video below provides detailed instructions on installing the [scikit-fuzzy](https://pypi.python.org/pypi/scikit-fuzzy) python module.

**NOTE: The following video contains some information that is out of date. NumPy_mkl is no longer required to run BRAT**

<iframe width="560" height="315" src="https://www.youtube.com/embed/6-Je5jtH-j8" frameborder="0" allowfullscreen></iframe>

You can download the software menitoned in the video from these links:
- [PipInstall](https://pip.pypa.io/en/stable/installing/) - only if you don't have it (usually installs with ArcGIS 10.4 or later)
- To install the [scikit-fuzzy module](https://pypi.python.org/pypi/scikit-fuzzy), navigate in a command prompt to where Pip is located (e.g.  `c:\Python27\ArcGIS10.4\Scripts\`) and at command prompt type: `pip install scikit-fuzzy`. Note, the beauty of pip (Python Install Package) is that you don't have to go download these files, you just run ip and it downloads and installs them for you. 

## Installing BRAT
You can download the latest version of BRAT [here](https://github.com/Riverscapes/pyBRAT/releases/latest). The video below walks you through the install process.

<iframe width="560" height="315" src="https://www.youtube.com/embed/MVEXXMOPTBI" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

------
<div align="center">
	<a class="hollow button" href="{{ site.baseurl }}/Documentation"><i class="fa fa-info-circle"></i> Back to Help </a>
	<a class="hollow button" href="{{ site.baseurl }}/"><img src="{{ site.baseurl }}/assets/images/favicons/favicon-16x16.png">  Back to BRAT Home </a>  
</div>