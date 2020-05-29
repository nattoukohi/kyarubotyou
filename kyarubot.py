import discord # インストールした discord.py
import random
import time
import re
from datetime import datetime
import mysql.connector

import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http


client = discord.Client() # 接続に使用するオブジェクト



soubi = [
"白銀の大翼弓",
"ネクロディムアックス",
"ムーンセスタス",
"ファンタズムメイル",
"忘哭の冠",
"星詠みの円盾",
"蒼輝の鎧",
"イージスコート",
"純潔の巫女装束",
"天開の聖剣",
"ラヴァエッジ",
"ゲイルスティンガー",
"神花の聖杖",
"白祈の聖冠",
"インファナルグリーブ",
"九天の鎧",
"エンプレスローブ",
"メイデンクロース",
"聖櫻の鎧",
"エンジェルアーマー",
"月華杖",
"雷光弓",
"プレシャスナイフ",
"フェザーワルツ",
"緋竜槍",
"パラディングリーブ",
"エンプレスシールド",
"火焔のガントレット",
"ウィザードフード",
"光輝の剣",
"ヘルファイアアックス",
"ハーミットクロース",
"法王のフード",
"聖者のローブ",
"バーミリオンメイル",
"ミスリルプレート",
"エンジェルブーツ",
"ストームブリンガー",
"フェニックスロッド",
"ブリザードクロー",
"バイオレットアーマー",
"ネクロマンサーブーツ",
"蒼天のローブ",
"クルセイダープレート",
"ガーディアンシールド",
"福音のティアラ",
"ユニコーンナイフ",
"ハイデビルズワンド",
"鳳凰刀",
"スカーレットメイル",
"フェアリアルブーツ",
"翠緑の霊衣",
"アクエリアスブーツ",
"ダークテラードレス",
"ドラゴニックアーマー"
]


clist = [
"アンナ",
"マホ",
"リノ",
"ハツネ",
"カスミ",
"イオ",
"サレン",
"ノゾミ",
"ニノン",
"アキノ",
"キョウカ",
"トモ",
"マコト",
"イリヤ",
"ジュン",
"シズル",
"モニカ",
"ルカ",
"ジータ",
"ムイミ",
"アリサ",
"クリスティーナ",
"アン",
"ペコリーヌ（サマー）",
"スズメ（サマー）",
"キャル（サマー）",
"タマキ（サマー）",
"シノブ（ハロウィン）",
"ミサキ（ハロウィン）",
"チカ（クリスマス）",
"アヤネ（クリスマス）",
"ヒヨリ（ニューイヤー）",
"ユイ（ニューイヤー）",
"シズル（バレンタイン）",
"マツリ",
"アカリ",
"ミヤコ",
"ユキ",
"ナナカ",
"ミサト",
"スズナ",
"カオリ",
"ミミ",
"アヤネ",
"リン",
"エリコ",
"シノブ",
"マヒル",
"シオリ",
"チカ",
"クウカ",
"タマキ",
"ミフユ",
"ミツキ",
"ツムギ",
"ヒヨリ",
"ユイ",
"レイ",
"ミソギ",
"クルミ",
"ヨリ",
"スズメ",
"ユカリ",
"アオイ",
"ミサキ",
"リマ",
"ペコリーヌ",
"コッコロ",
"キャル",
"ルゥ",
"コッコロ（サマー）",
"ミフユ（サマー）",
"ミヤコ（ハロウィン）",
"クルミ（クリスマス）",
"レイ（ニューイヤー）"
]


# 起動時に通知してくれる処理
@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message):
    if client.user != message.author:
            global replymessage2
            channel = client.get_channel('')
            
            div3 = re.match(r"[^\x01-\x7E]*",message.content)
            div4 = re.search(r"[ -~｡-ﾟ]+",message.content)

            if(div3):
                char = div3.group()
            else:
                char = "ないよ"

            replymessage = ""
            c = ""
            if char in clist:
                if(div4):
                    num = div4.group()
                    reply = test_mysql(char,num)
                    replymessage = reply[0] +"\n"
                    replymessage += "Rank" + reply[1] + "の必要装備\n"

                    for i in range(2,8):
                        a = search_weapon(reply[i])
                        replymessage += "【" + reply[i] + "】 " +  " ".join(a) +"\n"
                        
                        #print(a)
                        
                        c =circulate(reply[i])

                    replymessage += "\n他に必要な素材\n"
                        

                    
                else:
                    reply = ""
            else:
                reply = ""



            if not reply:
                reply = ""
            if not replymessage:
                replymessage = ""
        
            
            replymessage2 = ""
            

            #time.sleep(0.5)
            #for mes in reply:
            #    if not mes:
            #        continue
            await message.channel.send(replymessage + c)
        

@client.event
async def dontcrash():
    channels = client.get_all_channels()
    asyncio.sleep(50)

replymessage2 = ""
def circulate(wepname):
    global replymessage2
    if wepname in soubi:
        #print(wepname+"装備あるよ")
        b = weapon_material(wepname)
        #print(b)
        for name in b:
            c = search_weapon(name)
            #print(name + " "+ " ".join(c))
            replymessage2 += "【" + name + "】 " +  " ".join(c) +"\n"

            circulate(name)
    else:
        return replymessage2


 
def test_mysql(charname,num):
    # ホスト名等入力
    conn = mysql.connector.connect(host='', 
                                  port=, 
                                  db='', 
                                  user='', 
                                  passwd='', 
                                  charset="utf8")
 
    cur = conn.cursor(buffered=True)
    
    #SQL
    sql = "select * from `TABLE 1` WHERE Name='"+ charname + "' AND Rank=" + num
    # 実行
    cur.execute(sql)
    # データ取得
    rows = cur.fetchall()


 
    for row in rows:
       print (row)
       return row

    conn.commit()
 
    # 接続を閉じる
    cur.close()
    conn.close()


def search_weapon(weponname):
    # ホスト名等入力
    conn = mysql.connector.connect(host='', 
                                  port=, 
                                  db='', 
                                  user='', 
                                  passwd='', 
                                  charset="utf8")
 
    cur = conn.cursor(buffered=True)
    
    #SQL
    sql = "select * from `TABLE 3` WHERE (CONCAT(w1,w2,w3,w4,w5,w6,w7,w8) LIKE '%" + weponname +"%')"
    # 実行
    cur.execute(sql)
    # データ取得
    rows = cur.fetchall()


    result = []

    for row in rows:
        if(weponname in row[2])or(weponname in row[4]):
            result.append("**"+ row[0] + "**")
        else:
            result.append(row[0])
       
    return result

    conn.commit()
 
    # 接続を閉じる
    cur.close()
    conn.close()

def weapon_material(weponname):
    # ホスト名等入力
    conn = mysql.connector.connect(host='', 
                                  port=, 
                                  db='', 
                                  user='', 
                                  passwd='', 
                                  charset="utf8")
 
    cur = conn.cursor(buffered=True)
    
    #SQL
    sql = "select * from `TABLE 4` WHERE wep = '" + weponname +"'"
    # 実行
    cur.execute(sql)
    # データ取得
    rows = cur.fetchall()


    result = []

    for row in rows:
        result.append(row[2])

        if row[1] == "2":
            result.append(row[3])

        if row[1] == "3":
            result.append(row[4])
       
    return result

    conn.commit()
 
    # 接続を閉じる
    cur.close()
    conn.close()

# botの接続と起動
# （tokenにはbotアカウントのアクセストークンを入れてください）
client.run('')
client.loop.create_task(dontcrash())

 
    
 
