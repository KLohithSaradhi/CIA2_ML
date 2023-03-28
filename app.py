from flask import Flask, request, render_template
import mysql.connector
import os
from keras.models import load_model
import cv2
import numpy as np

app = Flask(__name__)
inputDirectory = r"D:\College Files\SEM4\ML\CIA2\input"

model = load_model("model.h5")

def infer(filename, model):
    pixels = []
    img = cv2.imread(os.path.join(inputDirectory, filename))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    pixels.append(np.array(img))
    
    pixels = np.array(pixels)
    
    return model.predict(pixels)



@app.route('/')
def main():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("pwd")

    mydb = mysql.connector.connect(host = "localhost", 
                               user = "root", 
                               password = "hrao1272",
                               database = "userprofiles");
    mycursor = mydb.cursor()
    mycursor.execute("select * from login")

    if (username, password) in mycursor.fetchall():
    
        return render_template("input.html")
    else:
        return render_template("login.html")

@app.route('/predict', methods=['POST'])
def predict():
    f = request.files['file']
    f.save(os.path.join(inputDirectory, f.filename))
    print(infer(f.filename, model))
    return render_template("login.html")


if __name__ == '__main__':
    app.run(host = "localhost", port = 5000)