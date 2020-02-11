import requests,sys
from bs4 import BeautifulSoup

class download(object):
    def __init__(self):
        self.target='http://www.196105.com/31/31851/'
        self.names=[]
        self.urls=[]
        self.nums=0

    def get_download_url(self):
        req=requests.get(url=self.target)
        req.encoding='GBK'
        html=req.text
        chapter_bf=BeautifulSoup(html,features="html.parser")
        chapter=chapter_bf.find_all('td',class_='ccss')
        name_bf=BeautifulSoup(str(chapter))
        name=name_bf.find_all('a')
        self.nums=len(name)
        for each in name:
            self.names.append(each.string)
            self.urls.append(self.target+each.get('href'))

    def get_context(self,target):
        req=requests.get(url=target)
        req.encoding='GBK'
        html=req.text
        bf=BeautifulSoup(html,features="html.parser")
        texts=bf.find_all('div',id='content')
        texts=texts[0].text.replace('更多原创耽美小说尽在耽美中文网http://www.blnovel.com。','\n\n')
        return texts

    def writer(self,name,path,text):
        write_flag=True
        with open(path,'a',encoding='utf-8') as f:
            f.write(name+'\n')
            f.writelines(text)
            f.write('\n\n')

if __name__=='__main__':
    dl=download()
    dl.get_download_url()
    print('start downloading')
    for i in range(dl.nums):
        dl.writer(dl.names[i],'novel',dl.get_context(dl.urls[i]))
        sys.stdout.write("downloaded:%.2f%%" % float(i/dl.nums)+'\r')
        sys.stdout.flush()
    print('download complete')