# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:23:58 2019

@author: jacqu

Process DUD to extract SMILES and labels for each of the actives/ ligands sets 
"""

import pandas as pd 
import os 
import numpy as np

dud_repo = 'C:/Users/jacqu/Documents/mol2_resource/dud/all'
os.chdir(dud_repo)

dict_a, dict_d= {}, {}

for target_folder in os.listdir(dud_repo):
    a_smiles, d_smiles = [], []
    
    with open(f'{target_folder}/actives_final.ism', 'r') as f : 
        actives = f.readlines()
        for l in actives :
            a_smiles.append(l.split(' ')[0])
        

    with open(f'{target_folder}/decoys_final.ism', 'r') as f : 
        dec = f.readlines()
        for l in dec :
            d_smiles.append(l.split(' ')[0])
        
    dict_a[target_folder] = a_smiles
    dict_d[target_folder] =  d_smiles
        
# Save dicts to data
np.save('C:/Users/jacqu/Documents/data/DUD_a.npy', dict_a)
np.save('C:/Users/jacqu/Documents/data/DUD_d.npy', dict_d)
            
        
            
