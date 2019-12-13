# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 15:12:45 2019

@author: Parth
"""

import time
import threading
import urllib
import re
import io
import re
import sys
from time import sleep
import pickle
import os
from math import ceil
import active
from pathlib import Path
import pandas as pd
import concurrent.futures 
import psycopg2
import tweepy
start_time = time.time()
consumer_key='rNrnFupaEqKt0eb7hjbdHKdWg'
consumer_secret= 'DTTMoQOrCBmngaXmOnFhrBjdjwtT54x0AbGvNwwuqyYNWwEvc7'
access_token='1002268050513575936-gGrQUmDiMyCxO2Y88lc3ojqNzbtLGm'
access_token_secret='G572YTe2S5TQTTaXhFvl1WyNopa8ilrkgWSlCXBZQwU4C'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
word='passive'
query_word='Hiranandani'
query = "SELECT id, username,tweet_text, created_at,location,polarity FROM {}".format(query_word)

try:     
    conn = psycopg2.connect(database=query_word, user = "postgres", password = "parth123n@#*", host = "127.0.0.1", port = "5432")
except:
    print("Create database first")

cur= conn.cursor()


if(conn):
    '''
    Check if this table exits. If not, then create a new one.
    '''
    mycursor = conn.cursor()
    mycursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(word))
    if mycursor.fetchone()[0] != 1:
        cur.execute('''CREATE TABLE {} (USERNAME TEXT,LOCATION TEXT);'''.format(word))
        conn.commit()
    mycursor.close()

df=pd.read_sql(query,con=conn)

def get_uname(df):
    set1=set()
    likers=list()
    for j,i in df.iterrows(): 
        if i['id'] not in set1:
            if 'hiranandani' not in (i['username']).lower():
                try:
                    id1=active.get_user_ids_of_post_likes(i['id'])
                    likers.extend(id1)        
                    set1.add(i['id'])
                except:
                    continue
    set2=set()
    likers_uname=dict()
    
    for i in likers:   
        if i not in set2:
            u=api.get_user(i)
            likers_uname[u.screen_name]=u.location            
            set2.add(i)
            print(u.screen_name)


    return likers_uname



with concurrent.futures.ThreadPoolExecutor(8) as executor:
    future = executor.submit(get_uname, df)
    return_value = future.result()


print("--- %s seconds ---" % (time.time() - start_time))

u_name=list(df['list'])

for i in return_value:
    if i not in u_name:
        sql = "INSERT INTO {} (username,location) VALUES (%s, %s)".format(word)
        val = (i, return_value[i])
        cur.execute(sql,val)












