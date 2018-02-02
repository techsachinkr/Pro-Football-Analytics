# -*- coding: utf-8 -*-
"""
Spyder Editor
Created by : Sachin Kumar
Id: 200204275

"""
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as npy


page=requests.get("https://www.pro-football-reference.com/years/2017/games.htm")

soupObj = BeautifulSoup(page.text,'lxml')   
tableGames= soupObj.find("table",id="games")
table_rows= tableGames.findAll('tr')

table_data= [[ td.get('href') if td.has_attr('href')   else td.getText() for td in table_rows[cntr].findAll(['th','td','a'])] for cntr in range(len(table_rows))] 

finalgamesdata =[[data for data in table_data[cntr] ]for cntr in range(len(table_rows)) if len(table_data[cntr]) > 1] 

table_data[0]=['Week',
 'Day',
 'Date',
 'Time',
 'Winner/tie',
 'Winner_team_page',
 'Dummyvar',
 'Loser/tie',
 'Losing_team_page',
 'Boxscore ind',
 'Boxscore_Page',
 'PtsW',
 'PtsL',
 'YdsW',
 'TOW',
 'YdsL',
 'TOL']

gamesdata = pd.DataFrame(finalgamesdata[1:],columns=table_data[0])

#Gt play-by-play scores
data2=[]
for game in gamesdata['Boxscore_Page']:
    print (game)
    if len(game) > 10:
        url2="http://www.pro-football-reference.com" + str(game)
        pageb=requests.get(url2)             
        comments=re.compile("<!--|-->")                       
        soupObj = BeautifulSoup(comments.sub("",pageb.text),'lxml')   
        tablePbp= soupObj.find("table",id="pbp")
        if tablePbp is not None:
           table_rows= tablePbp.findAll('tr')
        else:
            table_rows=''
            
        table_data= [[td.getText() for td in table_rows[cntr].findAll(['th','td'])] for cntr in range(len(table_rows))] 
        data2.extend([[data for data in table_data[cntr] ]for cntr in range(len(table_rows)) if len(table_data[cntr]) > 1] )
         


findata=pd.DataFrame(data2)    
# exporting play by play data to csv
findata.to_csv(r'C:\Users\sachi\Documents\DDDM code\finalfile.csv')