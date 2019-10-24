# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 09:02:30 2019

@author: jacqu

CHEMBL API Bioactivites data
"""

import pandas as pd
d={}
d['can']=[]
d['Ki']=[]


from chembl_webresource_client.new_client import new_client
target = new_client.target
activity = new_client.activity
herg = target.search('herg')[0]
herg_activities = activity.filter(target_chembl_id=herg['target_chembl_id']).filter(standard_type="Ki")

cpt=0
for a in herg_activities : 
    cpt+=1
    d['can'].append(a['canonical_smiles'])
    d['Ki'].append(a['value'])
    if(cpt%10000==0):
        print(cpt)
    
df=pd.DataFrame.from_dict(d)

df.to_csv('chembl_herg.csv')


