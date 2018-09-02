#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 12:15:21 2018

@author: jruiz
"""
import pandas as pd

def wb_countryreader_csv(file, start=1960, end=2017, skiprows=4):
    """
    Read csv files downloaded from the World Bank into dataframes
    
    Read csv file from the World Bank, where every row conveys data
    from a specific country or multinational region with columns names
    "Country Code", "Country Name", "Indicator Name", "Indicator Code"
    and each of the years available in the series, eg. "1960",..."2017".
    The first four rows usually contain metadata.
    
    Args:
        file: name, including full path if necessary, to csv data file
        start: initial year in the series (default 1960)
        end: last year (default 2017)
        skiprows: number of initial rows to be skipped from file (default 4)
    Return:
        dataframe with aggregate regions
        dataframe with countries
        dictionanary with code to/from region and country conversions
    """
    
    cols = (['Country Name', 'Country Code'] + 
            [str(i) for i in range(start, end+1)])
    idx = pd.PeriodIndex(range(start,end+1), freq='A', name='Year')    
    regions = ['ARB', 'CEB', 'CSS', 'EAP', 'EAR', 'EAS', 'ECA', 'ECS', 'EMU', 
           'EUU', 'FCS', 'HIC', 'HPC', 'IBD', 'IBT', 'IDA', 'IDB', 'IDX', 
           'INX', 'LAC', 'LCN', 'LDC', 'LIC', 'LMC', 'LMY', 'LTE', 'MEA', 
           'MIC', 'MNA', 'NAC', 'OED', 'OSS', 'PRE', 'PSS', 'PST', 'SAS', 
           'SSA', 'SSF', 'SST', 'TEA', 'TEC', 'TLA', 'TMN', 'TSA', 'TSS',
           'UMC', 'WLD']
    
    df = pd.read_csv(file, skiprows=4, usecols=cols)
    
    df_regions = df[[c in regions for c in df['Country Code'].values]]
    region2code = dict(zip(df_regions['Country Name'].values, 
                        df_regions['Country Code'].values))
    code2region = dict(zip(df_regions['Country Code'].values, 
                        df_regions['Country Name'].values))
    del df_regions['Country Name']
    df_regions.set_index(['Country Code'], inplace=True);
    df_regions.columns = idx
    #df_regions = df_regions.T
    #df_regions.index = idx
    
    # print(df_regions)
    
    df_countries = df[[not (c in regions) for c in df['Country Code'].values]]
    country2code = dict(zip(df_countries['Country Name'].values, 
                        df_countries['Country Code'].values))
    code2country = dict(zip(df_countries['Country Code'].values, 
                        df_countries['Country Name'].values))      
    del df_countries['Country Name']
    df_countries.set_index(['Country Code'], inplace=True);
    df_countries.columns = idx
    #df_countries = df_countries.T
    #df_countries.index = idx

    return (df_regions, df_countries, 
            {'region2code': region2code, 'code2region': code2region, 
             'country2code': country2code, 'code2country': code2country})
    

