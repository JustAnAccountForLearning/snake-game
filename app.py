import os
from flask import Flask, redirect, render_template, request, session, g
import sqlite3

app = Flask(__name__)

# Initialized database connection
DATABASE = '/home/thomas/www/snake/venv/SnakeGame/scores.db'
conn = sqlite3.connect(DATABASE)
db = conn.cursor()

@app.route('/')
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
        return redirect("index")

    if request.method == "POST":
        data = request.form.get("topscore")
        
        # TODO: Collect score from the form input 

        return render_template("highscores.html", data = data)


@app.route('/recordscore', methods=['POST', 'GET'])
def recordscore(data):
    """ Records the within the database. """

    if request.method == "GET":
        return redirect("index")
    
    if request.method == "POST":
        if data is None:
            return 0
        
        # TODO: Collect the score. 
        # Add score to the database along with the timecode. 

        # Table created with: CREATE TABLE records (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, score INTEGER NOT NULL, name TEXT NOT NULL, time INTEGER NOT NULL);
    return 1




if __name__ == '__main__':
    app.run()