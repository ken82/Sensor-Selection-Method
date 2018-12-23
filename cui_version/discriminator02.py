#/usr/bin/python3
#_*_coding:utf-8_*_
# シソーラスを用いたセンサー選択
import re
import csv
import sys
import sqlite3
from pprint import pprint
from collections import namedtuple

# sensor_selection.pyから読み込むモジュール
#t = input()
#r = input()
#r2 = float(r)
def thesaurus(t, r2):
    sensorID = {"s1(eqSensor)":0, "s2(wtSensor)":0, "s3(unknownSnsor)":0, "Nothing":0}  # センサーIDとその重み
    result = []  # 結果を格納するためのリスト
    sid = []  # 結果から選んだセンサーのIDを格納するリスト
    r2_a, r2_b = r2 / 2, r2 / 2  # センサーの数に応じて重みを分ける
# 読み込んだ Wordnetシソーラス内の検索用の関数群----------------------------------------------------------------
    conn = sqlite3.connect("./data_set/wnjpn.db")  # wordnetのシソーラスを読み込む
    Word = namedtuple('Word', 'wordid lang lemma pron pos')  # namedtupleで属性付きタプルを作成
    def getWords(lemma):
        cur = conn.execute("select * from word where lemma=?", (lemma,))  # execute()メソッドでSQL文を実行
        return [Word(*row) for row in cur]
    Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')
    def getSenses(word):
        cur = conn.execute("select * from sense where wordid=?", (word.wordid,))
        return [Sense(*row) for row in cur]
    Synset = namedtuple('Synset', 'synset pos name src')
    def getSynset(synset):
        cur = conn.execute("select * from synset where synset=?", (synset,))
        return Synset(*cur.fetchone())
    def getWordsFromSynset(synset, lang):
        cur = conn.execute("select word.* from sense, word where synset=? and word.lang=? and sense.wordid = word.wordid;", (synset,lang))
        return [Word(*row) for row in cur]
    def getWordsFromSenses(sense, lang="jpn"):
        synonym = {}
        for s in sense:
            lemmas = []
            syns = getWordsFromSynset(s.synset, lang)
        for sy in syns:
            lemmas.append(sy.lemma)
            synonym[getSynset(s.synset).name] = lemmas
        return synonym
    def getSynonym (word):
        synonym = {}
        words = getWords(word)
        if words:
            for w in words:
                sense = getSenses(w)
                s = getWordsFromSenses(sense)
                synonym = dict(list(synonym.items()) + list(s.items()))
        return synonym

# 入力(t)された文字を元にシソーラスにかけ，類義語を抽出----------------------------------
    synonym = getSynonym(t)  # 入力されたテキストの類義語を取得
    synonym2 = list(synonym.values())  # 辞書型になっているのでリストに変換(キーは取得しない)
    #print(synonym2)
    # シソーラスに類義語があった場合は処理を行う
    if synonym2:
        synonym3 = list(synonym2[0])  # 二次元配列扱いなので一次元に変換
        synonym_processed = " ".join(synonym3)  # 空白でつなげて文字列に変換
    elif not synonym2:
        synonym_processed = t  # 類義語がない場合はシソーラスを用いないパターンマッチングになる

# その類義語でパターンマッチングを行う------------------------------------------------
    with open('./data_set/keyword.csv') as f:  # csv形式のdatasetを読み込む(共通キーワード)
        reader = csv.reader(f)
        for keyword in reader: pass  # リストに格納
        keyword2 = '|'.join(keyword) # 正規表現で使える形式にする
        keyword_compile = re.compile(keyword2)  # 正規表現型に変換
        match_keyword = keyword_compile.findall(synonym_processed)  # 正規表現で類義語とキーワードを比較
    with open('./data_set/earthquake.csv') as f:  # 地震キーワード
        reader = csv.reader(f)
        for earthquake in reader: pass
        earthquake2 = '|'.join(earthquake)
        earthquake_compile = re.compile(earthquake2)
        match_earthquake = earthquake_compile.findall(synonym_processed)
    with open('./data_set/flood.csv') as f:  # 水害キーワード
        reader = csv.reader(f)
        for flood in reader: pass
        flood2 = '|'.join(flood)
        flood_compile = re.compile(flood2)
        match_flood = flood_compile.findall(synonym_processed)

# パターンマッチングの結果による重み付け-----------------------------------------------
    if match_keyword or match_earthquake and match_flood:  # 共通
        sensorID["s1(eqSensor)"] = r2_a
        sensorID["s2(wtSensor)"] = r2_b
        r_d2 = [r2_a, r2_b]
    if match_earthquake and not match_flood:  # 地震
        sensorID["s1(eqSensor)"] = r2_a + r2_b
        r_d2 = r2_a + r2_b
    if match_flood and not match_earthquake:  # 水害
        sensorID["s2(wtSensor)"] = r2_a + r2_b
        r_d2 = r2_a + r2_b
    if not match_keyword and not match_earthquake and not match_flood:  # 該当なし
        sensorID["Nothing"] = r2_a + r2_b
        r_d2 = r2_a + r2_b

# 重みの大きいセンサーを選択--------------------------------------------------------
    max_sensor = max(sensorID.values())
    sid = [sensor for sensor in sensorID if sensorID[sensor] == max_sensor]  # 辞書の中から最も大きいものを取り出す
    r2 = r_d2
    #return(sid, r2)
    return(sid, sensorID)
#func = thesaurus(t, r2)
#print("")
#print(func)
