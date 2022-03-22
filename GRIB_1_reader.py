#Import Libraries
import xarray as xr 
import pandas as pd
import numpy as np
import gc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#creating a FastAPI object
GRIB_1_API = FastAPI()

CORSMiddleware(GRIB_1_API)

@GRIB_1_API.get('/')
async def root():
    return '------ Application is Running! ------'

#GRIB1 reader function with arguments - GRIBFile_path, Latitude and Longitude extents(South-West corner and North-East corner) of bounding box to clip the file.
@GRIB_1_API.post('/grib_1_reader')
def grib_1_reader(params: dict):
    
    #pass the grib file location as an input to the function
    grib_file_path = params['grib_file_path']
    lon1 = params['longitude_extent_1']
    lat1 = params['latitude_extent_1']
    lon2 = params['longitude_extent_2']
    lat2 = params['latitude_extent_2']

    #xarray library is used to open the GRIB file, the engine can be cfgrib/pynio/netcdf4/h5netcdf
    grib1_data =xr.open_dataset(grib_file_path, engine='cfgrib')
    #convert the data to a dataframe
    grib1_df = grib1_data.to_dataframe()
    #the GRIB1 files are multi-indexed so resetting the index to Step, Latitude and Longitude makes the dataframe more organised and accessable
    grib1_df = grib1_df.reset_index(level=['step','latitude','longitude'])
    #the longitude values in GRIB1 files range from 0 to 360, scaling the range from -180 to 180 gets it into the most used convention/form.
    grib1_df['longitude'] = (grib1_df['longitude']-180)

    #Latitude and Longitude filter created with the extents entered by the user.
    lat_filter = (grib1_df["latitude"] >= lat1) & (grib1_df["latitude"] <= lat2)
    lon_filter = (grib1_df["longitude"] >= lon1) & (grib1_df["longitude"] <= lon2)
    clipped_grib1_df = grib1_df.loc[lat_filter & lon_filter]

    #Free and collect memory as GRIB1 files when unpacked reach 8-10GB, not compatible for systems with 8GB RAM.
    del grib1_df
    gc.collect()

    #returns a dataframe
    return clipped_grib1_df

    #Free memory


if __name__ == "__main__":
    uvicorn.run("app:GRIB_1_API", host="0.0.0.0", port=5008, log_level="info")
