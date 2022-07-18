# -*- coding: utf-8 -*-
"""
Created on Thu May  5 15:32:47 2022

@author: asandhaa
"""

import pandas as pd
import datetime
import holidays
import matplotlib.pyplot as plt
import numpy as np


"""Dopplungen vermeiden
CLASS?"""

'''Plotting and saving results'''



def plot_el(y):
# ELEKTRISCH
    new_colors = [ (254/255, 188/255, 195/255),     #Farbe Raumwärme RGB/255
     (255/255, 89/255, 105/255),                    #Farbe Warmwasser 
     (172/255, 0/255, 16/255),                      #Farbe Prozesswärme
     (82/255, 203/255, 190/255),                    #Farbe Klimakälte
     (49/255, 164/255, 151/255),                    #Farbe Prozesskälte
     (254/255, 198/255, 48/255),                    #Farbe Beleuchtung
     (146/255, 208/255, 80/255),                    #Farbe IKT
     (93/255, 115/255, 115/255)]                    #Farbe Mechanische Antriebe
    
    labels = ['Raumwärme', 'Warmwasser', 'Prozesswärme', 'Klimakälte', 
                  'Prozesskälte', 'Beleuchtung', 'IKT', 'Mechanische Antriebe']
    
    # labels = ['Space heating', 'Hot water', 'Process heat', 'Space cooling', 'Process cooling',
    # 'Lighting', 'ICT', 'Mechanical drive']

    y_plot = np.vstack([y['Raumwärme'].tolist(), 
                y['Warmwasser'].tolist(),
                y['Prozesswärme'].tolist(),
                y['Klimakälte'].tolist(),
                y['Prozesskälte'].tolist(),
                y['Beleuchtung'].tolist(),
                y['IKT'].tolist(),
                y['Mechanische Antriebe'].tolist()])
    
    return  new_colors, labels, y_plot
    
    

def plot_th(y):
# THERMISCH
    new_colors = [ (200/255, 200/255, 200/255),   #Farbe Space heating RGB/255
     (93/255, 115/255, 115/255),                  # Farbe Hot water
     (255/255, 201/255, 206/255),                 #Farbe < 100 °C
     (255/255, 117/255, 130/255),                 #Farbe 100 °C - 500 °C
     (255/255, 1/255, 25/255),                    #Farbe 500 °C - 1000 °C
     (150/255, 0/255, 14/255)]                    #Farbe > 1000 °C
    
    #labels = ['Raumwärme','Warmwasser', '< 100 °C', '100 °C - 500 °C', '500 °C - 1000 °C', '>1000 °C']
    labels = ['Space heating', 'Hot water', '< 100 °C', '100 °C - 500 °C', '500 °C - 1000 °C', '>1000 °C']
    
    y_plot = np.vstack([y.iloc[:,0].tolist(), 
                y.iloc[:,1].tolist(),
                y.iloc[:,2].tolist(),
                y.iloc[:,3].tolist(),
                y.iloc[:,4].tolist(),
                y.iloc[:,5].tolist()])
    
    return  new_colors, labels, y_plot



def plot_layout(new_colors, labels, y_plot, x_plot, xtick):
    # fig, ax = plt.subplots(figsize= (20,4))              # year
    fig, ax = plt.subplots(figsize= (10,4))              # day 
    ax.stackplot(x_plot, y_plot, labels=labels, colors = new_colors )
    # ax.set_xlabel('Zeit',fontsize=18)
    # ax.set_ylabel('Leistung normiert in kW',fontsize=18)

    ax.set_xlabel('Time',fontsize=18) #englisch
    ax.set_ylabel('Power in kW',fontsize=18) #englisch

    plt.xticks(x_plot[::xtick], fontsize=18, rotation = 45) #x_plot[::96].str[:10]
    plt.yticks(fontsize=18)
    plt.legend(reversed(plt.legend().legendHandles), reversed(labels), loc='upper right', fontsize=16)
    plt.xlim(left=0, xmax=max(x_plot))
    plt.ylim(bottom=0, top=220) #optional
    plt.grid()


def day_electrical(y):
    x_plot = pd.date_range(start='2020-01-01', end='2020-01-02', freq = '0.25H', closed ='left') # 15 min intevals for one day
    x_plot = x_plot.strftime('%H:%M') 
    xtick = 8
    new_colors, labels, y_plot = plot_el(y)
    plot_layout(new_colors, labels, y_plot, x_plot, xtick)

    #plt.title('Synthetical load profile of WZ08 '+ str(industry_type) + ' '+ industry_name, fontsize=20)
    plt.show()

    
def year_electrical(y, industry_name, industry_type, path):
    
    x_plot = y.index
    x_plot = x_plot.strftime('%H:%M       %Y-%m-%d')
    
    # x_plot = y.index.astype(str)
    x_plot = x_plot[:1344] #1344 --> 2 Wochen
    
    y= y.iloc[:1344] #first two weeks
    
    xtick = 96
    new_colors, labels, y_plot = plot_el(y)
    plot_layout(new_colors, labels, y_plot, x_plot, xtick)
    
    #plt.title('Synthetical load profile of WZ08 '+ str(industry_type) + ' '+ industry_name, fontsize=20)
    plt.savefig(path + "\\Electrical\\Diagramme\\" +str(industry_name) +'_Diagram.png', bbox_inches = 'tight')
    
    plt.show()

def day_thermal(y, industry_type, industry_name, path):
    x_plot = pd.date_range(start='2020-01-01', end='2020-01-02', freq = '0.25H', closed ='left') # 15 min intevals for one day
    x_plot = x_plot.strftime('%H:%M') 
    xtick = 8
    new_colors, labels, y_plot = plot_th(y)
    plot_layout(new_colors, labels, y_plot, x_plot, xtick)
    
    #plt.title('Synthetical load profile of WZ08 '+ str(industry_type) + ' '+ industry_name, fontsize=20)
    plt.show()

    
def year_thermal(y, industry_name, industry_type, path):
    
    x_plot = y.index
    x_plot = x_plot.strftime('%H:%M       %Y-%m-%d')
    
    # x_plot = y.index.astype(str)
    
    x_plot = x_plot[:1344]
    y= y.iloc[:1344] #first two weeks
    
    xtick = 96
    new_colors, labels, y_plot = plot_th(y)
    plot_layout(new_colors, labels, y_plot, x_plot, xtick)
    
    #plt.title('Synthetical load profile of WZ08 '+ str(industry_type) + ' '+ industry_name, fontsize=20)
    plt.savefig(path + "\\Thermal\\Diagramme\\" +str(industry_name) +'_Diagram.png', bbox_inches = 'tight')
    plt.show()


