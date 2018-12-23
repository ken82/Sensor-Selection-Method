#/usr/bin/python3
#_*_coding:utf-8_*_
#複数センサーの選択及び学習方式
import re
import cgi
import MeCab
import discriminator01
import discriminator02
#import discriminator03

# input text--------------------------------------------------------------------
print("<Sensor Selection & Learning Method>")
print("------------------------------------\nPlease input some text (e.g. \"東京都で震度5の地震が発生した.\").")
text = input()  # 入力を受け取る

print("\n----------<Result>----------")
def sensor_selection(text):
    t = None  # textの解析結果を入れるグローバル変数を定義しておく
    sensors = {"s1(eqSensor)":0, "s2(wtSensor)":0, "s3(unknownSnsor)":0, "Nothing":0}  # 最終的なセンサーの重み付けを行うためのセンサーID
# Filtering by Regular Expression (正規表現で伝聞形，推量形は除く)--------------------
# (本来この前処理はcalcシステムの方に実装すればいいもの．)
    pattern = re.compile(r'だろう|らしい|かもしれない|と思われる|だそうだ|とのこと')
    match = pattern.findall(text)
    if match:
        print("\nError.\nBecause of the form of this text, the system cannot assess credibility. ")
        exit()
# Morphological Analysis (日本語文章の名詞を抽出)
    def preprocessing(text):
        tagger = MeCab.Tagger()  # MeCabのインスタンス
        tagger.parse('')  # 一度空の文字列をparseしないとエラー
        text_node = tagger.parseToNode(text)  # 解析
        words = []  # 単語を格納するリスト．ここにtextの名詞が格納される．
        while text_node:
            word = text_node.surface.split(",")[0]  # surfaceは単語を取得
            pos = text_node.feature.split(",")[0]  # featureは品詞(PartsOfSpeech)を取得
            if pos == "名詞":  # 文章に名詞が含まれたら，その単語を取り出す
                words.append(word)
            text_node = text_node.next  # nextで全形態素に順次アクセス
        result = " ".join(words)  # 抜き出したキーワードを文字列に変換し，空白で繋げて格納
        return result
    t = preprocessing(text)
    print("Element: " + t + "\n")

# 判別器 1-----------------------------------------------------------------------
    with open('./data_set/R1_weight.dat', 'r') as f:  # 判別器の持つ重み(信頼性)の初期値の保存先
        global r1
        r_1 = f.read()
        r1 = float(r_1)  # r1は判別器の持つ重みの初期値(信頼値)
    d1, R1 = discriminator01.pattern_matching(t, r1)  # 判別器1のモジュール(discriminator01.pyで定義したpattern_matchingの関数を実行)
    print("Discriminator No.1: ", end="")
    print(d1)
    print("Reliability: ", end="")
    print(r1)
    print("Weight: ", end="")
    print(R1)
    #  ここは判別器に対する重み付けの時に必要になる処理
    d1_max = max(R1.values())  # d1判別器の中で最も重みのあるセンサーを取り出す
    d1_choice = [d1_max2 for d1_max2 in R1 if R1[d1_max2] == d1_max]  # d1判別器の中で最も重みのあるセンサーを全て取り出す

    # 判別器1がセンサーにつけた重みをセンサーリストにあるセンサーに足していく
    if R1["s1(eqSensor)"] != 0:  #もしd1の地震センサーの値が 0でなければ，
        sensors["s1(eqSensor)"] = sensors["s1(eqSensor)"] + R1["s1(eqSensor)"]  # その値を最終的なセンサーの値に足す
    if R1["s2(wtSensor)"] != 0:  # 同様に，もしd1の気象センサーの値が 0でなければ，
        sensors["s2(wtSensor)"] = sensors["s2(wtSensor)"] + R1["s2(wtSensor)"]  # その値を最終的なセンサーの値に足す，これを繰り返す．
    if R1["s3(unknownSnsor)"] != 0:
        sensors["s3(unknownSnsor)"] = sensors["s3(unknownSnsor)"] + R1["s3(unknownSnsor)"]
    if R1["Nothing"] != 0:
        sensors["Nothing"] = sensors["Nothing"] + R1["Nothing"]
    print("")

# 判別器 2-----------------------------------------------------------------------
    with open('./data_set/R2_weight.dat', 'r') as f:
        global r2
        r_2 = f.read()
        r2 = float(r_2)
    d2, R2 = discriminator02.thesaurus(t, r2)  # 判別器2のモジュール (シソーラスを用いたパターンマッチングの関数を実行)
    print("Discriminator No.2: ", end="")
    print(d2)
    print("Reliability: ", end="")
    print(r2)
    print("Weight: ", end="")
    print(R2)
    #  ここは判別器に対する重み付けの時に必要になる処理
    d2_max = max(R2.values())  # d1判別器の中で最も重みのあるセンサーを取り出す
    d2_choice = [d2_max2 for d2_max2 in R2 if R2[d2_max2] == d2_max]  # d1判別器の中で最も重みのあるセンサーを全て取り出す

    # 判別器2がセンサーにつけた重みをセンサーリストにあるセンサーに足していく(判別器1と同様)
    if R2["s1(eqSensor)"] != 0:
        sensors["s1(eqSensor)"] = sensors["s1(eqSensor)"] + R2["s1(eqSensor)"]
    if R2["s2(wtSensor)"] != 0:
        sensors["s2(wtSensor)"] = sensors["s2(wtSensor)"] + R2["s2(wtSensor)"]
    if R2["s3(unknownSnsor)"] != 0:
        sensors["s3(unknownSnsor)"] = sensors["s3(unknownSnsor)"] + R2["s3(unknownSnsor)"]
    if R2["Nothing"] != 0:
        sensors["Nothing"] = sensors["Nothing"] + R2["Nothing"]
    print("")

# 判別器 3-----------------------------------------------------------------------
    '''
    with open('./data_set/R3_weight.dat', 'r') as f:
        global r3
        r_3 = f.read()
        r3 = float(r_3)
    d3, R3 = discriminator02.thesaurus(t, r3)  # 判別器3のモジュール (機械学習を用いたパターンマッチング)
    print("Discriminator No.2: ", end="")
    print(d3)
    print("Weight: ", end="")
    print(R3)
    print("")
    '''

# 多数決による最終的なセンサーの選択--------------------------------------------------
    sensor = max(sensors.values())  # センサーの中で最も重みのあるものを取り出す
    final_sensorID = [max_sensor for max_sensor in sensors if sensors[max_sensor] == sensor]  # 最も重みのあるものと同じ値のものは全て取り出す
    print("", "", "")
    print("Final Weight of Sensors: ", end="")  # センサーには重みが足されているのでその中で重みがもっとも大きいものを選択する．
    print(sensors.items())

# 判別器に対する重み付け------------------------------------------------------------
    if d1_choice == final_sensorID:  # もし判別器の最後の選択が最終的に選ばれたセンサーIDと合致していたら
        r1 = r1 + d1_max  # 判別器がセンサーに割り振った値を，重みの初期値に足す(信頼回復)
        if r1 > 100:  # 上限を100にする(数値が100を超えたら100にする)
            r1 = 100.0
        r1_str = str(r1)  # 一度テキストにしないと書き込めない．
        with open('./data_set/R1_weight.dat', 'w') as f:  # 判別器の重み(信頼値)を保存する
            f.write(r1_str)  # 保存先ファイルへの書き込み完了
    elif d1_choice != final_sensorID:  # もし判別器の最後の選択が最終的に選ばれたセンサーIDと合致していなかったら
        r1 = r1 - d1_max  # 判別器がセンサーに割り振った値を，重みの初期値から引く(信頼減少)
        if r1 < 1:  # もし数値が 0より小さくなったら，0にする(下限を0にする)
            r1 = 1
        r1_str = str(r1)  # ファイルへ書き込む際は文字列型に変換する
        with open('./data_set/R1_weight.dat', 'w') as f:  # 判別器の重み(信頼値)を保存する
            f.write(r1_str)  # 保存先ファイルへの書き込み完了

    # 判別器2にも 1と同様の処理
    if d2_choice == final_sensorID:
        r2 = r2 + d2_max
        if r2 > 100:
            r2 = 100.0
        r2_str = str(r2)
        with open('./data_set/R2_weight.dat', 'w') as f:
            f.write(r2_str)
    elif d2_choice != final_sensorID:
        r2 = r2 - d2_max
        if r2 < 1:
            r2 = 1
        r2_str = str(r2)
        with open('./data_set/R2_weight.dat', 'w') as f:
            f.write(r2_str)
    return final_sensorID
func = sensor_selection(text)
print("")
print(func)
