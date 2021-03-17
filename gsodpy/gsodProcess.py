import numpy as np
import pandas as pd
import tarfile
import re
import os
import datetime
import io


def get_years_files(num_years):
    """
    Create list of files and list of the years we chose

    Parameters:
    -----------
    num_years: int
        The length you would like you time series to be from current time
    """
    files = os.listdir("noaa_data")
    files.sort()
    # take only number of years we want starting from the present
    files = files[-num_years:]
    # find all the years using regex on the digits that start each filename
    years = [int(re.findall('\d+',file)[0]) for file in files]
    
    return years, files


def process_all_years(yearfiles, target_day):  
    """
    Open each zip file in tar, check if station was operating in time series 

    Parameters:
    -----------
    yearfiles: str
        List of zipped tarballs to unpack 
    target_day: datetime.datetime
        Target day to store unaggregated data 
    """
    df = pd.DataFrame([])
    df_day = pd.DataFrame([])
    # process every file for each year into pandas (skip most recent year for now)
    for yearfile in yearfiles[:-1]: 
        print("Processing file: {}".format(yearfile))
        tar = tarfile.open("noaa_data/"+yearfile, "r")
        print("Number of stations in file: {}".format(len(tar.getmembers()[1:])))
        for member in tar: # change to "for member in tar"
            wmo = member.name[0:6]
            wban = member.name[6:11]
            de = pd.read_csv(io.BytesIO(tar.extractfile(member).read()), encoding = 'utf8')
            de = process_df(de)
            df_day = df_day.append(de[(de['MONTH']==target_day.month) & (de['DAY']==target_day.day)]).reset_index(drop=True)
            de = de.groupby(['STATION', 'WMO', 'WBAN', 'YEAR', 'MONTH', 'NAME']).agg('median').reset_index()
            df = df.append(de)
        tar.close()
    df = add_meta(df)
    df_day = add_meta(df_day)
    df_day.reset_index(inplace = True, drop=True)
    return df, df_day



def add_meta(df):
    """
    Add metadata column to dataframe for plotly text boxes

    Parameters:
    -----------
    df: pd.DataFrame
        The final weather station dataframe to add metadata to
    """
    df['META'] = df['NAME']
    df['ELEV_LABEL'] = df['ELEVATION'].apply(lambda x: 'Elevation: '+str(x)+' m' if ~np.isnan(x) else np.nan)
    df['META'] = df[['META','ELEV_LABEL']].apply(lambda x: x.str.cat(sep='<br>'), axis=1)
    df['addmeta'] = df['TEMP'].apply(lambda x: "Temp: {} C".format(f2c(x)))
    df['META'] = df[["META", "addmeta"]].apply(lambda x: x.str.cat(sep='<br>'), axis=1)
    df = df.drop(['NAME', 'ELEV_LABEL', 'addmeta'], axis=1)
    return df


def process_df(df):
    """
    Clean and process the raw weather station dataframes

    Parameters:
    -----------
    df: pd.DataFrame
        Raw dataframe from station csv file to clean and process
    """
    df['WMO'] = df['STATION'].apply(lambda x: str(x)[0:6])
    df['WBAN'] = df['STATION'].apply(lambda x: str(x)[6:11])
    df['MAX'] = df['MAX'].apply(lambda x: str(x).strip("*"))
    df['MIN'] = df['MIN'].apply(lambda x: str(x).strip("*"))
    df[['STATION','TEMP','DEWP','WDSP','MAX','MIN']] = df[['STATION','TEMP','DEWP','WDSP','MAX','MIN']].apply(pd.to_numeric)
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d', errors='ignore')
    df['YEAR'] = pd.DatetimeIndex(df['DATE']).year
    df['MONTH'] = pd.DatetimeIndex(df['DATE']).month
    df['DAY'] = pd.DatetimeIndex(df['DATE']).day
    df.drop(['TEMP_ATTRIBUTES', 'DEWP_ATTRIBUTES', 'MAX_ATTRIBUTES',
             'PRCP_ATTRIBUTES','SLP_ATTRIBUTES', 'MIN_ATTRIBUTES',
             'SLP', 'STP', 'STP_ATTRIBUTES'], axis=1, inplace=True)
    return df



def create_extremes(df, target_day, num_extremes):
    """
    Create extremes dataframe to plot coldest and warmest places on a given day
    
    Parameters:
    -----------
    df: pd.DataFrame 
        df_day (unaggregated) dataframe to find extreme temps from
    target_day: datetime.datetime
        The day from the year we are using. (df_day stores the same day from every year)
    num_extremes: int
        The number of coldest and hotest weather stations we want to see (e.g. 30 = 60 total stations)
    """
    extremes = pd.DataFrame([])
    extremes = extremes.append(df[df['DATE']==target_day].sort_values(by="TEMP", ascending=False).head(num_extremes))
    extremes = extremes.append(df[df['DATE']==target_day].sort_values(by="TEMP", ascending=False).tail(num_extremes))
    return extremes


def c2f(temp):
    """
    Convert C to F
    """
    return np.round(((temp*9/5)+32),1)


def f2c(temp):
    """
    Convert F to C
    """
    return np.round(((temp-32)*5/9),1)