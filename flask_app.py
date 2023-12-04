from flask import Flask, render_template, request, redirect,g
import os
import json
import sqlite3
import socket

app = Flask(__name__)
DATABASE='ans_data.db'

@app.route('/')
def index():
    return "<h1>Oops!</h1><h3>There doesn't seem to be anything here.</h3>"

@app.route('/appreciate')
def thanks():
    return render_template('appreciate.html')

@app.route('/questionnaire/<path:path>')
def app_ctr(path):
    #pathを/で分割
    path_list = path.split('/')
    path_list_len = len(path_list)

    #要素数が2つ以下かを確認
    if path_list_len > 2:
        return redirect('/')
    json_path=f"./json/{path_list[0]}.json"
    
    #jsonをtextで読み込む
    with open(json_path, 'r',encoding="utf-8") as f:
        json_txt=f.read()
    
    if path_list_len==1 or path_list[1]=='':
        return render_template('app_home.html', json_txt=json_txt)
    
    if path_list_len==2:
        
        #path_list[1]が数字ではなかったらエラー
        if path_list[1]=="send":
            return render_template('app_send.html', json_txt=json_txt)
        if not path_list[1].isdigit():
            return redirect('/')
        return render_template('app_questionnaire.html', json_txt=json_txt, q_num=path_list[1])
    return render_template('index.html')


@app.route('/api/send/<title>', methods=['POST'])
def api_send(title):

    json_data=request.json
    #jsonを改行のない文字列に変換
    json_str=json.dumps(json_data, ensure_ascii=False)
    #jsonをsqliteに保存
    conn = get_db()
    c = conn.cursor()
    #ans_dataテーブルにはtitle,name,ansを保存
    try:
        c.execute("REPLACE INTO ans_data VALUES (?,?,?)", (title, json_data['name'], json_str))
        conn.commit()
    except:
        conn.close()
        return {"status": "ng"}
    conn.close()
    return {"status": "ok"}



#エラーページ
@app.errorhandler(404)
def error_404(error):
    return "<h1>Oops!</h1> <h3>There doesn't seem to be anything here.</h3>", 404

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

if __name__ == '__main__':
    app.run(debug=True,host=socket.gethostbyname(socket.gethostname()),port=80)