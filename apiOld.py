from flask import Flask, request, render_template
from flask_cors import CORS
import sqlite3



app = Flask(__name__)
CORS(app)


@app.route("/get")
def get():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("select * from data")
    data = c.fetchall()
    return "<br>".join([i[0] for i in data])


@app.route("/register")
def register():
    name = request.args.get('name')
    password = request.args.get('password')
    secret = request.args.get('secret')


    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    try:
        statement = "INSERT INTO user1 (name,password,secret) VALUES ('{}','{}','{}')".format(name,password,secret)

        ##c.execute("INSERT INTO user1 (name,password,secret) VALUES (?,?,?)",(name,password,secret))
        c.execute(statement)
        conn.commit()

        return f"Successfully added {name}'s secret"
    except sqlite3.Error as e:
        return str(e)


@app.route("/search")
def search():
    name = request.args.get('name')
    password = request.args.get('password')
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    try:
        statement = "select secret from user1 where name='{}' AND password='{}'".format(name,password)


        c.execute(statement)

        found = c.fetchall()
        if found == []:
            return f"No Access<br>{statement}"
        else:
            return f"Access granted<br> YOUR SECRET IS {found[0][0]}"
    except sqlite3.Error as e:
        return str(e) + f"<br>{statement}"




if __name__ == "__main__":
    app.run(host="0.0.0.0")
