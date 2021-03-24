# gsodpy
Python module to download and work with GSOD data from NOAA

## Usage Guide: 

### Dowload All Data


```{Python}
import gsodpy.gsodDownloader as gdown

gdown.get_data(directory="noaa_gsod")
```

### Process Desired Time Series

```{Python}
import gsodpy.gsodProcess as gsod 
import pandas as pd
import datetime

num_years = 10
num_extremes = 30
target_day = datetime.datetime(2020,3,20)

years, files = gsod.get_years_files(num_years)

df, df_day = gsod.process_all_years(files, target_day)
```

#### Save Processed DataFrame

```{Python}
df.to_pickle("df_monthly.pkl")
df_day.to_pickle("df_daily.pkl")

df = pd.read_pickle("df_monthly_fin.pkl")
df_day = pd.read_pickle("df_daily_fin.pkl")
```

### Create Extremes DataFrame

If we want to find the coldest and warmest stations on a given day we can use the ```create_extremes()``` function 

```{Python}
extremes = gsod.create_extremes(df_day, df_day['DATE'][0], 40)
```