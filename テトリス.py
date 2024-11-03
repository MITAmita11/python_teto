#モジュールのインストール
import tkinter as tk        #GUIを作るために使用_名前をtkに短縮
import random       #ブロックをランダムに作成するために使用
from tkinter import messagebox      #GAME‗OVERのメッセージボックスを作成するために使用

#ミノ関係
SIZE = 30       #1ブロックのサイズを決定
moveX = 4       #ミノの発生場所_横
moveY = 0       #ミノの発生場所_縦
type = random.randint(0, 6)      #0～6のランダムの数値の代入_ミノの種類_7種類

timer = 800     #ミノの落ちるスピード決定
score = 0       #スコアの作成_初期だから0点

color = ["magenta", "blue", "cyan", "yellow", "orange", "red", "green", "black", "white"]       #ミノとフィールドと枠の色を決定

minoT = [-1, 0, 0, 0, 1, 0, 0, 1]      #T字ミノの作成
minoJ = [-1, 0, 0, 0, 1, 0, 1, 1]      #J字ミノの作成
minoI = [-1, 0, 0, 0, 1, 0, 2, 0]      #I字ミノの作成
minoO = [ 0, 0, 1, 0, 0, 1, 1, 1]      #O字ミノの作成
minoL = [-1, 0, 0, 0, 1, 0,-1, 1]      #L字ミノの作成
minoZ = [-1,-1, 0,-1, 0, 0, 1, 0]      #Z字ミノの作成
minoS = [ 0, 0, 1, 0, 0, 1,-1, 1]      #S字ミノの作成
mino = [minoT,minoJ,minoI,minoO,minoL,minoZ,minoS]      #7種類のミノを1つのリストにまとめる

#フィールドデータ
field = []      #フィールドリストを作成
for y in range(22):     #フィールド縦20マス+上下枠1マス　22回ループ
    sub = []
    for x in range(12):     #フィールド横10マス+左右枠1マス　12回ループ
        if x==0 or x==11 or y==21 :
            sub.append(8)
        else :
            sub.append(7)
    field.append(sub)

def drawmino1():       #ミノを表示させる関数の作成
    for i in range(4):      #4回繰り返す？？？？？？
        x = (mino[type][i*2]+moveX)*SIZE        #変数ⅹに20行目のミノリストから11行目を利用してランダムに1つを取り出して？？？？？
        y = (mino[type][i*2+1]+moveY)*SIZE      #28行目と同じ
        can. create_rectangle(x, y, x+SIZE, y+SIZE, fill=color[type])      #Tkiterの機能で四角形を作成‗28、29行目の数値と21行目のカラーでミノを作成

def drawField():        #フィールドを表示させる関数の作成
    for i in range(21):
        for j in range(12):
            outLine=0 if color[field[i+1][j]]=="white" else 1   #白いブロックは枠無しで表示
            can.create_rectangle(j*SIZE, i*SIZE, (j+1)*SIZE, (i+1)*SIZE, fill=color[field[i+1][j]], width=outLine)


def keyPress(event):        #ミノを動かす関数の作成
    global moveX, moveY
    afterX = moveX
    afterY = moveY
    afterMino = []
    afterMino.extend(mino[type])
    if event.keysym=="Right" :      #右移動
        afterX += 1
    elif event.keysym=="Left" :     #左移動
        afterX -= 1
    elif event.keysym=="Down" :     #下移動
        afterY += 1
    elif event.keysym=="space" :    #右回転
        afterMino.clear()
        for i in range(4):
            afterMino.append(mino[type][i*2+1]*(-1))
            afterMino.append(mino[type][i*2])
    judge(afterX, afterY, afterMino)      #あたり判定関数の呼び出し


def judge(afterX, afterY, afterMino):     #あたり判定をする関数の作成
    global moveX, moveY
    result = True
    for i in range(4):
        x = afterMino[i*2]+afterX
        y = afterMino[i*2+1]+afterY
        if field[y+1][x]!=7 :
            result = False
    if result==True :
        moveX = afterX
        moveY = afterY
        mino[type].clear()
        mino[type].extend(afterMino)
    return result


def dropMino():
    global moveX, moveY, type, timer
    afterMino = []
    afterMino.extend(mino[type])
    result = judge(moveX, moveY+1, afterMino)
    if result==False :
        for i in range(4):
            x = mino[type][i*2]+moveX
            y = mino[type][i*2+1]+moveY
            field[y+1][x] = type
        deleteLine()
        type = random.randint(0, 6)
        moveX = 4
        moveY = 0
    can.after(timer,dropMino)
    timer -= 2      #落下速度をコントロール？
    if timer<140 :
        timer = 180

##########
def deleteLine():
    global score
    for i in range(1, 21):
        if 7 not in field[i]:
            for j in range(i):
                for k in range(12):
                    field[i-j][k] = field[i-j-1][k]
            score += 800-timer
    for i in range(1, 11):
        if 7 != field[1][i]:
            messagebox.showinfo("information", "GAME OVER !")
            exit()

#######################ゲームをループさせる#########################################
win = tk.Tk()
win.geometry("340x630")
win.title("Rough TETRIS")
can = tk.Canvas(win, width=12*SIZE, height=21*SIZE)
can.place(x=-10, y=0)
var = tk.StringVar()
lab = tk.Label(win, textvariable=var, fg="blue", bg="white", font=("", "20"))   #得点表示
lab.place(x=50, y=600)

win.bind("<Any-KeyPress>", keyPress)    #キープレスをバインド

def gameLoop():
    can.delete("all")
    var.set(score)
    drawField()
    drawmino1()
    can.after(50, gameLoop)

gameLoop()
dropMino()

win.mainloop()



