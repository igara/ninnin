# -*- coding: utf-8 -*-
#Import Libraries
import time
import hashlib
import urllib
import os
import sys
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


########### 設定パラメータ ###########
# arg = sys.argv
# if len(arg) == 1:
#     print("検索したいワードがありません")
#     sys.exit()

#検索ワード
# word = arg[1]
word = 'ピカチュウ'
#ダウンロード数
imageNum = 200 #最大値100
USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
########### End ###########


#ダウンロード
def download_page(url):
    import urllib.request
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        print(str(e))


#検索
def _images_get_next_item(s):
    start_line = s.find('thumbnail_src')
    if start_line == -1:
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_content = s.find('"thumbnail_src": "')
        end_content = s.find('", "', start_content+1)
        content_raw = str(s[start_content+18:end_content])
        return content_raw, end_content


#リンク取得
def _images_get_all_items(URL):
    HTML = (download_page(URL))
    time.sleep(0.05)
    _items = []
    start_end_cursor = HTML.find('"end_cursor": "')
    end_end_cursor = HTML.find('"}}, "top_posts"')
    end_cursor = str(HTML[start_end_cursor+15:end_end_cursor])
    while True:
        item, end_content = _images_get_next_item(HTML)
        if item == "no_links":
            NEXT_URL = '{}&max_id={}'.format(URL, end_cursor)
            break
        else:
            _items.append(item)
            time.sleep(0.05)
            HTML = HTML[end_content:]
    while True:
        HTML = (download_page(NEXT_URL))
        time.sleep(0.05)
        start_end_cursor = HTML.find('"end_cursor": "')
        end_end_cursor = HTML.find('"}}, "top_posts"')
        end_cursor = str(HTML[start_end_cursor+15:end_end_cursor])
        while True:
            item, end_content = _images_get_next_item(HTML)
            if item == "no_links":
                NEXT_URL = '{}&max_id={}'.format(URL, end_cursor)
                break
            else:
                _items.append(item)
                time.sleep(0.05)
                HTML = HTML[end_content:]
        if len(_items) >= imageNum:
            break
    return _items


############## Main Program ############
T0 = time.time()   #開始時間

#画像リンク取得
temp = word
items = []

search = temp.replace(" ", "%20")

print("検索ワード:" + search)
URL = 'https://www.instagram.com/explore/tags/' + search + '/?__a=1'
p = urlparse(URL)
path = urllib.parse.quote_plus(p.path, safe='/')
URL = '{}://{}{}{}{}{}{}{}{}'.format(p.scheme, p.netloc, path,';' if p.params else '', p.params,'?' if p.query else '', p.query,'#' if p.fragment else '', p.fragment)

items.extend(_images_get_all_items(URL))

print("ダウンロード開始")

errorCount = 0
Cnt = 0
folderName = os.getcwd() + '/images/instagram_' + word
if os.path.exists(folderName)==False:
    os.mkdir(folderName)
for item in items:
    if Cnt == imageNum:
        break
    try:
        outputPath = folderName + '/' + hashlib.md5(item.encode('utf-8')).hexdigest() + ".jpg"
        print('-------------------------------------------------------------------')
        if os.path.isfile(outputPath):
            print(outputPath + " ダウンロード済み画像のためスキップ")
        else:
            REQ = urllib.request.Request(item, headers={"User-Agent": USER_AGENT})
            RESPONSE = urlopen(REQ)
            DATA = RESPONSE.read()
            open(outputPath, 'wb').write(DATA)
            RESPONSE.close()
            pass

        print("ダウンロード完了 ====> "+str(item))

    except IOError:
        errorCount += 1
        Cnt -= 1
        print("IOError"+str(item))
    except HTTPError as e:
        errorCount += 1
        Cnt -= 1
        print("HTTPError"+str(item))
    except URLError as e:
        errorCount += 1
        Cnt -= 1
        print("URLError "+str(item))
    except UnicodeEncodeError as e:
        errorCount += 1
        Cnt -= 1
        print("UnicodeEncodeError "+str(item))
    print('-------------------------------------------------------------------')
    Cnt += 1

print("\n")
print("ダウンロード完了")
print("\n"+str(errorCount)+" ----> 合計エラー数")

