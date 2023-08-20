# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 10:53:30 2023

@author: rwenzel
Version: 0.4.5
"""

# Packages
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

# Header
from .TickerRequest import *

class StratosphereRequest(TickerRequest):
    def __init__(self, ticker, headers_standard):
        super().__init__(ticker, headers_standard)
        self.__headers_standard = headers_standard
        
    ################################
    ###                          ###
    ###  Stratosphere Requests   ###
    ###                          ###
    ################################
    
    @property
    def returns(self):
        return self.__stratosphere_returns_abfrage()
    
    ###########################
    ###                     ###
    ###  Stratosphere Data  ###
    ###                     ###
    ###########################
    
    # Dummy Abfragen, um Fehler im Vorfeld abzufangen  
    def __stratosphere_returns_abfrage(self):
        
        if self.ticker is None or self.ticker == '':
            self.ticker = 'None'
            return None
        
        return self.__stratosphere_returns_df()
    
    # Hilfsfunktionen
    
    def __initialize_dataframe(self, index):
        df = pd.DataFrame([''], columns=["Summary"], index=index)
        return df
    
    # Eigentlichen Abfragen
    
    def __stratosphere_data_dict(self):
        
        url = f'https://www.stratosphere.io/company/{self.ticker}/'

        page = requests.get(url)
        
        if page.status_code != 200:
            return None
        
        page = BeautifulSoup(page.content, 'html.parser')

        """
        Der Header der Tabelle, quasi der Column Label
        Ausgabe als Liste
        """

        content = page.find('div', {'class':'w-full columns-1 gap-x-2.5 sm:columns-2 desktopSm:columns-3'}).find_all(string = True)

        data = [
            (content[0], content[1], content[2]),
            (content[0], content[3], content[4]),
            (content[0], content[5], content[6]),
            (content[0], content[7], content[8]),
            (content[0], content[9], content[10]),
            
            (content[11], content[12], content[13]),
            (content[11], content[14], content[15]),
            (content[11], content[16], content[17]),
            (content[11], content[18], content[19]),
            (content[11], content[20], content[21]),
            (content[11], content[22], content[23]),
            
            (content[24], content[25], content[26]),
            (content[24], content[27], content[28]),
            (content[24], content[29], content[30]),
            (content[24], content[31], content[32]),
            
            (content[33], content[34], content[35]),
            (content[33], content[36], content[37]),
            (content[33], content[38], content[39]),
            (content[33], content[40], content[41]),
            (content[33], content[42], content[43]),
            (content[33], content[44], content[45]),
            
            (content[46], content[47], content[48]),
            (content[46], content[49], content[50]),
            (content[46], content[51], content[52]),
            (content[46], content[53], content[54]),
            (content[46], content[55], content[56]),
            
            (content[57], content[58], content[59]),
            (content[57], content[60], content[61]),
            (content[57], content[62], content[63]),
            (content[57], content[64], content[65]),
            
            (content[66], content[67], content[68]),
            (content[66], content[69], content[70]),
            (content[66], content[71], content[72]),
            (content[66], content[73], content[74]),
            (content[66], content[75], content[76]),
            (content[66], content[77], content[78]),
            (content[66], content[79], content[80]),
            (content[66], content[81], content[82]),
            (content[66], content[83], content[84]),
            (content[66], content[85], content[86]),
            
            (content[87], content[88], content[89]),
            (content[87], content[90], content[91]),
            (content[87], content[92], content[93]),
            (content[87], content[94], content[95]),
            (content[87], content[96], content[97]),
            (content[87], content[98], content[99]),
            (content[87], content[100], content[101]),
        ]
        
        dfs = {}
        
        for col, idx, val in data:
            if col not in dfs:
                dfs[col] = pd.DataFrame(columns=[col])
            dfs[col].loc[idx] = val
        
        dict_stratosphere_summary = dfs 
    
        return dict_stratosphere_summary

    # Returns (5Yr Avg)
    def __stratosphere_returns_df(self):
        
        data = self.__stratosphere_data_dict()
        
        if data != None:
            df_stratosphere_returns = data["Returns (5Yr Avg)"]
        else:
            return data
        
        return df_stratosphere_returns
    
    # Dividends
    def __stratosphere_dividends_df(self):
        
        data = self.__stratosphere_data_dict()
        
        df_stratosphere_dividends = data["Dividends"]
        
        return df_stratosphere_dividends
    
    # All
    def __stratosphere_summary_df(self):
        
        data = self.__stratosphere_data_dict()
        
        df1_1 = self.__initialize_dataframe(data["Basic"].columns)
        df2_1 = self.__initialize_dataframe(data["Margins"].columns)
        df3_1 = self.__initialize_dataframe(data["Returns (5Yr Avg)"].columns)
        df4_1 = self.__initialize_dataframe(data["Valuation (TTM)"].columns)
        df5_1 = self.__initialize_dataframe(data["Valuation (NTM)"].columns)
        df6_1 = self.__initialize_dataframe(data["Per Share"].columns)
        df7_1 = self.__initialize_dataframe(data["Growth (CAGR)"].columns)
        df8_1 = self.__initialize_dataframe(data["Dividends"].columns)

        df_stratosphere_summary = pd.concat([df1_1, data["Basic"].rename(columns={'Basic': 'Summary'}),
                                             df2_1, data["Margins"].rename(columns={'Margins': 'Summary'}),
                                             df3_1, data["Returns (5Yr Avg)"].rename(columns={'Returns (5Yr Avg)': 'Summary'}),
                                             df4_1, data["Valuation (TTM)"].rename(columns={'Valuation (TTM)': 'Summary'}),
                                             df5_1, data["Valuation (NTM)"].rename(columns={'Valuation (NTM)': 'Summary'}),
                                             df6_1, data["Per Share"].rename(columns={'Per Share': 'Summary'}),
                                             df7_1, data["Growth (CAGR)"].rename(columns={'Growth (CAGR)': 'Summary'}),
                                             df8_1, data["Dividends"].rename(columns={'Dividends': 'Summary'})
                                             ], axis=0)
        
        return df_stratosphere_summary