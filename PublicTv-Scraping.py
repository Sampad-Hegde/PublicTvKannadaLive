import requests
import bs4
import json
import m3u8
import os
import vlc


session = requests.session()

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 "
}

startplaying = 0
counter = 0
firstsegmentnumber = 0

def init():
    try:
        os.remove('publictvlive.ts')
    except:
        print()
    webdata = session.get(url = 'https://publictv.in/live' , headers = head)
    soup = bs4.BeautifulSoup(webdata.text, 'html5lib')
    return soup.find("iframe").get('src') 



def fetch(mainurl): 
    startplaying = 0 
    counter= 0
    firstsegmentnumber = 0    
    print(mainurl)
    with open("publictvlive.ts",'wb+') as f:
        while(1):
            try: 
                webdata = session.get(url = mainurl,headers = head)
                soup = bs4.BeautifulSoup(webdata.text, 'html5lib')
                data = soup.findAll("script")
        
                url = json.loads(data[1].contents[0][27:-1])['metadata']['qualities']['auto'][0]['url']

                m3u8_main_data = m3u8.loads(session.get(url = url, headers = head).text)
                url = m3u8_main_data.data['playlists'][-1]['uri']       # change -1 to 0 for low quality stream in case your internet is slow

                    
                m3u8_main_data = m3u8.loads(session.get(url = url, headers = head).text)
                url = url[:url.rfind('/')+1]

                if counter == 0:
                    firstsegmentnumber = m3u8_main_data.data['media_sequence']

                if m3u8_main_data.data['media_sequence'] % 10 == firstsegmentnumber % 10:
                    for segment in m3u8_main_data.data['segments']:
                        f.write(session.get(url = url+segment['uri'], headers = head).content)
                    
                if startplaying == 1:
                    p = vlc.MediaPlayer('publictvlive.ts')
                    p.set_fullscreen(True)
                    p.play()
                    startplaying = 2

                if counter == 1:
                    startplaying = 1

                counter = counter + 1
            except:
                print("dailymotion Offline")


fetch(init())
