import pandas as pd
import numpy as np
from pandasgui import show
import os
import yfinance as yf
from datetime import datetime, timedelta

directory = sorted(os.listdir('/home/gun/Documents/CalculatedRatios'))

num_rows = []
stocks = []
list_of_df = []

for i in directory:
    file = pd.read_excel(f'/home/gun/Documents/CalculatedRatios/{i}')
    num = file.shape[0]
    num_rows.append(num)

longes_row = max(num_rows)

for i in directory:
    stock_name = os.path.splitext(i)[0]
    stocks.append(stock_name)

def get_row_or_zero(df, row_index):
    if row_index < df.shape[0]:
        return df.iloc[row_index]
    else:
        return pd.Series([0] * df.shape[1], index=df.columns)

for j in range(longes_row + 1):
    hisseler_df = pd.DataFrame()
    for i in directory:

        file = pd.read_excel(f'/home/gun/Documents/CalculatedRatios/{i}')
        file = file.rename(columns={'Unnamed: 0': 'Tarih'})

        file = get_row_or_zero(file, j)
        hisseler_df = hisseler_df._append(file, ignore_index=True)
    hisseler_df.set_index(pd.Index(stocks), inplace=True)

    hisseler_df['F/K'] = hisseler_df['F/K'].apply(lambda x: 0 if x >= 100 or x <= 0 else x)
    min_fk = hisseler_df['F/K'].min()
    max_fk = hisseler_df['F/K'].max()
    normalize_fk = (hisseler_df['F/K'] - min_fk) / (max_fk - min_fk)
    # hisseler_df['Norm'] = normalize_fk
    fk_puan = 1 - normalize_fk
    fk_puan = fk_puan.apply(lambda x: 0 if x >= 1 or x <= 0 else x)
    hisseler_df['F/K Puan'] = fk_puan

    hisseler_df['PD/DD'] = hisseler_df['PD/DD'].apply(lambda x: 0 if x >= 100 or x <= 0 else x)
    min_pd_dd = hisseler_df['PD/DD'].min()
    max_pd_dd = hisseler_df['PD/DD'].max()
    normalize_pd_dd = (hisseler_df['PD/DD'] - min_pd_dd) / (max_pd_dd - min_pd_dd)
    # hisseler_df['PD NORM'] = normalize_pd_dd
    pd_dd_puan = 1 - normalize_pd_dd
    pd_dd_puan = pd_dd_puan.apply(lambda x: 0 if x >= 1 or x <= 0 else x)
    hisseler_df['PD/DD Puan'] = pd_dd_puan

    min_cari_oran = hisseler_df['Cari Oran'].min()
    max_cari_oran = hisseler_df['Cari Oran'].max()
    normalize_cari_oran = (hisseler_df['Cari Oran'] - min_cari_oran) / (max_cari_oran - min_cari_oran)
    normalize_cari_oran = normalize_cari_oran.apply(lambda x: 0 if x < 0 else x)
    hisseler_df['Cari Oran Puan'] = normalize_cari_oran

    kaldirac_puan = 1 - hisseler_df['Kaldıraç Oranı']
    kaldirac_puan = kaldirac_puan.apply(lambda x: 0 if x <= 0 or x >= 1 else x)
    hisseler_df['Kaldirac Puan'] = kaldirac_puan

    brutkar_ceyrek_puan = hisseler_df['Brüt Kar Marjı Çeyreklik'].apply(lambda x: 0 if x < 0 else x)
    hisseler_df['Brüt Kar Marjı Çeyreklik Puan'] = brutkar_ceyrek_puan.apply(lambda x: 1 if x > 1 else x)

    brutkar_yil_puan = hisseler_df['Brüt Kar Marjı Yıllık'].apply(lambda x: 0 if x < 0 else x)
    hisseler_df['Brüt Kar Marjı Yıllık Puan'] = brutkar_yil_puan.apply(lambda x: 1 if x > 1 else x)

    netkarmarji_ceyrek_puan = hisseler_df['Net Kar Marjı Çeyreklik'].apply(lambda x: 0 if x < 0 else x)
    hisseler_df['Net Kar Marjı Çeyreklik Puan'] = netkarmarji_ceyrek_puan.apply(lambda x: 1 if x > 1 else x)
    
    netkarmarji_yil_puan = hisseler_df['Net Kar Marjı Yıllık'].apply(lambda x: 0 if x < 0 else x)
    hisseler_df['Net Kar Marjı Yıllık Puan'] = netkarmarji_yil_puan.apply(lambda x: 1 if x > 1 else x)

    ozkaynak_karliligi_puan = hisseler_df['Özkaynak Karlılığı'].apply(lambda x: 0 if x < 0 else x)
    hisseler_df['Özkaynak Karlılığı Puan'] = ozkaynak_karliligi_puan.apply(lambda x: 1 if x > 1 else x)

    hisseler_df['Toplam Puan'] = (hisseler_df['F/K Puan'] + hisseler_df['PD/DD Puan'] +
                                  hisseler_df['Cari Oran Puan'] + hisseler_df['Kaldirac Puan'] + 
                                  hisseler_df['Brüt Kar Marjı Çeyreklik Puan'] + 
                                  hisseler_df['Brüt Kar Marjı Yıllık Puan'] + 
                                  hisseler_df['Net Kar Marjı Çeyreklik Puan'] + 
                                  hisseler_df['Net Kar Marjı Yıllık Puan'] + 
                                  hisseler_df['Özkaynak Karlılığı Puan'])
   
    # hisseler_df = hisseler_df.sort_values(by='Toplam Puan', ascending=False)

    stck = (hisseler_df.index.tolist())
    percent_change = []
    last_trading_day = '2024/02/15'
    # stck = stck[:5]
    # stck = stck[111:112]
    # list_of_df.append(hisseler_df)

    for d in stck:
        yfstock = d + '.IS'
        amele = pd.read_excel('/home/gun/Documents/Amele/RaporTarihleri/{}.xlsx'.format(d)).T
        amele = amele[0].iloc[1:]
        file_sell_date = pd.read_excel('/home/gun/Documents/Amele/RaporTarihleri/{}.xlsx'.format(d)).T

        if j in amele.index:    #Check If Buy Date Exists In File
            raw_date = amele[j]
            raw_date = datetime.strptime(raw_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            date = datetime.strptime(raw_date, '%Y-%m-%d')
            buy_date = date + timedelta(days=1)

            file_sell_date[0].iloc[0] = last_trading_day   # If Buy Day Exists Get Sell Date
            raw_sell_date = file_sell_date[0].iloc[j]
            raw_sell_date = datetime.strptime(raw_sell_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            sell_date = datetime.strptime(raw_sell_date, '%Y-%m-%d')
            sell_date = sell_date + timedelta(days=1)
            
            while buy_date.weekday() >= 5:
                days_until_monday = (7 - buy_date.weekday()) % 7
                buy_date += timedelta(days=days_until_monday)
            buy_date_str = buy_date.strftime('%Y-%m-%d')

            while sell_date.weekday() >= 5:
                days_until_monday2 = (7 - sell_date.weekday()) % 7
                sell_date += timedelta(days=days_until_monday2)

            data = yf.download(yfstock, start=buy_date_str)['Close']

            #Adjusting Buy Order According To Available YF_DATES
            buy_day_difference = data.index[0] - buy_date

            if buy_date in data.index:
                buy_date = buy_date.strftime('%Y-%m-%d')
                buy_price = round(data.iloc[0], 2)

            elif 0 < buy_day_difference.days <= 10:
                buy_date = data.index[0]
                buy_date = buy_date.strftime('%Y-%m-%d')
                buy_price = round(data.iloc[0], 2)

            else:
                buy_price = 0
           
            #Adjusting Sell Order According To Available YF_DATES
            closest_index = min(filter(lambda date: date > sell_date, data.index))
            sell_day_difference = (closest_index - sell_date).days
            closest_index = datetime.strftime(closest_index, '%Y-%m-%d')

            if sell_date in data.index:    #Check If YF_Data Has Older Date
                sell_price = round(data[sell_date], 2)
                sell_date = sell_date.strftime('%Y-%m-%d')

            elif 0 < sell_day_difference <= 10:  #Filter For Last Date (Tryna Prevent Infinite Last YF_DATE Loop)
                sell_date = closest_index
                sell_price = round(data[closest_index], 2)

            else:
                sell_price = 0

            print(d)
            print(buy_date)
            print(buy_price)
            print(sell_date)
            print(sell_price)
            
            change = pd.Series([buy_price, sell_price])
            pct_change = change.pct_change()
            percent_change.append(round(pct_change[1] * 100, 2))
            print(pct_change[1] * 100)

        else:
            percent_change.append(0)
        # break
    hisseler_df['Getiri'] = percent_change
    hisseler_df = hisseler_df.sort_values(by='F/K Puan', ascending=False)
    show(hisseler_df)
    # break
