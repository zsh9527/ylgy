#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import requests
import time

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
matchPlayInfo = 'CAMiBQjdARAAIgYI3gEQ2QQiBgiLAhCOAyIGCIYCEIgCIgYIiQIQuAMiBgiIAhCaAiIGCPkBEPcCIgYI/AEQoAQiBgiEAhCCAyIGCP0BEIUCIgYI7gEQ2AMiBgjqARCJAiIGCOUBEN8BIgYI5AEQqAIiBgjwARChBSIGCNYBEPABIgYIigIQ1wQiBgj6ARCJAiIGCIICENgCIgYIgwIQ2AMiBgj7ARD/ASIGCN8BEOACIgYI5gEQgQIiBgjoARDnASIGCO0BENgBIgYIhwIQ2AQiBgjzARDoASIGCPQBEIcDIgYI3AEQwgIiBgjVARC3AyIGCPEBEJkDIgYIjQIQ4QQiBgj/ARCXAiIGCOMBEOcBIgYI9gEQxwQiBgj+ARDqAiIGCPUBEIcCIgYI7AEQ3AMiBgjpARCNAiIGCNMBELkCIgYI4QEQ1wMiBgjUARCHAyIGCIUCEIgFIgYIjAIQqAIiBgiAAhD4AiIGCPcBEIgCIgYI7wEQuAIiBgj4ARD4AiIGCIECEIoCIgYI8gEQ/wEiBgjbARCgAiIGCNkBELkDIgYI2gEQtgUiBgjXARDoBSIGCNgBENgCIgYI4AEQ7wMiBgjrARCDAyIGCOcBEJ4CIgYI4gEQkAoiBgjOARCgCCIGCMsBELADIgYIzAEQwAMiBgi1ARDIAyIGCLYBEJgJIgYIpwEQ6AMiBgioARCgCCIGCJYBELgGIgYIugEQiQciBgiuARC3BiIGCLkBEIMCIgYIwwEQjwMiBgjKARCGAiIGCKYBEKgCIgYIuAEQ6QIiBgi7ARC3AyIGCK8BEPgDIgYIpQEQwAIiBgjHARChAiIGCMQBEKgCIgYI0gEQnwMiBgjPARC4AyIGCLwBEKkCIgYIswEQ/gIiBgjBARDhAiIGCJ8BEK8CIgYItAEQiwMiBgigARDmAyIGCMABENAEIgYInQEQ+QMiBgieARDfAiIGCM0BENEEIgYIxgEQpwMiBgjJARCIAiIGCKMBEIgCIgYIwgEQgAMiBgi/ARCoAyIGCMgBEM8CIgYIxQEQmQIiBgjRARCaAiIGCL0BELYCIgYIpAEQkAciBgixARCQAyIGCNABEMgGIgYIvgEQuAIiBgiyARDhByIGCKEBEJACIgYIogEQtwQiBgiwARD4DCIGCLcBEMgDIgYIrQEQyAYiBgiUARDnESIGCI4BEOkCIgYIlQEQ5wMiBgiIARDBBCIGCIcBEIgEIgUIehDoAyIFCGwQmAQiBQh5EIAEIgYIggEQlwQiBQhrELoDIgUIcxC2BCIFCGQQ0QIiBgiBARDYAiIFCGoQqQUiBgiPARCnAyIGCJABEPkCIgYIhAEQ3wQiBgiDARCYBiIFCHUQoQIiBgiSARD3ByIGCJEBELADIgYIhgEQvwQiBQh3EPgDIgUIZhChCSIGCKkBEJ8wIgYIlwEQ2QQiBgibARCPAyIGCJwBEOgDIgUIchDoByIFCGMQwQYiBgiNARCHBCIFCH8Q+B8iBQhxENgKIgYIkwEQiAMiBQhiEOgEIgYIhQEQyAUiBQhoELICIgUIXBD2RyIFCF0Q2AQiBQhKEPAEIgUISxC4BSIFCDQQiAQiBQg1EOAMIgUIUhCYBCIFCDwQqAQiBQhbENgDIgUIWhCIAyIFCFgQ+QEiBQhZEPABIgUIRxD/AyIFCEYQgAIiBQhFEKECIgUIRBCQByIFCEMQlwMiBQhCEPgCIgUIJxDoKCIFCCYQsikiBQglELYKIgYIrAEQ6CgiBQhQEOAJIgUISRChBCIFCEgQwAIiDwj9//////////8BEOKBBSIGCJoBENUsIgYIiQEQ2DwiBgiqARCfBSIGCKsBEIoFIgUIexC4CiIFCHQQlgQiBQhtELkFIgUIdhDwFyIGCIABENAJIgUIXhDQEiIFCC4QwEMiBQgfENgRIgUIVhDnBSIGCJgBEPpDIgYIigEQ9gciBgiZARCQBSIGCIwBELgHIgUIURCPaCIFCHwQoQciBQhlEIAIIgUIOxCZHCIFCC0Q1gciBQhAELEHIgYIbhCggAEiBQhTEIgEIgUIXxCwAyIFCEwQtwYiBQhNEIEqIgUIPRCoFCIFCFQQ6Q0iBQg5EPcFIgUIExD4BSIFCCkQsTQiBQgvEO4FIgUIHhDpBSIFCAgQmAQiBQgaEPcCIgUIPhDYTiIFCDAQ0AQiBQggEO8DIgUIERDAAyIFCAIQmQUiBQghENcDIgUIeBCxByIFCGkQuHIiBQg2ENoDIgUIZxC2BSIFCBIQ6GEiBQgUEMAHIgUIFxDwByIFCH4Qjw0iBQgyEJEhIgUICRDICCIGCIsBEJhVIgUIfRDZBCIFCHAQmBEiBQhhEPYGIgUIKBDoGiIFCBkQokMiBQhPEIcZIgUIbxCgMSIPCP///////////wEQw/oCIgUIYBC0YCIFCFUQyBsiBQhXENBKIgUIGBD5HSIFCD8Qhw4iBQgjEPgCIgUIThCwFCIFCDcQ6AMiBQhBEMAEIgUIMRCADCIFCCsQ8AMiBQgzEPgDIgUIJBDnEiIFCBwQyQMiBQgWEMAEIgUICxC4CSIFCDoQoAQiBQgFENcFIgUIBxDoFiIFCCIQsAQiBQgOEKgiIgUIEBCYAyIFCAoQ4AUiBQgBEJELIgUIOBCPDCIFCBUQoAYiBQgqENgPIgUIGxCBAiIFCCwQ8gUiBQgdEL4DIgUIDxC/AiIFCA0QigYiBQgMEN4eIgUIBhCJAyIFCAQQ0AMiBQgAENcCIgUIAxC6Aw=='

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
        

def execute():
    global winCount
    for i in range(0, executeTimes): 
        requests.get(getMapUrl, headers=headers)
        # 休眠60s, 否则无法更新记录成功
        time.sleep(60)
        result = requests.post(reportUrl, headers=headers, 
                                json={'rank_score': 1, 'rank_state': 1, 'rank_time': 15, 'rank_role': 1, 'skin': 1, 'MatchPlayInfo': matchPlayInfo})
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
    print('刷新通关次数(每次需要1分钟):', executeTimes)
    execute()
