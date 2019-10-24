# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 16:15:41 2019

@author: jacqu

GitHub notebook to get all data in chembl with valid type, organized by targets, 
into a pandas dataframe 

Conditions on the data we retrieve : (WHERE request section)
    - confidence score >=8 
    - activity type in ('EC50', 'IC50', 'Ki', 'Kd', 'XC50', 'AC50', 'Potency')
    - activities.standard_relation IN ('=', '<') 
    - activities.potential_duplicate = 0
    - assays.confidence_score >= 8 
    - target_dictionary.target_type = 'SINGLE PROTEIN' 
    - target_dictionary.organism = 'Homo sapiens'
    
# Optional : add the MCF and RO5 filters to the collected columns 
    
structural_alert_sets.set_name       AS alerts
JOIN compound_structural_alerts ON compound_structural_alerts.molregno = activities.molregno
JOIN structural_alert_sets ON structural_alert_sets.alert_set_id = compound_structural_alerts.alert_id
    
"""
import psycopg2
from postgresql_utils import * 
from chembl_requests import get_target_act, get_targets_list
import pandas as pd

# 1 / Connect to chembl25 database on localhost port 5432
connection, cursor = reach_chembl()

qtext = """
SELECT
  activities.doc_id                    AS doc_id,
  activities.standard_value            AS standard_value,
  molecule_hierarchy.parent_molregno   AS molregno,
  compound_structures.canonical_smiles AS canonical_smiles,
  molecule_dictionary.chembl_id        AS chembl_id,
  target_dictionary.tid                AS tid,
  target_dictionary.chembl_id          AS target_chembl_id,
  target_dictionary.organism           AS organism,
  target_dictionary.pref_name          AS target_name,
  protein_family_classification.l1     AS l1,
  protein_family_classification.l2     AS l2,
  protein_family_classification.l3     AS l3
  
FROM activities
  JOIN assays ON activities.assay_id = assays.assay_id
  JOIN target_dictionary ON assays.tid = target_dictionary.tid
  JOIN target_components ON target_dictionary.tid = target_components.tid
  JOIN component_class ON target_components.component_id = component_class.component_id
  JOIN protein_family_classification ON component_class.protein_class_id = protein_family_classification.protein_class_id
  JOIN molecule_dictionary ON activities.molregno = molecule_dictionary.molregno
  JOIN molecule_hierarchy ON molecule_dictionary.molregno = molecule_hierarchy.molregno
  JOIN compound_structures ON molecule_hierarchy.parent_molregno = compound_structures.molregno
  
  
WHERE activities.standard_units = 'nM' AND
      activities.standard_type IN ('EC50', 'IC50', 'Ki', 'Kd', 'XC50', 'AC50', 'Potency') AND
      activities.data_validity_comment IS NULL AND
      activities.standard_relation IN ('=', '<') AND
      activities.potential_duplicate = 0 AND assays.confidence_score >= 8 AND
      target_dictionary.target_type = 'SINGLE PROTEIN' AND
      target_dictionary.organism = 'Homo sapiens'"""

cursor.execute(qtext)
df = pd.DataFrame(cursor.fetchall())
close(connection, cursor)

df.columns = [cursor.description[i].name for i in range(12)] # Change if we collect more or less columns
df = df.where((pd.notnull(df)), None)

# Save dataframe : 
df.to_csv('C:/Users/jacqu/Documents/data/CHEMBL.csv')

# Count target occurences in dataframe : 

grouped_targets = df.groupby('target_name').count()
grouped_targets= grouped_targets.sort_values('standard_value', ascending=False)

# Get top 100 targets : 

top_100 = grouped_targets[:100]
top_100.to_csv('C:/Users/jacqu/Documents/data/CHEMBL_top100.csv')

import matplotlib.pyplot as plt
import seaborn as sns

sns.scatterplot(np.arange(100),top_100['doc_id'])
plt.ylabel('Nb assayed values')
plt.xlabel('Nb targets')

# Compare with BDB top 100 : 
top_100_bdb = pd.read_csv('C:/Users/jacqu/Documents/data/bindingdb/top100.csv')
top_100_bdb = top_100_bdb.groupby('target').count()
top_100_bdb= top_100_bdb.sort_values('IC50', ascending=False)

# 3 - example : get all affinities for CHEMBL240
herg = df[df['target_chembl_id']=='CHEMBL240']