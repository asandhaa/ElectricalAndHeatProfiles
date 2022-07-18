# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 10:18:40 2021

@author: asandhaa
"""
import pandas as pd
import numpy as np

def modul_2(year, industry_number, data_industry_type, 
            weekday_1, saturday_1, sunday_1, holiday_1, constant_1):
    
    
    """1) Zunächst wird die Basislast der Gesamtlast (außer Constant) auf den Start-Wert von 0 gezogen, 
          damit die Kurven gestreckt oder gestaucht werden können und der Fixpunkt (Start) unverändert bleibt.
       2) Gesamtlast wird anhand der peak- und base-Faktoren gestreckt/gestaucht
       3) Gesamtlast wird auf 100 kW Basislast versetzt
       4) Anwendungen werden  anschließend wieder eingefügt, indem an jedem Zeitpunkt der Anteil der
          jeweiligen Anwendung aus modul_1 ermittelt und das gestreckte Gesamtprofil anhand der Anteile
          in die Anwendungen aufgetrennt wird.
          
    """

    """WEEK DAY"""     
    # Gesamtverbrauch
    y = weekday_1['Total']-weekday_1['Total'][0]    #Zeitreihe des Gesamtverbrauchs komplett versetzen, auf Startwert 0
    peak_ist = np.max(y)    #peak_ist und peak_soll bestimmen
    peak_soll = (float(data_industry_type[data_industry_type['industry_number']==industry_number]['Peak_faktor'])-1)*100
    if peak_soll == -100:
        peak_soll = peak_ist #falls kein Faktor hinterlegt
    weekday = y*(peak_soll/peak_ist)  #Strecken bzw. Stauchen
    weekday =weekday +100   # Zeitreihe komplett versetzen, auf Startwert 100
        
    # Anwendungen wieder einfügen
    weekday_2 = weekday_1.copy()    #Formate, Spaltennamen übernehmen
    for i in range(len(weekday_2)): # Anwendungen anpassen
        weekday_2.iloc[i] = weekday_1.iloc[i]/weekday_1['Total'].iloc[i]*weekday[i] #An jedem Zeitpunkt i wird der Anteil der Anwendung mit Gesamtverbrauch multipliziert
    weekday_2 = weekday_2.round(2)
    
    
    """SATURDAY"""   
    y = saturday_1['Total']-saturday_1['Total'][0]    
    base_ist = np.min(y)
    base_soll = (float(data_industry_type[data_industry_type['industry_number']==industry_number]['Base_faktor'])-1)*100
    if base_soll == -100:
        base_soll = base_ist
    saturday = y*(base_soll/base_ist)
    saturday = saturday +100
    
    saturday_2 = saturday_1.copy()
    for i in range(len(saturday_2)):
        saturday_2.iloc[i] = saturday_1.iloc[i]/saturday_1['Total'].iloc[i]*saturday[i]
    saturday_2 = saturday_2.round(2)
    #modul_plot_IND_E.day_electrical(y)
    
        
    """SUNDAY"""
    y = sunday_1['Total'] - sunday_1['Total'][95]
    sunday = y*(base_soll/base_ist)
    sunday = sunday + 100

    sunday_2 = sunday_1.copy()
    for i in range(len(sunday_2)):
        sunday_2.iloc[i] = sunday_1.iloc[i]/sunday_1['Total'].iloc[i]*sunday[i]
    sunday_2 = sunday_2.round(2)
         
    
    """HOLIDAY"""
    y = holiday_1['Total']-holiday_1['Total'][0]
    holiday = y*(base_soll/base_ist)
    holiday = holiday + 100
    
    holiday_2 = holiday_1.copy()
    for i in range(len(holiday_2)):
        holiday_2.iloc[i] = holiday_1.iloc[i]/holiday_1['Total'].iloc[i]*holiday[i]
    holiday_2 = holiday_2.round(2)
         
    
    
    """CONSTANT HOLIDAY"""
    #Die Methode weicht von den anderen ab, da die Verteilung der Anwendungen in jedem Punkt die gleiche ist
    y= [(100+base_soll) for i in range(96)]
    constant = pd.Series(y,index=holiday.index)
    
    constant_2 = constant_1.copy()
    for i in range(len(constant_2)):
        constant_2.iloc[i] = constant_1.iloc[i]/constant_1['Total'].iloc[i]*constant[i]
    constant_2 = constant_2.round(2)
    # modul_1_IND_E.diagram_1(constant_2) 
    
    return weekday_2, saturday_2, sunday_2, holiday_2, constant_2 

