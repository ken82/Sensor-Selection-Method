#/usr/bin/python3
#_*_coding:utf-8_*_
# 正規表現によるパターンマッチングを用いたセンサーへの重み付け
import re
import csv
import difflib

# sensor_selection.pyから読み込むモジュール
#t = input()
#r1 = 100.0
def pattern_matching(t, r1):
    sensorID = {"s1(eqSensor)":0, "s2(wtSensor)":0, "s3(unknownSnsor)":0, "Nothing":0}  # センサーIDとその重み
    #sensor_weight = {"s1(eqSensor)":0, "s2(wtSensor)":0}  # 類似度を使うときの辞書
    result = []  # パターンマッチングの結果を格納するリスト
    sid = []  # 結果から選んだセンサーのIDを格納するリスト
    r1_a, r1_b = r1 / 2, r1 /2  # センサーの数に応じて重みを分ける
# キーワード(csvファイル)の読み込みと加工，パターンマッチング. --------------------------
# データの流れ(変数名の遷移)に注意．
    with open('./data_set/keyword.csv') as f:  # csv形式のdatasetを読み込む(共通キーワード)
        reader = csv.reader(f)
        for keyword in reader: pass  # リストに格納
        keyword2 = '|'.join(keyword) # 正規表現で使える形式にする
        keyword_compile = re.compile(keyword2)  # 正規表現型に変換
        match_keyword = keyword_compile.findall(t)  # 正規表現で,入力されたtext(t)とキーワードを比較
        # 類似度を用いる場合
        '''mk = str(match_keyword)  # 正規表現型から文字列に戻す
        mk2 = re.sub('[\\[\\]\']', '', mk)  # 余計な記号を削除
        mk_ratio = difflib.SequenceMatcher(None, t, mk2).ratio()  # 正規表現で比較した文字の一致度(類似度)を計算(値は0.0 ~ 1.0の実数)'''
    with open('./data_set/earthquake.csv') as f:  # 地震キーワード
        reader = csv.reader(f)
        for earthquake in reader: pass
        earthquake2 = '|'.join(earthquake)
        earthquake_compile = re.compile(earthquake2)
        match_earthquake = earthquake_compile.findall(t)
        # 類似度を用いる場合
        '''me = str(match_earthquake)
        me2 = re.sub('[\\[\\]\']', '', me)
        me_ratio = difflib.SequenceMatcher(None, t, me2).ratio()'''
    with open('./data_set/flood.csv') as f:  # 水害キーワード
        reader = csv.reader(f)
        for flood in reader: pass
        flood2 = '|'.join(flood)
        flood_compile = re.compile(flood2)
        match_flood = flood_compile.findall(t)
        # 類似度を用いる場合
        '''mf = str(match_flood)
        mf2 = re.sub('[\\[\\]\']', '', mf)
        mf_ratio = difflib.SequenceMatcher(None, t, mf2).ratio()'''

# キーワードに応じた重み付け--------------------------------------------------------
    if match_keyword or match_earthquake and match_flood:  # 共通
        sensorID["s1(eqSensor)"] = r1_a
        sensorID["s2(wtSensor)"] = r1_b
        r_d1 = [r1_a, r1_b]
    if match_earthquake and not match_flood:  # 地震
        sensorID["s1(eqSensor)"] = r1_a + r1_b
        r_d1 = r1_a + r1_b
    if match_flood and not match_earthquake:  # 水害
        sensorID["s2(wtSensor)"] = r1_a + r1_b
        r_d1 = r1_a + r1_b
    if not match_keyword and not match_earthquake and not match_flood:  # 該当なし
        sensorID["Nothing"] = r1_a + r1_b
        r_d1 = r1_a + r1_b

# 重みの大きいセンサーを選択--------------------------------------------------------
    max_sensor = max(sensorID.values())  # 辞書の中から最も大きいものを取り出す
    sid = [sensor for sensor in sensorID if sensorID[sensor] == max_sensor]  # さらに辞書の中で最も大きいものと同じ値のものを全て取り出す
    r1 = r_d1
    #return(sid, r1)
    return(sid, sensorID)
'''
# パターンマッチングの結果に応じてセンサーを変える
    if "all" in result and "eq" not in result and "wt" not in result:
        sid.append(sensorID[0])
        sid.append(sensorID[1])
    if "eq" in result:
        sid.append(sensorID[0])
    if "wt" in result:
        sid.append(sensorID[1])
    if "None" in result:
        sid.append(sensorID[3])
'''
'''
# 類似度を用いた場合の処理
    if match_keyword:  # 共通
        sensor_weight["s1(eqSensor)"] = mk_ratio / 2
        sensor_weight["s2(wtSensor)"] = mk_ratio / 2
        r1 = mk_ratio
    if match_earthquake:  # 地震
        sensor_weight["s1(eqSensor)"] = me_ratio
        r1 = me_ratio
    if match_flood:  # 水害
        sensor_weight["s2(wtSensor)"] = mf_ratio
        r1 = mf_ratio
    if not match_keyword and not match_earthquake and not match_flood:  # 該当なし
        sensor_weight["s1(eqSensor)"] = 0
        sensor_weight["s2(wtSensor)"] = 0
        r1 = 0
    sensor = max(sensor_weight.values())
    sid = [key for key in sensor_weight if sensor_weight[key] == sensor]
    return (sid, r1)
'''
#func = pattern_matching(t, r1)
#print("")
#print(func)
