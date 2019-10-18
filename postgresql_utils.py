# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:16:42 2019

@author: jacqu

Utils functions to connect to database 
"""
import psycopg2

def reach_chembl():
    """ Connects to chembl_25 local database and returns connection, cursor to perform requests """
    
    try : 
        connection = psycopg2.connect(user = "postgres",
                                      password = "zunjoc",
                                      host = "localhost",
                                      port = "5432",
                                      database = "chembl_25")
    
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")
    
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
        
        return connection, cursor
    
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        return 
    
def close(connection, cursor):
    """closes connexion and cursor """
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
    