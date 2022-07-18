# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 11:46:24 2021

@author: asandhaa
"""
import matplotlib.pyplot as plt
import pandas as pd
import os

os.chdir(r"P:\INES\INES\Projekte\IND-E\5 - Projektarbeit\AP1\Python") #Arbeitsverzeichnis festlegen, wo Module gespeichert sind
import modul_1_IND_E
import modul_2_IND_E
import modul_3_IND_E 
import modul_4_IND_E 
import modul_plot_IND_E

"""MANUELLE SETTINGS"""

"""
industry_number	     industry_name
	
1	Gew. v. Steinen u. Erden
2	Ernährung und Tabak
3	Papiergewerbe
4	Grundstoffchemie
5	Sonst. chemische Industrie
6	Gummi- u. Kunststoffwaren
7	Glas u. Keramik
8	Verarb. v. Steine u. Erden
9	Metallerzeugung
10	NE-Metalle, -gießereien
11	Metallbearbeitung
12	Maschinenbau
13	Fahrzeugbau
14	Sonstige Wirtschaftszweige"""

"""MANUAL SETTINGS"""
PATH = "P:\INES\INES\\Projekte\IND-E\\5 - Projektarbeit\AP1\Python" #Speicherplatz
industry_number = 7     # Auswahl aus obiger Liste
year = 2020          # 2018, 2019, 2020
""""""""""""""""""""""""

"""Ausführen von Modul 1:
    Normierte Lastprofile pro Typtag"""
weekday_1, saturday_1, sunday_1, holiday_1, constant_1, data_industry_type = modul_1_IND_E.modul_1_el(industry_number, PATH)

industry_type = data_industry_type['WZ_ID'][industry_number]   
industry_name = str(data_industry_type['Name'][industry_number]) #defines industry name
print(industry_name)

"""Ausführen von Modul 2:
    Anpassung in vertikaler Richtung, Strecken und Stauchen anhand base_ und peak_faktoren"""
weekday_2, saturday_2, sunday_2, holiday_2, constant_2 = modul_2_IND_E.modul_2(year, industry_number, data_industry_type, 
            weekday_1, saturday_1, sunday_1, holiday_1, constant_1)

"""Ausführen von Modul 3:
    Zusammensetzen der Tageslastgänge zu Lastgang 1 Jahr, Normierung auf Verbrauch von 1000 MWh/a"""
year_list, array_load_type = modul_3_IND_E.modul_3(year)
df = modul_3_IND_E.seasonality(year, year_list, array_load_type, weekday_2, saturday_2, sunday_2, holiday_2, constant_2, PATH)
df_year_3 = modul_3_IND_E.normalising_1000(df)

"""Ausführen von Modul 4:
    Skalieren auf Jahresverbrauch und Aufprägung der Fluktuationen"""
df_year_4 = modul_4_IND_E.modul_4(year, industry_number, df_year_3, data_industry_type)
df_year_4 = modul_4_IND_E.modul_4_fluct(industry_number, df_year_4, data_industry_type)

"Speichern der Lastdaten und Diagramme"
if not os.path.exists(PATH +'\\Electrical\\Diagramme\\'):    
    os.mkdir(PATH +'\\Electrical\\Diagramme')    
modul_plot_IND_E.year_electrical(df_year_4, industry_name, industry_type, PATH) #Plottet und Speichert Diagramm


if not os.path.exists(PATH +'\\Electrical\\Lastdaten\\'):    
    os.mkdir(PATH +'\\Electrical\\Lastdaten')    
ARRAY = [['Raumwärme', 'Warmwasser', 'Prozesswärme', 'Klimakälte', 
          'Prozesskälte', 'Beleuchtung', 'IKT', 'Mechanische Antriebe', 'Total'],
         ['in kW', 'in kW', 'in kW', 'in kW', 'in kW', 'in kW', 'in kW', 'in kW', 'in kW']]
DF_COLUMN = pd.MultiIndex.from_arrays(ARRAY, names=('Anwendung', 'Einheit'))
DF = df_year_4.copy()
DF.columns = DF_COLUMN
DF.index.name = 'Zeit'
DF.to_excel(PATH + "\\Electrical\\Lastdaten\\" + industry_name+' WZ08 '+ str(industry_type) +'.xlsx', index=True) 

