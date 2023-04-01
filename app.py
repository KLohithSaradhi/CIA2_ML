from flask import Flask, request, render_template
import mysql.connector
import os
from keras.models import load_model
import cv2
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

def prerequisite():
    global columns, model
    with open("columns.txt", "r") as f:
        columns = eval(f.read())
    
    columns.remove("price")
        
    import pickle
    
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    
    
def convert(data, columns):
    Input = [0 for i in range(len(columns))]
    for key in data:
        if type(data[key]) == str:
            colName = key + "_" + data[key]
            try:
                Input[columns.index(colName)] = 1
            except:
                pass
        else:
            colName = key
            Input[columns.index(colName)] = data[key]
    return Input

def toInches(x):
    return 0.0393701 * float(x)

def toPounds(x):
    return 2.20462 * float(x)

def toCubicInches(x):
    return 61.0237 * float(x)

def toMPG(x):
    return 2.352145 * float(x)


prerequisite()


@app.route('/')
def main():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    mydb = mysql.connector.connect(host = "localhost", 
                               user = "root", 
                               password = "hrao1272",
                               database = "userprofiles");
    mycursor = mydb.cursor()
    mycursor.execute("select * from login")
    print(username, password)

    if (username, password) in mycursor.fetchall():
    
        return render_template("input.html")
    else:
        return render_template("login.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = {"fueltype" : request.form["fueltype"],
        "aspiration" : request.form["aspiration"],
        "doornumber" : request.form["doors"],
        "carbody" : request.form["body"],
        "drivewheel" : request.form["wheeldrive"],
        "enginelocation" : request.form["engineloc"],
        "enginetype" : request.form["enginetype"],
        "cylindernumber" : request.form["cylindercount"],
        "fuelsystem" : request.form["fuelsys"],
        "symboling" : request.form["symboling"],
        "wheelbase" : toInches(request.form["wheelbase"]),
        "carlength" : toInches(request.form["carlength"]),
        "carwidth" : toInches(request.form["carwidth"]),
        "carheight" : toInches(request.form["carheight"]),
        "curbweight" : toPounds(request.form["curbweight"]),
        "enginesize" : toCubicInches(request.form["enginesize"]),
        "boreratio" : request.form["boreratio"],
        "stroke" : request.form["stroke"],
        "compressionratio" : request.form["compratio"],
        "horsepower" : request.form["horsepower"],
        "peakrpm" : request.form["peakrpm"],
        "citympg" : toMPG(request.form["citympg"]),
        "highwaympg" : toMPG(request.form["highmpg"])
    }
    i = convert(data, columns)
    pred = model.predict([i])[0][0]
    return render_template("output.html", data=round(pred))


if __name__ == '__main__':
    app.run(host = "localhost", port = 5000)