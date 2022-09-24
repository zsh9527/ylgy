#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import requests
import time
import struct
import base64

describe = '''
usage: python|python3 main.py

description: 该程序用于羊了个羊快速通关, 可刷新通关次数
require: 配置项: 1. token字段 2. 刷新通关次数executeTimes(默认为9), 每次需要1分钟
author: zsh
date: 2022-09-23
'''

# 配置项
token = ''
executeTimes = 9
winCount = 0
matchPlayInfo = ''

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'Connection': 'keep-alive',
    'content-type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2012K11C Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/4629 MicroMessenger/8.0.27.2220(0x28001B37) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
    't': token
}

getMapUrl = 'https://cat-match.easygame2021.com/sheep/v1/game/map_info_ex?matchType=3'
reportUrl = 'https://cat-match.easygame2021.com/sheep/v1/game/game_over_ex?'
getInfoUrl = 'https://cat-match.easygame2021.com/sheep/v1/game/personal_info?'

# 检查token
def checkToken():
    global winCount
    if token == '' :
        print("请配置token")
        exit(1)
    try:
        result = requests.get(getInfoUrl, headers=headers).json()
        if result['err_code'] != 0:
            print(result['err_msg'])
            print("token过期或配置不正确")
            exit(1)
        else:
            winCount = result['data']['win_count']
            print(result['data']['nick_name'], ": 当前通关次数为", winCount)
    except Exception as e:
        print("请求失败, 请检查token过期或配置不正确")
        exit(1)

# @reference https://www.52pojie.cn/thread-1690631-1-1.html
def calculateMatchPalyInfo():
    global matchPlayInfo
    mapResutl = requests.get(getMapUrl, headers=headers).json()
    mapMD5 = map_md5 = mapResutl['data']['map_md5'][1]
    mapsUrl = f'https://cat-match-static.easygame2021.com/maps/{mapMD5}.txt'  # 由于每天获取的地图不一样，需要计算地图大小
    map = requests.get(mapsUrl).json()
    levelData = map['levelData']
    p = []
    for h in range(len(sum(levelData.values(), []))):  # 生成操作序列
        p.append({'chessIndex': 127 if h > 127 else h, 'timeTag': 127 if h > 127 else h})
    GAME_DAILY = 3
    data = struct.pack('BB', 8, GAME_DAILY)
    for i in p:
        c, t = i.values()
        data += struct.pack('BBBBBB', 34, 4, 8, c, 16, t)
    matchPlayInfo = base64.b64encode(data).decode('utf-8')

def execute():
    global winCount
    for i in range(0, executeTimes): 
        mapResutl = requests.get(getMapUrl, headers=headers).json()
        # 时间戳
        mapSeed2 = mapResutl['data']['map_seed_2']
        # 休眠60s, 否则无法更新记录成功
        time.sleep(60)
        result = requests.post(reportUrl, headers=headers, 
                                json={'rank_score': 1, 'rank_state': 1, 'rank_time': 15, 'rank_role': 1, 'skin': 1, 'MapSeed2': mapSeed2, 'MatchPlayInfo': matchPlayInfo, 'Version': '0.0.1'})
        print('上传结果', result.text)
        # 检查是否更新成功        
        info = requests.get(getInfoUrl, headers=headers).json()
        newWinCount = info['data']['win_count']
        if (newWinCount == winCount):
            print('更新失败, 可能被羊了个羊小程序拉黑')
        else:
            print('更新成功, 通关次数', winCount, '->', newWinCount)
            winCount = newWinCount

# 主函数
if __name__ == '__main__':
    print(describe)
    checkToken()
    calculateMatchPalyInfo()
    print('刷新通关次数(每次需要1分钟):', executeTimes)
    execute()
