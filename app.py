import os
from flask import Flask, redirect, render_template, request, session, g
import sqlite3

app = Flask(__name__)

DATABASE = '~Documents/Snake/static/scores.db'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/gamepage', methods=['POST'])
def gamepage():
    return render_template("gamepage.html")