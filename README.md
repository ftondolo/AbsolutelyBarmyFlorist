# AbsolutelyBarmyFlorist
A program that reads all the ABF files in its directory and creates a series of CSV files for each of the ABF files' channels and sweeps with some minor data analysis mixed in. Code **very** heavily based on pyABF sample code. It creates an OUTPUT folder in which files with the format  `<filename>-sweep<#>-ch<#>.csv` are saved
<br>
### SimplisticFlorist
AbsolutelyBarmyFlorist is, as you can probably guess, insane.  It has a massive amount of features, however, this makes it unimaginably slow.  SimplisticFlorist does away with all the visual fantasmagoria and console interactions thus keeping the runtime (relatively) in check.  The CSV creation hierarchy is very much the same.

## Notice
Due to the naming structure, __it is necessary that there are no folders named 'OUTPUT' in the program's directory, and that every abf filename have no spaces in it__. 

The mad florist in action:
![alt text](https://raw.githubusercontent.com/ftondolo/AbsolutelyBarmyFlorist/master/image.png)
