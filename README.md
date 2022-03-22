# GRIB-Files-Manipulation-Python
GRIB - GRIdded Binary or General Regularly-distributed Information in Binary form, is a data format used in meteorology to store historical and forecast weather data. GRIB_1 and GRIB_2 files are the most used versions as GRIB_0 files is no longer operational.


Difference between GRIB1 and GRIB2 -

GRIB1	is	the	original	format	and	requires	a	separate	parameter	table	to	unpack	the	data. GRIB2	improves	upon	the	standard with	file	compression	and	the	inclusion	of	the	metadata/parameter	table	that	you	need	to	unpack	the	data	in	each	file.	GRIB2	exploits	the	same	compression	software commonly	used	for	images	to	gain	a	roughly 50%	reduction	in	Hile	size	over GRIB1.

The Xarray library in python is very helpful in opening GRIB files. Once unpacked, the data can be converted into a dataframe and sliced/manipulated using pandas functions.
