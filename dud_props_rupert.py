# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:26:06 2019

@author: jacqu

Add chemical properties to DUD dataframe 
For execution on rupert
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem import Draw, QED, Crippen, Descriptors, rdMolDescriptors, GraphDescriptors
import pandas as pd

DUD = pd.read_csv('/home/mcb/jboitr/data/DUD_dataframe.csv')

smiles = list(DUD['can'])
d={}
prop_names=['QED','logP','molWt','maxCharge','minCharge','valence','TPSA','HBA','HBD','jIndex']
for name in prop_names : 
    d[f'{name}']=[]


for i,s in enumerate(smiles) : 
    if(i%10000==0):
        print(i)
    m=Chem.MolFromSmiles(s)
    if(m==None or 'i' in s or '.' in s):
        DUD=DUD.drop(i)
        print(s, i)
    else:
        d['QED'].append(QED.default(m))
        d['logP'].append(Crippen.MolLogP(m))
        d['molWt'].append(Descriptors.MolWt(m))
        d['maxCharge'].append(Descriptors.MaxPartialCharge(m))
        d['minCharge'].append(Descriptors.MinPartialCharge(m))
        d['valence'].append(Descriptors.NumValenceElectrons(m))
        d['TPSA'].append(rdMolDescriptors.CalcTPSA(m))
        d['HBA'].append(rdMolDescriptors.CalcNumHBA(m))
        d['HBD'].append(rdMolDescriptors.CalcNumHBD(m))
        d['jIndex'].append(GraphDescriptors.BalabanJ(m))
    
df = pd.DataFrame.from_dict(d)

df_merge = pd.merge(df, DUD, on=df.index)

df_merge.to_csv('/home/mcb/jboitr/data/DUD_full.csv')
