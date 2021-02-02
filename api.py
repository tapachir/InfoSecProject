from flask import Flask, request, render_template
from flask_cors import CORS
import sqlite3
from Cryptodome.Cipher import AES



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

    ## This is for preparing the encryption
    ## we need to convert the password to a key and make the size a multiply of 16bytes
    passwordBytes = password.encode("utf8")
    length = 16 - (len(passwordBytes) % 16)
    passwordBytes += bytes([length])*length


    obj = AES.new(passwordBytes, AES.MODE_CFB, 'This is an IV456'.encode("utf8"))
    message = secret.encode("utf8")
    secretEncrypted = obj.encrypt(message)
    ##return f"Successfully added {secretEncrypted}'s secret"
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    try:
        ##statement = "INSERT INTO user2 (id,name,secret) VALUES (1,'{}','{}')".format(name,secretEncrypted)

        c.execute("INSERT INTO user2 (id,name,secret) VALUES (1,?,?)",(name,secretEncrypted))
        ##c.execute(statement)
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

    passwordBytes = password.encode("utf8")
    length = 16 - (len(passwordBytes) % 16)
    passwordBytes += bytes([length])*length

    obj2 = AES.new(passwordBytes, AES.MODE_CFB, 'This is an IV456'.encode("utf8"))

    try:
        ##statement = "select secret from user2 where name='{}'".format(name,password)

        ##statement = "PRAGMA table_info('user1')"
        c.execute("select secret from user2 where name=?", (name,))
        #c.execute(statement)

        found = c.fetchall()
        if found == []:
            return f"No secret saved<br>{password}"
        else:
            try:
                decryptedSecret = (obj2.decrypt(found[0][0])).decode("utf8")

                return f"Access granted<br> YOUR SECRET IS {decryptedSecret}"
            except:
                return f"Wrong password<br>  {password}"

    except sqlite3.Error as e:
        return str(e) + f"<br>{password}"


@app.route("/login")
def login():
    return open("login.html").read()


@app.route("/")
def main():
    return open("403.html").read()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
