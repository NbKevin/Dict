#!/usr/bin/env python
# -*- encoding:utf-8 -*-

__author__ = 'Nb'

import requests
import os, sys
import platform


class Dictionary():

    queryAddress = 'http://dict.youdao.com/search?le=eng&q='
    headerDict = {
        'Host': 'dict.youdao.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-tw,zh;q=0.8,en-us;q=0.5,en;q=0.3'
    }

    def __init__(self, argv):
        if len(argv) == 0:
            self.queryAddress = self.queryAddress + input('enter the word you want to query: ')
            self.translate()
        elif len(argv) == 1:
            self.queryAddress = self.queryAddress + argv[0]
            self.translate()
        else:
            print('Input argv error: can only accept one word')

    def translate(self):
        print('\n            Waiting for response...')
        response = requests.get(self.queryAddress, headers=self.headerDict).text

        #refresh console
        if platform.system().lower() == 'windows':
            os.system('cls')
        elif platform.system().lower() == 'linux':
            os.system('clear')

        #check response
        #no entry found
        if response.count('error-wrapper') > 0 and response.count('error-typo') == 0 :
            print('\n          抱歉，查無此詞')

        #no entry found but with suggestions
        elif response.count('error-wrapper') > 0 and response.count('error-typo') > 0 :
            #find suggestion container
            suggesContainer = response.split('<div class="error-typo">')[1].split('</div>')[0]

            #find all sugggestions
            suggesCount = suggesContainer.count('</a>')
            suggesList = []
            for i in range (1, suggesCount+1):
                suggestion = suggesContainer.split('</a>')[i-1].split('<a')[1].split('>')[1]
                suggesList.append(suggestion)

            #print results
            print('\n          抱歉，查無此詞')
            print('          您是不是想要查 %s' % suggesList[0])
            if len(suggesList) > 1:
                for i in range(1, len(suggesList)):
                    print('                         %s' % suggesList[i])

        #entry found
        else:
            #find result container
            transContainer = response.split('<div class="trans-container">')[1].split('</div>')[0]

            #find all results
            expCount = transContainer.count('</li>')
            transList = []
            for i in range(1, expCount+1):
                explanation = transContainer.split('<li>')[i].split('</li>')[0]
                transList.append(explanation)

            #print results
            print('\n      Input: %s' % self.queryAddress.split('q=')[1])
            print('Explanation: %s' % transList[0])
            if len(transList) > 1:
                for i in range(1, len(transList)):
                    print('             %s' % transList[i])

if __name__ == '__main__':
    Dictionary(sys.argv[1:])
else:
    query = input('Entre input: ')
    Dictionary([query])