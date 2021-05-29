import numpy as np
import pandas as pd

class subset_helper():
    # Simple data subsetting before running predictive model
    # The purpose is to provide a flexible way to experiment model performance on differenet periods and diseases
    def __init__(self, data):
        self.data = data
        
    def get_summer(self, df):
        # Subset the summer period, May - Aug
        return df[(df['MONTH'] <= 8) & (df['MONTH'] >= 5)]

    def get_disease(self, df):
        # Subset common heat-related illness, sourced from reviewing multiple academic papers
        diseases = ('Diseases of the circulatory system', 
                    'Diseases of the respiratory system', 
                    'Diseases of the skin and subcutaneous tissue')
        return df[df['COD'].isin(diseases)]
    
    def subset(self):
        self.data = self.get_summer(self.data)
        self.data = self.get_disease(self.data)
        return self.data

    
    
class cleaner_climate():  
    # Data cleaning script to calculate the number of heat days and other factors
    def __init__(self,  df_concat, df_reference, key):
        self.climate_city = df_concat
        self.reference_dist = df_reference
        self.key1 = key
        self.key2 = key.copy().remove('YEAR')
    
    def count_consecutive(self, x):
        # Count consecutive days
        x_str = ''.join(map(lambda x: str(int(x)), x.to_list())) # For each groupby, join the list into string e.g. 00001111010011
        x_str = x_str.replace('0', ' ').split(' ') # replace 0 with empty string and split e.g. ['', '1111', '', 1, '', 11]
        x_str = list(filter(lambda x: len(x) >= 2, x_str)) # Filter to a list, count length > 2 (consecutive heatwave days) e.g. ['1111', '11']
        return len(''.join(x_str)) # Join all substrings together and count the total number of consecutive heatwave days within a month e.g. '111111'
    
    def monthly_stat(self):
        df_results = pd.DataFrame()
        df_groupby = self.climate_city.groupby(self.key1)
        # Do some features transformation here, add extra columns if needed
        df_results['TEMP_MEAN'] = df_groupby['T2M_MAX'].mean() # Mean of daily temperature
       #  df_results['TEMP_VAR'] = df_groupby['T2M_MAX'].std() # Standard deviation of daily temperature, removed, high correlation
        df_results['TEMP_RNG'] = df_groupby['T2M_RANGE'].max() # Maximum daily temperature range
        df_results['WS50M_MEAN'] = df_groupby['WS50M'].mean() # Average daily wind speed
        df_results['PRECTOT_MEAN'] = df_groupby['PRECTOT'].mean() # Average daily precipitation
        df_results['RH2M_MEAN'] = df_groupby['RH2M'].mean() # Average relative humidity
        return df_results
    
    def featurize(self):
        df_monthly_stat = self.monthly_stat().reset_index().merge(self.reference_dist, how = 'left', on = self.key2)
        df_results = self.climate_city.merge(df_monthly_stat, how = 'left', on = self.key1)
        # ABOVE_LIMIT: If daily max temperature > 90th percentile from the reference, 1. Else 0
        df_results['ABOVE_LIMIT'] = (df_results['T2M_MAX'] > df_results['TEMPMAX_90th']).astype(np.float64)
        df_monthly_stat['HEAT_DAYS'] = df_results.groupby(self.key1)['ABOVE_LIMIT'].agg(self.count_consecutive).values
        return df_monthly_stat.drop(['TEMPMAX_90th'], axis = 1)