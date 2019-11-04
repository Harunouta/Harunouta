#-*- coding:utf-8 -*-
import sys
import socket
import subprocess
import time
from datetime import datetime

def jtalk(t):
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(t.encode("utf-8"))
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    wr = subprocess.Popen(aplay)


def say_greetings(greeting):
    if greeting=='おはよう':
        text = '今日も頑張りましょう'
    if greeting=='こんにちわ':
        text = 'お昼ご飯は食べられましたか？'
    if greeting=='こんばんわ':
        text = 'お仕事お疲れ様です'
    if greeting=='おやすみ':
        text = 'いい夢見られるといいですね'
    if greeting=="終了":
        text = 'ご静聴、ありがとうございました'
    jtalk(text)
    print(text)

def say_daytime(day):
    d = dateline.now()
    if day=="今何時":
       text = '%s時%s分です' % (d.hour, d.minute)
    if day=="きょうは何日":
       text = '今日は%s月%s日です' % (d.month, d.day)
    jtalk(text)
    print(text)

def word(recv_data):
    for line in recv_data.split('\n'):
        index1 = line.find('WORD="')
        index2 = line.find('CM="')
        if index1!=-1:
            WORD = line[index1+6:line.find('"',index1+6)]
            if index2!=-1:
                CM = float(line[index2+4:line.find('"',index2+4)])
                if(WORD!='[s]' and WORD!='[/s]'):
                    if WORD == 'おはよう' and CM >= 0.97:
                        print(WORD)
                        print(CM)
                        say_greetings("おはよう")
                        time.sleep(1)
                    elif WORD == 'こんにちわ' and CM >= 0.97:
                        print(WORD)
                        print(CM)
                        say_greetings("こんにちわ")
                        time.sleep(1)
                    elif WORD == 'こんばんわ' and CM >= 0.97:
                        print(WORD)
                        print(CM)
                        say_greetings("こんばんわ")
                        time.sleep(1)
                    elif WORD == 'おやすみ' and CM >= 0.97:
                        print(WORD)
                        print(CM)
                        say_greetings("おやすみ")
                        time.sleep(1)
                    elif WORD == '終了' and CM >= 0.97:
                        print(WORD)
                        print(CM)
                        say_greetings("終了")
                        time.sleep(1)
                    elif WORD == '今何時' and CM >= 0.97:
                        print(WORD)
                        print(CM)
                        say_daytime("今何時")
                        time.sleep(1)
                    elif WORD == 'きょうは何日' and CM >= 0.97:
                        print(WORD)
                        print(CM)
                        say_daytime("きょうは何日")
                        time.sleep(1)
                    yield WORD

#Julius_comming
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 10500))
try:
        data = ''
        while 1:
            if '\n.' in data:
                data = data[data.find(''):].replace('\n.', '')
                print(''.join(word(data)))
                data = ''
            else:
                data = data + client.recv(1024).decode('utf-8')
except KeyboardInterrupt:
       client.close()

