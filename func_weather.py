# -*- coding: utf-8 -*-

import random
import pandas as pd
import requests
import re


class Weather(object):
    def __init__(self) -> None:
        self.df = pd.read_csv("China-City-List.csv", delimiter=",")

    def _build_data(self):
        df = self.df.copy()
        print(df)
        # print(df)
        # df["shouzi"] = df["chengyu"].apply(lambda x: x[0])
        # df["mozi"] = df["chengyu"].apply(lambda x: x[-1])
        #
        # df["shouyin"] = df["pingyin"].apply(lambda x: x.split(" ")[0])
        # df["moyin"] = df["pingyin"].apply(lambda x: x.split(" ")[-1])
        #
        # cys = dict(zip(df["chengyu"], df["moyin"]))
        # zis = df.groupby("shouzi").agg({"chengyu": set})["chengyu"].to_dict()
        # yins = df.groupby("shouyin").agg({"chengyu": set})["chengyu"].to_dict()
        #
        # return cys, zis, yins
    def get_text(self, name, day):
        if(day == 0):
            day_name = '今天'
        elif(day == 1):
            day_name = '明天'
        elif(day == 2):
            day_name = '后天'
        df = self.df.copy()
        # print(df)
        filtered_df = df.loc[df["Location_Name_ZH"] == name]
        if filtered_df.empty:
            return False
        selected_row = filtered_df.iloc[0]
        row_index = selected_row.name

        location = df.iloc[row_index]['Location_ID']

        url = 'https://devapi.qweather.com/v7/weather/3d?location=' + location + '&key=a7a8020835354483ac47da08f3287164'
        response = requests.get(url)
        contents = response.json()
        # print(contents)
        data = contents['daily'][day]
        text = name + day_name + '天气：'
        text += data['textDay']
        if (data['textNight'] != data['textDay']):
            text += '转' + data['textNight']
        text += '，温度：' + data['tempMin']
        text += '°C~' + data['tempMax'] + '°C'
        text += '，' + data['windDirDay'] + data['windScaleDay'] + '级'
        text += '。日出时间：' + data['sunrise']
        text += '，日落时间：' + data['sunset'] + '。'
        text += "\n" + contents['fxLink']
        print(text)
        return text


wt = Weather()

if __name__ == "__main__":
    content = '杭州今天天气'
    times = re.findall(r"(今天|明天|后天|今日|明日|后日)", content)
    times = times[0]
    day = 0
    if (times == '今天' or times == '今日'):
        day = 0
    elif (times == '明天' or times == '明日'):
        day = 1
    elif (times == '后天' or times == '后日'):
        day = 2
    content = re.sub(r"[^\u4e00-\u9fa5]", "", content)
    content = re.sub(r"今天|明天|后天|今日|明日|后日|天气", "", content)

    text = wt.get_text(content, day)
    print(text)
