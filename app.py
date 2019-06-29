import os
from flask import Flask, redirect, url_for, render_template, request, session, g
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Initialized database connection
connection = mysql.connector.connect(host="mydbinstance.czwmx6aikpma.us-east-2.rds.amazonaws.com", user="JustAnAccount", passwd="iW4nGwkfQWHkW6X", database="simpledatabase")
db = connection.cursor()

application = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    """ Home page that allows game start selection. """

    return render_template("index.html")



@app.route('/gamepage', methods=['POST','GET'])
def gamepage():
    """ Page for Snake game display and play. """

    if request.method == "GET":
        return redirect("index")
    return render_template("gamepage.html")



@app.route('/highscores', methods=['POST', 'GET'])
def highscores():
    """ Allows the user to input their initials. """

    if request.method == "GET":
        return redirect(url_for("index"))

    if request.method == "POST":
        data = {}
        score = request.form.get("topscore")

        db.execute("SELECT * FROM records ORDER BY score DESC LIMIT 10")
        data = db.fetchall()

        return render_template("highscores.html", data = data, score = score)


@app.route('/recordscore', methods=['POST', 'GET'])
def recordscore():
    """ Records the within the database. """

    if request.method == "GET":
        return redirect("index")
    
    if request.method == "POST":

        # TODO: Sanitize and format the incomming data.
        
        info = (
            request.form.get("score"),
            str(request.form.get("initials")),
            str(datetime.now())
        )

        db.execute("INSERT INTO records (score, name, time) VALUES (%s, %s, %s)", info)
        connection.commit()
        
    return redirect(url_for("index"))




if __name__ == '__main__':
    application.debug = True
    application.run()