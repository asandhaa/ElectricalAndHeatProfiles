# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:59:18 2021

@author: asandhaa
"""

import numpy as np
import pandas as pd



def modul_4(year, industry_number, df_year_3, data_industry_type):
   
    """Upscaling the yearly load to energy demand of 2019"""
    energy_per_year_MWh = float(data_industry_type['Energieverbrauch '+ str(year)]) #in 1000 MWh/a
    
    df_year_4 = df_year_3*energy_per_year_MWh
    df_year_4 = df_year_4.round(0)
    
    return df_year_4

def modul_4_fluct(industry_number, df_year_4, data_industry_type):

    s_norm = data_industry_type['Fluktuation'][industry_number] #relative Fluktuation in % relativ zu 100 kW Leistung
    power_peak = np.max(df_year_4['Total']) #in kW
    s_rel = s_norm * (100/power_peak)**0.5 #relative Fluktuation in % bezogen auf tatsächliche Leistung
    s_abs = s_rel/100 * power_peak
    
    rand_numbers = np.random.normal(0, s_abs, len(df_year_4)).round(0)
    
    df_year_4['Mechanische Antriebe'] = df_year_4['Mechanische Antriebe']+rand_numbers  
    df_year_4['Total'] = df_year_4['Total']+rand_numbers
    
    return df_year_4
