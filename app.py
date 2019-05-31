import os
from flask import Flask, redirect, render_template, request, session, g
import sqlite3

app = Flask(__name__)

# Initialized database connection
DATABASE = '~Documents/Snake/static/scores.db'
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

if __name__ == '__main__':
    app.run()


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
    return 1