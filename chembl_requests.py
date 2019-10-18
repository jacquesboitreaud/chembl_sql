# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:24:33 2019

@author: jacqu

Functions to request specific data in CHEMBL database

"""

def get_target_act(cursor, target_id):
    """ 
    Cursor : instance to request in database
    target_id : CHEMBL target id (ex 'CHEMBL1827'), string type 
    """
    
    cursor.execute(f"""SELECT m.chembl_id AS compound_chembl_id,   
    s.canonical_smiles,   
    r.compound_key,   
    a.description                   AS assay_description,   act.standard_type,   
    act.standard_relation,   
    act.standard_value,   
    act.standard_units,   
    act.activity_comment 
    FROM compound_structures s,   
    molecule_dictionary m,   
    compound_records r,   
    docs d,   
    activities act,   
    assays a,   
    target_dictionary t 
    WHERE s.molregno = m.molregno 
    AND m.molregno       = r.molregno 
    AND r.record_id      = act.record_id 
    AND r.doc_id         = d.doc_id 
    AND act.assay_id     = a.assay_id 
    AND a.tid            = t.tid 
    AND t.chembl_id      = '{target_id}';""")
    
    result=cursor.fetchall()
    
    return result

def get_targets_list(cursor):
    """ Returns target details for all protein targets in chembl """
    
    cursor.execute(f"""SELECT t.chembl_id AS target_chembl_id,
    t.pref_name        AS target_name,
    t.target_type,
    c.accession        AS protein_accession,
    c.sequence         AS protein_sequence
    FROM target_dictionary t
      JOIN target_type tt ON t.target_type = tt.target_type
      JOIN target_components tc ON t.tid = tc.tid
      JOIN component_sequences c ON tc.component_id = c.component_id
    AND tt.parent_type  = 'PROTEIN';""")
    
    result = cursor.fetchall()
    return result    