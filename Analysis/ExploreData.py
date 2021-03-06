# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:40:57 2018

@author: LFVARGAS
"" 

@Description Outliers detectetion

"""

import  os,sys
sys.path.append('../Factory')# commodity folder 

import numpy as np
import pandas as pd
from pandas.tools.plotting import autocorrelation_plot
import matplotlib.pyplot as plt


from Commodity import Commodity
#from matplotlib.backends.backend_pdf import PdfPages
#Constans
os.chdir("../")#AFFECT ALL THE EXETCUTION

RELATIVE_PATH="./data/Cleaned/"

FILE_NAME= RELATIVE_PATH+"Monthly_data_cmo_step3"
FILE_FORMAT=".csv"
GrouperColumns=["CommodityId","APMC"]


DF_Month= pd.read_csv("./%s%s"%(FILE_NAME,FILE_FORMAT))

DF_Month["date"]=pd.to_datetime(DF_Month["date"], format='%Y-%m-%d')


commodityManager=Commodity()


def flagMostFluctuation(DataFrame_View):
    by_group = DataFrame_View.groupby(["CommodityId"])
    
#    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
#                key=lambda x: len(x["rate_monthly_fluc"]),  # sort by number of rows (len of subDataFrame)
#                reverse=True)  # reverse the sort i.e. largest first
    dataset= None
    for name, group in by_group:
        rate_monthly_fluc=group["rate_monthly_fluc"]
        rate_frequency_fluc=group["rate_frequency_fluc"]
        
        LIMIT=.7
        limitMonth=rate_monthly_fluc.quantile(LIMIT)
        limitFreq=rate_monthly_fluc.quantile(LIMIT)
        
        def comparable(x,y):
            if(x>y):
                return True
            else:
                return False
        
        group["Highest_Fluctuation_Month"]=rate_monthly_fluc.apply(lambda x: comparable(x,limitMonth))
        group["Highest_Fluctuation_Freq"]=rate_frequency_fluc.apply(lambda x: comparable(x,limitFreq))
        
        if dataset is None:
            dataset=group
        else: 
            dataset=dataset.append(group, ignore_index=True) 
               
    return dataset

def viewFlagged(DataFrame_View):  
    by_group = DataFrame_View.groupby(GrouperColumns)
    
    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
                key=lambda x: len(x[1]),  # sort by number of rows (len of subDataFrame)
                reverse=True)  # reverse the sort i.e. largest first
    for name, group in by_group:
        
        isHighFreq=group["Highest_Fluctuation_Freq"].iloc[0]
        isHighMonth=group["Highest_Fluctuation_Month"].iloc[0]
        if(isHighFreq ):
            realName= commodityManager.getNameById(name[0])
            displayName=str(name[0])+"-"+realName
            displayName=displayName+"-"+name[1]
            
            fig, ax  = plt.subplots(figsize=(8,10))
            ax.set_title(displayName)
            
            group=group.sort_values("date")
            
            
            group["date"]=pd.to_datetime(group["date"])
            group=group.set_index("date")
            group=group.sort_index()
            
            plt.plot(group.index,group["modal_price"] , label="Series")
            
            
            ax.legend(loc='best')
            
            plt.xticks(rotation=90)
            plt.show()
        else: 
            print("NO fluctuated")
    
        
DF_flag=flagMostFluctuation(DF_Month)

viewFlagged(DF_flag)

#DF_Season= pd.read_csv("./%s%s"%(FILE_OUT,FILE_FORMAT))

#DF_Season_Flag=flagMostFluctuation(DF_Season)

