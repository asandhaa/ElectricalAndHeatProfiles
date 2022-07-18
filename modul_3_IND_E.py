# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:59:18 2021

@author: asandhaa
"""

import pandas as pd
import datetime
import holidays


    
def modul_3(year):
    
    
    """===LIST OF HOLIDAYS==="""
    
    year_list = pd.date_range(str(year)+'-01-01', str(year)+'-12-31', freq="D")
    year_list = list(year_list)
    
    dates=[]
    names=[]
    for date, name in sorted(holidays.Germany(years=year).items()):
        dates.append(date)
        names.append(name)
    dates.append(datetime.date(year,1,6))    
    dates.append(datetime.date(year,12,24))
    dates.append(datetime.date(year,12,31))
    names.append('Heilige drei Könige')
    names.append('Heiligabend')
    names.append('Sylvester')
    list_holidays = pd.DataFrame({'date':dates, 'name':names}, index=None)
    
    for i in list_holidays['date']:
        if datetime.date.weekday(i) == 1:
            list_holidays=list_holidays.append({'date':(i + datetime.timedelta(days = -1)), 'name':'Brückentag'}, ignore_index=True)
        elif datetime.date.weekday(i) == 3:
            list_holidays=list_holidays.append({'date':(i + datetime.timedelta(days = 1)), 'name':'Brückentag'}, ignore_index=True)
       

    
    """Clustering days into working days (1) and non working days (2)"""
    array_wd_we = []
    count =1
    for i in year_list:
        if datetime.datetime.weekday(i) in [0,1,2,3,4] and i  not in dates: #holidays
            array_wd_we.append(1)
        else:
            array_wd_we.append(2)
    
    """Clustering days into load pattern days (1)-(5)
    (1) working day with weekday load profile
    (2) holiday between working days with holiday load profile
    (3) Saturday or holiday where: day before working day, day after non-working day with saturday load profile
    (4) Saturday or holiday where: day before non-working day, day after working day with sunday load profile
    (5) Weekend or holiday where: days before and after non-working day with constant load profile
    
    """
    
    array_load_type=[]
    for i in range(len(array_wd_we)):
        if array_wd_we[i] == 1:
            array_load_type.append(1)
            count+=1
        elif array_wd_we[i] == 2 and i !=0 and i != len(array_wd_we)-1:
            if array_wd_we[i-1] == 1:
                if array_wd_we[i+1] == 1:
                    array_load_type.append(2)
                elif array_wd_we[i+1] == 2:
                    array_load_type.append(3)
            elif array_wd_we[i-1] == 2:
                if array_wd_we[i+1] == 1:
                    array_load_type.append(4)
                elif array_wd_we[i+1] == 2:
                    array_load_type.append(5)
        elif i ==0:
            if array_wd_we[i+1] == 1:
                array_load_type.append(4)
            elif array_wd_we[i+1] == 2:
                array_load_type.append(5)
        elif i ==len(array_wd_we)-1:
            if array_wd_we[i-1] == 1:
                array_load_type.append(3)
            elif array_wd_we[i-1] == 2:
                array_load_type.append(5)
        else: print(50)
    
    return year_list, array_load_type

""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""Space heating is modeled by seasonality factors"""
def seasonality(year, year_list, array_load_type, weekday_2, saturday_2, sunday_2, holiday_2, constant_2, path):    # With seasonality

    month_factor = pd.read_excel(path+'\\HeatingDegreeDays.xlsx'.format(), sheet_name='HDD') 
    month_factor = month_factor.iloc[0][1:13]
    
    df = pd.DataFrame(dtype=float)
    dict_load_type = {1:weekday_2, 2:holiday_2, 3: saturday_2, 4:sunday_2, 5:constant_2}
    
    for i in range(len(year_list)):
        dayprofile_3 = dict_load_type[array_load_type[i]].copy()
        dayprofile_3['Raumwärme'] = dayprofile_3['Raumwärme']*month_factor[year_list[i].month-1]
        df=df.append(dayprofile_3, ignore_index=True)    
            
    idx = pd.date_range(datetime.datetime(year,1,1,0,0),datetime.datetime(year,12,31,23,45), freq="15min" )    
    df.index = idx
    
    return df

""""""""""""""""""""""""""""""""""""""""""""""""""""""

def normalising_1000(df):

    """Normalising the yearly load to 1000 MWh"""
    energy_per_year_3 = float(df['Total'].sum()*0.25/1000) #Energie_ist in MWh/a

    df_year_3 = df/(energy_per_year_3/1000) #Energie_ist gleich 1000 MWh/a
    #print("Normiert auf %0.0f MWh/a" %(df_year_3['Total'].sum()*0.25/1000))     
    return df_year_3
       
       
"""TODO:
    - PATH in function
    - 
    """
