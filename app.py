import os
from flask import Flask, redirect, url_for, render_template, request, session, g
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialized database connection
DATABASE = '/home/thomas/www/snake/venv/SnakeGame/scores.db'
# Table created with: CREATE TABLE records (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, score INTEGER NOT NULL, name TEXT NOT NULL, time TEXT NOT NULL);
conn = sqlite3.connect(DATABASE)
db = conn.cursor()

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

        # TODO: Collect data from the database to show the high score chart
        data = db.execute("SELECT * FROM records ORDER BY score DESC LIMIT 10").fetchall()

        return render_template("highscores.html", data = data, score = score)


@app.route('/recordscore', methods=['POST', 'GET'])
def recordscore():
    """ Records the within the database. """

    if request.method == "GET":
        return redirect("index")
    
    if request.method == "POST":
        
        info = {
            "score" : request.form.get("score"),
            "name" : str(request.form.get("initials")),
            "time" : str(datetime.now())
        }

        db.execute("INSERT INTO records (score, name, time) VALUES (:score, :name, :time)", info)
        conn.commit()
        
    return redirect(url_for("index"))




if __name__ == '__main__':
    app.run()