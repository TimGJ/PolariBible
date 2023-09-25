#Polari Bible
The code and data files necessary to build the Polari Bible as produced
by the Manchester House of the Sisters of Perpetual Indulgence.

##Environment
The code is designed to be run on a Linux/Unix host. It requires the following:

* Python3
* Various Linux tools, particularly `make`
* LaTeX (TeTeX was used in development)
* Pandoc
* The typesetting uses Times New Roman so you will need to have the `msttcorefonts` package installed or otherwise mess
with the font settings.

##Building the Bible
The code should build by simply issuing the command

`$ make`

from the directory containing the various source and data files. To clean up after yourself you can also issue

`$ make clean`