import mysql.connector
import json
import textwrap
import urllib.request
from flask import Flask,render_template,request,render_template_string
from urllib.request import HTTPError

import openpyxl
from openpyxl import Workbook

import cv2
from pyzbar import pyzbar

import speech_recognition as sr
from flask import redirect,url_for
import pyaudio
import time


# Other File
from app import app

# app=Flask(__name__,template_folder='template')


# VALID ISBN 5 NUMBERS:
# 0-8057-8068-8   To Kill a Mockingbird         ---> ISBN Vary
# 0-300-08480-3   Stalinism as a Way of Life
# 0-8112-0051-5   The Crack-Up --->ERR ONLY TITLE
# 0-8624-1828-3   The Journal of Sir Walter Scott   --->ISBN Vary
# 0-7073-0131-9   The Siege of Malta Rediscovered  ----> ERR ONLY TITLE ---> this happens becoz of No summary in the book to display

#  VALID ISBN 5 NUMBERS:
# 9780545586177 -   Catching Fire
# 9780439023481 -  The First Book of Hunger Games
# 9781423163008 -  The Heroes of Olympus: The Demigod Diaries
# 9781423121718 -  The Percy Jackson and the Olympians: Ultimate Guide
# 9780395294697 -  Tolkien and the Silmarils    ---->  ERR ONLY TITLE
# 9789459179710     NOT A VALID ISBN

recognizer=sr.Recognizer()
commands=["login"]

#  VOICE Assist Functions
def voice_command():
    with sr.Microphone() as source:
        print("Say Something...")
        recognizer.adjust_for_ambient_noise(source)
        audio=recognizer.listen(source,timeout=10)

    try:
        # recognize the audio using Google Web speech API
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        print("Sorry,I could not understand what you said.")
        return "Sorry, I could not understand what you said."

    except sr.RequestError as e:
        print(f"Could not request results;{e}")
        return f"Could not request results;{e}"
    except sr.WaitTimeoutError as e:
        print(f"Wait Timeout Error...{e}")
        return f"Wait Timeout Error...{e}"

# Voice to Login
def voice_login(text):
    global username, password
    global role
    global u, p
    u = ""
    p = ""
    username = "user1"
    password = "pass1"
    role = "check"

    # username=request.form['username']
    # password=request.form['password']
    # role=request.form['role']

    print(username)
    print(password)
    print(role)

    print("input da")
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="lsk12312",
        database="isbn"
    )
    mycursor = db.cursor()

    if text=="login":
        print("Varta Mame")

        time.sleep(3)
        select_query = f"SELECT * FROM USERS WHERE USERNAME='{username}'"
        mycursor.execute(select_query)
        existing_record = mycursor.fetchone()

        if (existing_record):
            try:
                username_query = f"SELECT USERNAME FROM USERS WHERE USERNAME='{username}'"
                mycursor.execute(username_query)  # type NONE
                username_record = mycursor.fetchone()
                # print(username_record)                   # username_record ---> tuple

                # If password is wrong Type Error Occurs

                u = "".join(username_record)  # tuple to str conversion
                # print(u)

                password_query = f"SELECT PASSWORD FROM USERS WHERE USERNAME='{username}' AND PASSWORD= '{password}' "
                # password_query = f"SELECT PASSWORD FROM USERS WHERE PASSWORD='{password}'"
                mycursor.execute(password_query)
                password_record = mycursor.fetchone()
                # print(password_record)              # password_record ---> tuple
                p = "".join(password_record)  # tuple to str conversion
                # print(p)

                if (u == username and password == p):
                    print("Correct user and pass")

                    return render_template('index.html')


            except TypeError as e:
                incorrect_pass ="""
                        <html>
                        <head>
                        <script>
                        alert("Incorrect Password.... ")
                        </script>
                        </head>
                        <body>
                        </body>
                        </html>
                        """
                print("tada2")
                return render_template_string(incorrect_pass)


        else:
            print("Please Register...")
            register_alert = """
                                        <html>
                                        <head>
                                        <script>
                                        alert("PLEASE REGISTER TO ACCESS...")
                                        </script>
                                        </head>
                                        <body>
                                        </body>
                                        </html>
                                        """

            return render_template_string(register_alert)
#
#         # query="INSERT INTO USER(username,password,role) VALUES('"+username+"','"+password+"','"+role+"')"
#     return render_template('login.html')


@app.route('/')
def index():
    return render_template('login.html')



# LOGIN BUTTON
@app.route('/login_button',methods=['POST'])
def login_button():
    global username,password
    global role
    global u,p
    u=""
    p=""
    localhost_addr="https://localhost:5000"

    db=mysql.connector.connect(
        host="localhost",
        user='root',
        password='lsk12312',
        database='isbn'
    )
    mycursor=db.cursor()

    username=request.form['username']
    password=request.form['password']
    role=request.form['role']

    print(username)
    print(password)
    print(role)

    if request.form['click']=='btn_click':

        time.sleep(3)
        select_query=f"SELECT * FROM USERS WHERE USERNAME='{username}'"
        mycursor.execute(select_query)
        existing_record=mycursor.fetchone()

        if(existing_record):
            try:
                username_query = f"SELECT USERNAME FROM USERS WHERE USERNAME='{username}'"
                mycursor.execute(username_query)  # type NONE
                username_record = mycursor.fetchone()
                # print(username_record)                   # username_record ---> tuple

                # If password is wrong Type Error Occurs

                u = "".join(username_record)  # tuple to str conversion
                # print(u)

                password_query=f"SELECT PASSWORD FROM USERS WHERE USERNAME='{username}' AND PASSWORD= '{password}' "
                # password_query = f"SELECT PASSWORD FROM USERS WHERE PASSWORD='{password}'"
                mycursor.execute(password_query)
                password_record = mycursor.fetchone()
                # print(password_record)              # password_record ---> tuple
                p = "".join(password_record)  # tuple to str conversion
                # print(p)

                if (u == username and password == p):
                    print("Correct user and pass")

                    #localhost_address=localhost_addr

                return render_template('index.html')    #Localhost address of isbn page


            except TypeError as e:
                incorrect_pass="""
                <html>
                <head>
                <script>
                alert("Incorrect Password.... ")
                </script>
                </head>
                <body>
                </body>
                </html>
                """
                print("tada")
                return render_template_string(incorrect_pass)


        else:
            print("Please Register...")
            register_alert = """
                                <html>
                                <head>
                                <script>
                                alert("PLEASE REGISTER TO ACCESS...")
                                </script>
                                </head>
                                <body>
                                </body>
                                </html>
                                """

            return render_template_string(register_alert)


        # query="INSERT INTO USER(username,password,role) VALUES('"+username+"','"+password+"','"+role+"')"
    return render_template('login.html')

# SIGN UP LINK
@app.route('/signup')
def signup_link():
    print("Sign up link")
    return render_template('signup.html')

# Login Page⬆️
# Sign Up Page ⬇️

# SIGNUP BUTTON
@app.route('/signup_button', methods=['POST'])
def signup():
    global name,role,email
    global username,password

    print("Check point 2")

    db=mysql.connector.connect(
        host="localhost",
        user='root',
        password='lsk12312',
        database='isbn'
    )
    mycursor=db.cursor()

    name=request.form['name']
    username=request.form['username']
    password=request.form['password']
    role=request.form['role']
    email=request.form['email']

    print(name)
    print(username)
    print(password)
    print(role)
    print(email)

    if request.form['click']=='btn_click':
        print("asdasd")
        query="INSERT INTO USERS(name,username,password,role,email) VALUES('"+name+"','"+username+"','"+password+"','"+role+"','"+email+"')"
        mycursor.execute(query)
        db.commit()
    return render_template('signup.html')

# LOGIN LINK
@app.route('/login')
def login_link():
    print("Login Back")
    return render_template("login.html")


# Future...
# # MIC BUTTON🎈
# @app.route('/mic_button',methods=['POST'])
# def mic_button():
#     global username, password
#     global role
#     global u, p
#     username = "user1"
#     password = "pass1"
#     role = "check"
#     u = ""
#     p = ""
#
#
#     if request.form['click']=='btn_click':
#
#         text = voice_command()
#
#         # username = request.form['username']
#         # password = request.form['password']
#         # role = request.form['role']
#
#         print(username)
#         print(password)
#         print(role)
#
#         voice_login(text)
#             # return "Working"
#         return render_template("login.html",recognized_text=text)
#         # elif "save to db" in text.lower():
#         #     voice_db()
#         #     print("save to db")
#         # elif "save to excel" in text.lower():
#         #     voice_excel()
#         #     print("save to excel")
#         # elif "clear" in text.lower():
#         #     voice_clear()
#         #     print("clear ah")
#         # else:
#         #     print("break")
#
#     return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True,port=7000)

# TABLE CREATION
# CREATE TABLE USERS(ID INT PRIMARY KEY AUTO_INCREMENT,NAME VARCHAR(50),USERNAME VARCHAR(50),PASSWORD VARCHAR(50),EMAIL VARCHAR(50),ROLE VARCHAR(50));
 # elif( username == u or password == p):
        #     print("Username Exists...")
        #     alert = """
        #                 <html>
        #                 <head>
        #                 <script>
        #                 alert("INCORRECT PASSWORD...")
        #                 </script>
        #                 </head>
        #                 <body>
        #                 </body>
        #                 </html>
        #                 """
        #
        #     return render_template_string(alert)
        #
        # elif(username == u is False or password == p is True):
        #     print("Password Exists...")
        #     alert2= """
        #                             <html>
        #                             <head>
        #                             <script>
        #                             alert("INCORRECT USERNAME...")
        #                             </script>
        #                             </head>
        #                             <body>
        #                             </body>
        #                             </html>
        #                             """
        #
        #     return render_template_string(alert2)
        # select * from books where username={username}
        #
        # if password == password

        # ---
# if(f"SELECT USERNAME FROM USERS WHERE USERNAME='{username}'"==request.form['username']):
        #     if(f"SELECT PASSWORD FROM USERS WHERE PASSWORD='{password}'"==request.form['password']):
        #         print("Login Success")