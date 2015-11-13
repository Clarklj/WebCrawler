import urllib.request
import re
from bs4 import BeautifulSoup as bs
import jieba
import sys


class WebCrawler(object):
    def __init__(self, base_url):
        self.encode_mode = ['gbk', 'gb18030', 'utf-8']
        self.waiting_urls = [base_url]
        self.content = {}
        f = urllib.request.urlopen(self.waiting_urls[0])
        content = f.read()
        soup = bs(content, 'html.parser', from_encoding='gbk')
        news_list = soup.findAll('li')
        if news_list != None:
            for j in news_list:
                for k in j.findAll('a'):
                    p = re.compile(r'\w+://(\w+\.)+\w+(/\w*)+(\.\w)*')
                    if k.text not in self.content and p.match(k['href']):
                        self.waiting_urls.append(k['href'])
                        self.content[k.text] = []
        del self.waiting_urls[0]
        self.countTopWords(self.content.keys())
        print(self.waiting_urls[0])
        self.resolveWebPage(self.waiting_urls[0])

    def BreadthSearch(self):
        pass
        
    def countTopWords(self, sentence_set):
        words = {}
        for i in sentence_set:
            s = jieba.cut(i)
            for j in s:
                if j not in words:
                    words[j] = 1
                else:
                    words[j] += 1
        topwords = sorted(words.items(), key=lambda asd:asd[1], reverse=True)
        count = 0
        for i in topwords:
            p = re.compile(r'\w+')
            m = p.match(i[0])
            if m and len(i[0]) > 1 and count < 21:
                count += 1
                print(m.group(), i[1])

    def resolveWebPage(self, url, encoding='gbk'):
        f = urllib.request.urlopen(url)
        content = f.read()
        soup = bs(content, 'html.parser', from_encoding=encoding)
        text = soup.findAll('div', {'class', 'TRS_Editor'})
        if text != []:
            res = text[0].findAll('p')
            sentence_set = []
            for i in text:
                sentence_set.append(i.text)
            self.countTopWords(sentence_set)
        del self.waiting_urls[0]
        print(self.waiting_urls[0])
        self.resolveWebPage(self.waiting_urls[0])

if __name__ == '__main__':
    x = WebCrawler('http://news.baidu.com/')
