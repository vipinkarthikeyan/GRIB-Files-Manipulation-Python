#Import Libraries
import xarray as xr 
import pandas as pd
import numpy as np
import gc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#creating a FastAPI object
GRIB_2_API = FastAPI()

CORSMiddleware(GRIB_2_API)

@GRIB_2_API.get('/')
async def root():
    return '------ Application is Running! ------'

#GRIB2 reader function with arguments - GRIBFile_path, Latitude and Longitude extents(South-West corner and North-East corner) of bounding box to clip the file.
@GRIB_2_API.post('/grib_2_reader')
def grib_2_reader(params: dict):
    
    #pass the grib file location as an input to the function
    grib_file_path = params['grib_file_path']
    lon1 = params['longitude_extent_1']
    lat1 = params['latitude_extent_1']
    lon2 = params['longitude_extent_2']
    lat2 = params['latitude_extent_2']

    #xarray library is used to open the GRIB file, the engine can be cfgrib/pynio/netcdf4/h5netcdf
    grib2_data =xr.open_dataset(grib_file_path, engine='cfgrib')
    #convert the data to a dataframe
    grib2_df = grib2_data.to_dataframe()

    #Latitude and Longitude filter created with the extents entered by the user.
    lat_filter = (grib2_df["latitude"] >= lat1) & (grib2_df["latitude"] <= lat2)
    lon_filter = (grib2_df["longitude"] >= lon1) & (grib2_df["longitude"] <= lon2)
    clipped_grib2_df = grib2_df.loc[lat_filter & lon_filter]

    #Free and collect memory
    del grib2_df
    gc.collect()

    #returns a dataframe
    return clipped_grib2_df

    #Free memory


if __name__ == "__main__":
    uvicorn.run("app:GRIB_2_API", host="0.0.0.0", port=5008, log_level="info")
