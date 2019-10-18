# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:32:48 2019

@author: jacqu

Connect to chembl database and retrieve bioactivities and molecules from it 
"""
import psycopg2
from postgresql_utils import * 
from chembl_requests import get_target_act, get_targets_list


# 1 / Connect to chembl25 database on localhost port 5432
connection, cursor = reach_chembl()
    
# 2 / Try requesting some bioactivities 
# Retrieve compound activity details for a target
"""
target = 'CHEMBL1824'
result = get_target_act(cursor, target)

print(f"{len(result)} bioactivities found for target {target}")
"""

result = get_targets_list(cursor)
print(f"{len(result)} protein targets found")
    
# 3 / Close connection to database 
close(connection, cursor)