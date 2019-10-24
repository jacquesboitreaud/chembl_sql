# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:55:14 2019

@author: jacqu

Processing DUD + and - dictionaries to link to chembl targets , 
and enrich in negatives 

"""

import numpy as np 
import pandas as pd 


# Open DUD_a and DUD_d: 
dud_a , dud_d = np.load('C:/Users/jacqu/Documents/data/DUD_a.npy').item(),\
np.load('C:/Users/jacqu/Documents/data/DUD_d.npy').item()

# Optional: cluster targets by groups or load similarity clusters 

# Create dataframe with 102 columns of binary labels 
d = {}
for t in dud_a.keys():
    d[t] = []
    d['can']= [] # column for canonical smiles
    
for t in dud_a.keys():
    print(f'target {t}')
    for m in dud_a[t]: # for each molecule in actives: 
        d['can'].append(m)
        d[t].append(1)
        for other in dud_a.keys():
            if (other != t): # Those to which we assign a nan value 
                d[other].append(0)
                
df=pd.DataFrame.from_dict(d)

for t in dud_d.keys():
    print(f'target {t}')
    for m in dud_d[t]: # for each molecule in actives: 
        d['can'].append(m)
        d[t].append(-1)
        for other in dud_a.keys():
            if (other != t): # Those to which we assign a nan value 
                d[other].append(0)

         
df_decoys=pd.DataFrame.from_dict(d)

df=df.append(df_decoys, ignore_index=True)

df.to_csv('C:/Users/jacqu/Documents/data/DUD_dataframe.csv')
                
    
    
    