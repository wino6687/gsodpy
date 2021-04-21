import requests
import re
import os


def get_data(directory="noaa_gsod"):
    """
    Download all data from GSOD that is currently in the Bulk Download
    
    Parameters:
    -----------
    directory: str
        The directory you want to download the csv files to. Will create it if it
        doesn't exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    base_url = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/"
    rt = requests.get(base_url).text
    years = re.findall("(?<!\>)\d{4}", rt)
    for year in years:
        url = base_url+str(year)+'.tar.gz'
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open('noaa_data/'+str(year)+'.tar.gz', 'wb') as f:
                f.write(r.raw.read())