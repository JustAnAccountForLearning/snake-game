import os
from flask import Flask, redirect, url_for, render_template, request, session, g
import mysql.connector
from datetime import datetime
from helpers import formatname

# Configure Flask
application = Flask(__name__)
application.secret_key = 'bBX18z8wcJZq9YeUIBGd1CZTia7UDi27' # Randomly generated key

# Ensure templates are auto-reloaded
application.config["TEMPLATES_AUTO_RELOAD"] = True

# Initialized database connection
connection = mysql.connector.connect(host="mydbinstance.czwmx6aikpma.us-east-2.rds.amazonaws.com", user="JustAnAccount", passwd="iW4nGwkfQWHkW6X", database="simpledatabase")
db = connection.cursor()


@application.route('/')
@application.route('/index')
def index():
    """ Home page that allows game start selection. """

    return render_template("index.html")



@application.route('/gamepage', methods=['POST','GET'])
def gamepage():
    """ Page for Snake game display and play. """

    if request.method == "GET":
        return redirect("index")
    return render_template("gamepage.html")



@application.route('/highscores', methods=['POST', 'GET'])
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


@application.route('/recordscore', methods=['POST', 'GET'])
def recordscore():
    """ Records the within the database. """

    if request.method == "GET":
        return redirect("index")
    
    if request.method == "POST":

        # Sanitize and format the incomming initials.
        name = formatname(request.form.get("initials"))
        
        info = (
            request.form.get("score"),
            name,
            str(datetime.now())
        )

        db.execute("INSERT INTO records (score, name, time) VALUES (%s, %s, %s)", info)
        connection.commit()
        
    return redirect(url_for("index"))




if __name__ == '__main__':
    application.debug = True
    application.run()