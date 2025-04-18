import mysql.connector
import json
import textwrap
import urllib.request
from flask import Flask,render_template,request,render_template_string
from urllib.request import HTTPError

import openpyxl
from openpyxl import Workbook
import datetime

import cv2
from pyzbar import pyzbar

import speech_recognition as sr
from flask import redirect,url_for
import pyaudio

# from Page 1 to Page 2
from app import app

# from tkinter import messagebox is NOT WORKING as it is Window Messages
# WORKING Python FLASK --->Important
# Function Calls
# @app.route("/")`
# Buttons

# 4 API Calls
# 1.Add button
# 2.Upload Button
# 3.To check ISBN invalid with same length of isbn number in Add button
# 4.To check ISBN invalid with same length od isbn number in Upload button

#Programmed by LIKULEASH 9489284767

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

#C:\Users\likul\Desktop\Intern\Project\ISBN Project


# app= Flask(__name__,template_folder='template')


# Initialize the recognizer for Mic Button atlast
recognizer = sr.Recognizer()
commands=['input','add','upload','delete','save to database','save to excel','clear']

# Add a global list to store book information
book_list = []

# Add Button Function
def add_book(isbn):
    # Already DB established

    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="lsk12312",
    #     password="lsk12312",
    #     database="isbn"
    # )
    # mycursor = db.cursor()
    print(isbn)
    print("Check Point 1")
    base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    with urllib.request.urlopen(base_api_link + isbn) as f:
        text = f.read()
        decoded_text = text.decode("utf-8")
        obj = json.loads(decoded_text)
        # print(decoded_text)   #
        # print(obj)        #dict

            # print(obj)
        if "items" in obj and len(obj["items"]) > 0:
                # print(len(obj["items"])) #
            volume_info = obj["items"][0]
            authors = volume_info["volumeInfo"].get("authors", [])  # list
            string_author = ' '.join(authors)
            no_summary="No Summary For this Book"
            identifiers = volume_info["volumeInfo"]["industryIdentifiers"]

            isbn_10 = None
            isbn_13 = None

            for identifier in identifiers:
                    if identifier["type"] == "ISBN_10":
                        isbn_10 = identifier["identifier"]
                    elif identifier["type"] == "ISBN_13":
                        isbn_13 = identifier["identifier"]
                        # print(isbn_10)
                        # print(isbn_13)

                # INSERT COMMAND in HTML TABLE
            if "searchInfo" in volume_info:         # Summary Exists
                data = (
                    volume_info["volumeInfo"]["title"],
                    string_author,
                    volume_info["searchInfo"]["textSnippet"],
                    volume_info["accessInfo"]["publicDomain"],
                    volume_info["volumeInfo"]["pageCount"],
                    volume_info["volumeInfo"]["language"]
                )
            else:                                   #No Summary
                data = (
                    volume_info["volumeInfo"]["title"],
                    string_author,
                    no_summary,
                    volume_info["accessInfo"]["publicDomain"],
                    volume_info["volumeInfo"]["pageCount"],
                    volume_info["volumeInfo"]["language"]
                )

            book_info = {
                "title": data[0],
                "author": data[1],
                "summary": data[2],
                "public_domain": data[3],
                "page_count": data[4],
                "language": data[5],
                "isbn_10":isbn_10,
                "isbn_13":isbn_13
            }
            print(book_info)
            return book_info
        else:
            print("Test")

            invalid_alert="""
            <html>
            <head>
            <script>
            alert("Invalid ISBN Format...")
            </script>
            </head>
            <body>
            </body>
            </html>
            """
            return invalid_alert
            # return render_template_string(invalid_alert)
        # return show_error("HTTP Request Successful", "The request was successful!")

# UPLOAD BUTTON Function
def upload_img(bdata):
    print(bdata)
    print("Check Point 2")

    base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    with urllib.request.urlopen(base_api_link + bdata) as f:
        text = f.read()
        decoded_text = text.decode("utf-8")
        obj = json.loads(decoded_text)

        if "items" in obj and len(obj["items"]) > 0:
            volume_info = obj["items"][0]
            authors = volume_info["volumeInfo"].get("authors", [])  # list
            string_author = ' '.join(authors)
            no_summary = "No Summary For this Book"
            identifiers = volume_info["volumeInfo"]["industryIdentifiers"]

            isbn_10 = None
            isbn_13 = None

            for identifier in identifiers:
                if identifier["type"] == "ISBN_10":
                    isbn_10 = identifier["identifier"]
                elif identifier["type"] == "ISBN_13":
                    isbn_13 = identifier["identifier"]
                    # print(isbn_10)
                    # print(isbn_13)

            # INSERT COMMAND in HTML TABLE
            if "searchInfo" in volume_info:  # Summary Exists
                data = (
                    volume_info["volumeInfo"]["title"],
                    string_author,
                    volume_info["searchInfo"]["textSnippet"],
                    volume_info["accessInfo"]["publicDomain"],
                    volume_info["volumeInfo"]["pageCount"],
                    volume_info["volumeInfo"]["language"]
                    )
            else:  # No Summary
                data = (
                    volume_info["volumeInfo"]["title"],
                    string_author,
                    no_summary,
                    volume_info["accessInfo"]["publicDomain"],
                    volume_info["volumeInfo"]["pageCount"],
                    volume_info["volumeInfo"]["language"]
                )

            book_info = {
                "title": data[0],
                "author": data[1],
                "summary": data[2],
                "public_domain": data[3],
                "page_count": data[4],
                "language": data[5],
                "isbn_10": isbn_10,
                "isbn_13": isbn_13
            }
            # print(book_info)
            return book_info


#INSERT FUNCTION to DB
def insert_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="lsk12312",
        database="isbn"
    )
    mycursor = db.cursor()

    # book_list=add_button()    #BAD REQUEST

    # LIST SEPERATION (,)
    # input_list = ["element1,element2,element3", "element4,element5"]
    # split_list = [item.split(',') for item in input_list]
    # print(split_list)

    # print(book_list)

    for data in book_list:
        # print(book_list)
        print(type(data))
        title = data['title']  # str
        author = data['author']  # str
        summary = data['summary']  # str
        public_domain = data['public_domain']  # Bool
        page_count = data['page_count']  # Int
        language = data['language']  # str
        isbn_10 = data['isbn_10']  # str
        isbn_13 = data['isbn_13']  # str

        # print(type(title))

        # print(f"Title: {title}")
        query = (
                "INSERT INTO BOOKS(TITLE,AUTHOR,PUBLIC_DOMAIN,PAGE_COUNT,LANGUAGE,SUMMARY,ISBN_10,ISBN_13)VALUES('" + title + "','" + author + "','" + str(
            public_domain) + "','" + str(
            page_count) + "','" + language + "','" + summary + "','" + isbn_10 + "','" + isbn_13 + "')")

        # query = ("INSERT INTO BOOKS(TITLE,AUTHOR,PUBLIC_DOMAIN,PAGE_COUNT,LANGUAGE,SUMMARY,ISBN_10,ISBN_13)VALUES"
        #          "('")+item['title']+"','"+item['author']+"','"+str(item['public_domain'])+"','"+str(item['page_count'])+"','"+item['language']+"','"+item['summary']+"','"+item['isbn_10']+"','"+item['isbn_13']+"')"

        mycursor.execute(query)
    db.commit()

    # print(book_list)   #list

    # print(book_info)




#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="lsk12312",
#         database="isbn"
#         )
#     mycursor = db.cursor()
#
#     print("asd")
#     table_data=request.form.getlist('isbn-table')
#     # print(table_data) #[]
#     for row in table_data:
#         data=row.split(',')
#         # print(row)
#         query = "INSERT INTO BOOKS(TITLE,AUTHOR,PAGE_DOMAIN,PAGE_COUNT,LANGUAGE,SUMMARY,ISBN_10,ISBN_13)VALUES ('"+data[0]+"','"+data[1]+"','"+data[2]+"','"+data[3]+"','"+data[4]+"','"+data[4]+"','"+data[5]+"','"+data[6]+"')"
#         # query=f"INSERT INTO BOOKS (TITLE,AUTHOR,PAGE_DOMAIN,PAGE_COUNT,LANGUAGE,SUMMARY,ISBN_10,ISBN_13)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
#         mycursor.execute(query,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
#     db.commit()
#     print("DATA INSERTED SUCCESSFULLY")


# INSERT TO EXCEL
def insert_excel():

    global book_list
    global file_count

    file_count=1

 #  while (file_count == 0):
    while (file_count != 0):
        timestamp=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename=f"Test{timestamp}.xlsx"

        wb = Workbook()
        sheet= wb.active

        sheet["A1"]="Title"
        sheet["B1"]="Author"
        sheet["C1"]="Public Domain"
        sheet["D1"]="Page Count"
        sheet["E1"]="Language"
        sheet["F1"]="Summary"
        sheet["G1"]="ISBN 10"
        sheet["H1"]="ISBN 13"

    # sheet.append(["Bid""Title", "Summary", "Authors", "Public Domain", "Page Count", "Language"])

        print(book_list)

        for item in book_list:
            title=item['title']
            author=item['author']
            public_domain=item['public_domain']
            page_count=item['page_count']
            language=item['language']
            summary=item['summary']
            isbn_10=item['isbn_10']
            isbn_13=item['isbn_13']

            cell=[title,author,public_domain,page_count,language,summary,isbn_10,isbn_13]

            sheet.append([cell[0],cell[1],cell[2],cell[3],cell[4],cell[5],cell[6],cell[7]])

        wb.save(filename=f"Test({file_count}).xlsx")
        file_count+=1
        print(file_count)
        if (file_count == 3):
            break



    # print(f"Excel File:'{filename}' created successfuly...")
    print("EXCEL INSERTED SUCCESSFULLY...")

#Show HTTP Error: Too Many Requests
def show_error(title,message):
    alert=f"""
    <html>
    <head>
    <script>
            alert("{title}\\n\\n{message}");
            window.location.replace("/");
        </script>
    </head>
    <body>
    </body>
    </html>
    """
    return render_template_string(alert)

def show_alert():       # HTML template with JS alert  Already Book Exist
    alert_template = """
    <html>
    <head>
    </head>
    <body>
        <script>
            alert('Book Already Exist in the Database');
        </script>
    </body>
    </html>
    """
    # print("Info inside Show Alert")
    return render_template_string(alert_template)
def show_invalid():
    alert="""
    <html>
    <head>
    </head>
    <body>
        <script>
            alert('ISBN DID NOT EXIST');
        </script>
    </body>
    </html>
    """
    return render_template_string(alert)

def show_valid(v_isbn):
    alert=f"""
    <html>
    <head>
    </head>
    <body>
        <script>
            alert('VALID ISBN:{v_isbn}');
        </script>
    </body>
    </html>
    """
    return render_template_string(alert)

# VOICE Assist Functions

def voice_command():
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=5)  # Listen for up to 20 seconds

    try:
        # Recognize the audio using Google Web Speech API
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return "Sorry, I could not understand what you said."
    except sr.RequestError as e:
        print(f"Could not request results;{e}")
        return f"Could not request results; {e}"
    except sr.WaitTimeoutError as e:
        print(f"Wait Timeout Error...{e}")
        return f"Wait Timeout Error...{e}"

def voice_clear(text):
    # global book_list
    print("clear")
    # book_list = []
    # return render_template('index.html', books=book_list)
    clear_button()

def voice_db(text):
    print("saved to database")
    insert_db()

def voice_excel(text):
    print("saved to excel")
    insert_excel()


#Voice to Add ISBN Not Woeking...
# def voice_add(text):
#     print("input da")
#     global isbn
#     global book_list
#
#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="lsk12312",
#         database="isbn"
#     )
#     mycursor = db.cursor()
#
#     # isbn=recognizer.recognize_google(audio)
#     # isbn = request.form['search']
#     # if request.form['click']=='btn_click':
#
#     # textbox=request.form['search']
#     # text=request.form['search']
#
#
#     # Remove space from String
#     # txt = ' g e e k '
#     # chk = "".join(txt.split())
#     # print(chk)
#
#     print(text)    #str
#     # print(isbn)
#     v_isbn="".join(text.split())
#     # print(isbn)
#     print(v_isbn)
#     if len(v_isbn)==10 or len(v_isbn)==13:
#         print("Valid ISBN Number...")
#     return show_valid(v_isbn)
#     # else:
#     #     print("Invalid ISBN")
#     #     return show_invalid
#     # add_book(v_isbn)
#     print("After add book...")
#     return render_template('index.html', books=book_list)
#
#     # if (len(isbn)==10 or len(isbn)==13):
#     #     select_query = f"SELECT * FROM BOOKS WHERE ISBN_13 = '{isbn}'"
#     #     mycursor.execute(select_query)
#     #     existing_record = mycursor.fetchone()
#     #     # print(existing_record)                          #tuple
#     #     if (existing_record):
#     #         print("Already Inserted Value")
#     #         return show_alert()             #JS Alert
#     #     elif (True):
#     #         try:
#     #             base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
#     #             with urllib.request.urlopen(base_api_link + isbn) as f:
#     #                 text = f.read()
#     #                 decoded_text = text.decode("utf-8")
#     #                 obj = json.loads(decoded_text)
#     #                 # print(decoded_text)   #
#     #                 # print(obj)        #dict
#     #                 if obj['totalItems'] == 0:
#     #                     return show_invalid()
#     #
#     #                 print(isbn)
#     #                 books_info = add_book(isbn)  # Fuction Call
#     #                 book_list.append(books_info)
#     #
#     #         except HTTPError as e:
#     #             if e.code == 429:
#     #                 print("HTTPError 429: Too Many Requests...")
#     #                 error_message = "HTTP Error 429: Too Many Requests chech after 12:30 pm "
#     #             else:
#     #                 print(f"Error Occurred{e.code}:{e.reason}")
#     #                 error_message = f"Error Occurred{e.code}:{e.reason}"
#     #
#     #                 return show_error("HTTP Request Error", error_message)
#     #
#     #         except Exception as e:
#     #             # messagebox.showerror(f"Error Occurred:{str(e)}")
#     #             print(f"Error Occurred:{str(e)}")
#     #             error_message = (f"Error Occurred:{str(e)}")
#     #
#     #             return show_error("Error", error_message)
#     #             # print(books_info)   #dict
#     #             # print(book_list)    #list
#     #             return render_template('index.html',books=book_list)


# Define a route to render the HTML page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # LOGIN BUTTON
# @app.route('/login_button',methods=['POST'])
# def login_button():
#     global username,password
#     global role
#     # db=mysql.connector.connect(
#     #     host="localhost",
#     #     user="root",
#     #     password="lsk12312",
#     #     database="isbn"
#     # )
#     # mycursor=db.cursor()
#
#     # role=request.form['role']
#
#     print("varta")
#     if request.form['click']=='btn_click':
#         print("ISBN Page Loaded")
#     return render_template('index.html')



#ADD BUTTON
@app.route('/add_button',methods=['POST'])
def add_button():
    global isbn
    global book_list

    try:

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="lsk12312",
            database="isbn"
        )
        mycursor = db.cursor()

        isbn=request.form['search']

        if request.form['click']=='btn_click':

            if (len(isbn)==10 or len(isbn)==13):

                select_query = f"SELECT * FROM BOOKS WHERE ISBN_13 = '{isbn}'"
                mycursor.execute(select_query)
                existing_record = mycursor.fetchone()
                # print(existing_record)                          #tuple
                if (existing_record):
                    print("Already Inserted Value")
                    return show_alert()             #JS Alert
                elif (True):
                    try:
                        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
                        with urllib.request.urlopen(base_api_link + isbn) as f:
                            text = f.read()
                            decoded_text = text.decode("utf-8")
                            obj= json.loads(decoded_text)
                            # print(decoded_text)   #
                            # print(obj)        #dict
                            if obj['totalItems'] == 0:
                                return show_invalid()
                            else:
                                print(isbn)
                                books_info = add_book(isbn)  # Fuction Call
                                book_list.append(books_info)

                    except HTTPError as e:
                        if e.code == 429:
                            print("HTTPError 429: Too Many Requests...")
                            error_message = "HTTP Error 429: Too Many Requests"
                        else:
                            print(f"Error Occurred{e.code}:{e.reason}")
                            error_message = f"Error Occurred{e.code}:{e.reason}"

                        return show_error("HTTP Request Error", error_message)

                    except Exception as e:

                    # messagebox.showerror(f"Error Occurred:{str(e)}")
                        print(f"Error Occurred:{str(e)}")
                        error_message = (f"Error Occurred:{str(e)}")

                        return show_error("Error", error_message)

            # else:
            #     try:
            #         print(isbn)
            #         books_info = add_book(isbn)  # Fuction Call
            #         book_list.append(books_info)
            #     except HTTPError as e:
            #         if e.code == 429:
            #             print("HTTPError 429: Too Many Requests...")
            #             error_message = "HTTP Error 429: Too Many Requests"
            #         else:
            #             print(f"Error Occurred{e.code}:{e.reason}")
            #             error_message = f"Error Occurred{e.code}:{e.reason}"
            #
            #         return show_error("HTTP Request Error", error_message)
            #
            #     except Exception as e:
            #
            #         # messagebox.showerror(f"Error Occurred:{str(e)}")
            #         print(f"Error Occurred:{str(e)}")
            #         error_message = (f"Error Occurred:{str(e)}")
            #
            #         return show_error("Error", error_message)
                # print(books_info)   #dict
                # print(book_list)    #list

        return render_template('index.html',books=book_list)
    except Exception as err:
        print("Add Button Error")
        return f"Error: {err}"
# UPLOAD BUTTON
@app.route('/upload_button',methods=['POST'])
def upload_button():
    global book_list
    global isbn

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="lsk12312",
        database="isbn"
    )
    mycursor = db.cursor()

    if request.form['click']=='btn_click':

        if 'fileInput' not in request.files:
            print("No file part")
        file=request.files['fileInput']

        if file.filename=='':

            print("No selected file")
        if file:

        #     process the uploaded file
            file.save('uploaded_file.jpg')
            print("File uploaded successfully...")

        print("Image Upload Function")


        # Barcode Upload
        # img=cv2.imread("isbn_barcode.jpg")
        img=cv2.imread("uploaded_file.jpg")
        code=pyzbar.decode(img)

        for barcode in code:
            x,y,z,h=barcode.rect
            cv2.rectangle(img,(x,y),(x+y,x+h),0,0,255,4)
            bdata=barcode.data.decode("utf-8")
            btype=barcode.type
            text=f"{bdata},{btype}"
            cv2.putText(img,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
            # print("ISBN FOUND:",bdata)
            # print("Length of ISBN:",len(bdata))

        if len(bdata)==10 or len(bdata)==13 or len(bdata)==17:

            select_query = f"SELECT * FROM BOOKS WHERE ISBN_13 = '{bdata}'"
            mycursor.execute(select_query)
            existing_record = mycursor.fetchone()
            # print(existing_record)                          #tuple
            if (existing_record):
                print("Already Inserted Value")
                return show_alert()  # JS Alert
            elif (True):
                try:
                    base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
                    with urllib.request.urlopen(base_api_link + bdata) as f:
                        text = f.read()
                        decoded_text = text.decode("utf-8")
                        obj = json.loads(decoded_text)
                        # print(decoded_text)   #
                        # print(obj)        #dict
                        if obj['totalItems'] == 0:
                            return show_invalid()

                        books_info=upload_img(bdata)
                        print(books_info)
                        book_list.append(books_info)

                except HTTPError as e:
                    if e.code==429:
                        print("HTTPError 429: Too Many Requests...")
                        error_message = "HTTP Error 429: Too Many Requests"
                    else:
                        print(f"Error Occurred{e.code}:{e.reason}")
                        error_message=f"Error Occurred{e.code}:{e.reason}"

                    return show_error("HTTP Request Error",error_message)

                except Exception as e:

                # messagebox.showerror(f"Error Occurred:{str(e)}")
                    print(f"Error Occurred:{str(e)}")
                    error_message=(f"Error Occurred:{str(e)}")

                    return show_error("Error", error_message)
        else:
            print("Invalid ISBN Format")
            print("ISBN Format is Wrong...")
            invalid_alert = """
                       <html>
                       <head>
                       </head>
                       <body>  
                       <script>
                           alert('ISBN FORMAT is WRONG...');
                       </script>
                       </body>
                       </html>
                       """
            return render_template_string(invalid_alert)

                # cv2.imshow("img",img)
                #
                # if cv2.waitKey(1) & 0xFF== ord('q'):
                #     cv2.destroyAllWindows()
                #     break
        return render_template("index.html",books=book_list)


# CLEAR BUTTON
@app.route('/clear_button',methods=['POST'])
def clear_button():
    if request.form['click']=='btn_click':
        # global book_list
        book_list=[]
        return render_template('index.html',books=book_list)

# REMOVE Button
@app.route("/remove_button",methods=['POST'])
def remove_item():
    if request.form['click'] == 'btn_click':
        index = int(request.form['index'])
        if 0 <= index < len(book_list):
            removed_book = book_list.pop(index)
    return render_template("index.html",books=book_list)




# SAVE BUTTON to DB
@app.route('/save_button', methods=['POST'])
def save_button():
    global books,book_list

    data = request.form['save']  # Get the data sent from the client
    # print("ISBN SAVED:"+isbn)       #global ISBN
    if request.form['save']=='btn_click':
        books_info=insert_db()

        print("DB INSERTED SUCCESSFULLY")

    return render_template('index.html',books=book_list)
    # return "Table data saved and stored in the database"

# SAVE BUTTON TO EXCEL
@app.route('/save_excel',methods=['POST'])
def save_excel():
    global book_list
    global isbn

    data = request.form['save']  # Get the data sent from the client
    # print("ISBN SAVED:" + isbn)  # global ISBN
    if request.form['save'] == 'btn_click':
        books_info = insert_excel()

    return render_template('index.html',books=book_list)
    # return "Table data saved in EXCEL"

# MIC BUTTON
@app.route('/mic_button',methods=['POST'])
def mic_button():
    if request.form['click']=='btn_click':
        text=voice_command()
        if "input"in text.lower():
            if text in commands:
                voice_add(text)
            # return "Working"
        elif "clear" in text.lower():
            if text in commands:
                voice_clear(text)
            return "Data Cleared"
        elif "save to database" in text.lower():
            if text in commands:
                voice_db(text)
                db_alert="""
                <html>
                <head>
                <script>
                alert("Saved to Database Successfully...")
                </script>
                </head>
                <body>
                </body>
                </html>
                """
                return render_template_string(db_alert)
        elif "save to excel" in text.lower():
            if text in commands:
                voice_excel(text)
                excel_alert="""
                <html>
                <head>
                <script>
                alert("Saved to Excel Successfully...")
                </script>
                </head>
                <body>
                </body>
                </html>
                """
                return render_template_string(excel_alert)

        else:
            print("Not Recognized: "+text)
            return render_template("index.html",recognized_text=text)


        # return render_template("index.html",recognized_text=text)

        # elif "save to db" in text.lower():
        #     voice_db()
        #     print("save to db")
        # elif "save to excel" in text.lower():
        #     voice_excel()
        #     print("save to excel")
        # elif "clear" in text.lower():
        #     voice_clear()
        #     print("clear ah")
        # else:
        #     print("break")

    return render_template("index.html")


# Run the application
# if __name__ == '__main__':
#     app.run(debug=True,port=5000)

# ---Future ---
#Database Creation
# mycursor.execute("CREATE DATABASE isbn")

# Table Creation
    # mycursor.execute("CREATE TABLE BOOKS(ID INT UNIQUE AUTO_INCREMENT,TITLE VARCHAR(100),AUTHOR VARCHAR(100),PUBLIC_DOMAIN VARCHAR(50),PAGE_COUNT VARCHAR(10),LANGUAGE VARCHAR(30),SUMMARY VARCHAR(1000),ISBN_10 VARCHAR(10),ISBN_13 VARCHAR(13) PRIMARY KEY)")
# mycursor.execute("DESCRIBE BOOKS")


 # mycursor.execute("DELETE FROM BOOKS WHERE ID='1'")
 # mycursor.execute("SELECT * FROM BOOKS")


#
# while True:
#
#
#     user_input = input("Enter ISBN (ISBN-10 or ISBN-13): ").strip()
#
#     if len(user_input) == 10 or len(user_input) == 13 or len(user_input) == 17:
#         get_book_info(user_input)
#     else:
#         print("Invalid ISBN format. Please enter a valid ISBN-10 or ISBN-13.")
#
#     status_update = input("\nEnter another ISBN? y or n: ").lower().strip()
#     if status_update == "n":
#         print("\nThank you! Have a nice day.")
#         break



# ISBN EXTRACTION and API Call
# base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    #
    # with urllib.request.urlopen(base_api_link + isbn) as f:
    #     text = f.read()
    #
    # decoded_text = text.decode("utf-8")
    # obj = json.loads(decoded_text)
    #
    # if "items" in obj and len(obj["items"]) > 0:
    #     volume_info = obj["items"][0]
    #     authors = volume_info["volumeInfo"].get("authors", [])
    #     no_summary="No Summary For this Book."
    #
    #
    #
    #
    #     # TO EXTRACT THE ISBN NUMBER BASED ON POSITION
    #     # global isbn_list, identifier13, isbn13
    #     # isbn_list = volume_info["volumeInfo"].get("industryIdentifiers", [])  # list to string conversion
    #     # print(isbn_list)
    #     # identifier13 = isbn_list[1]
    #     # isbn13 = identifier13["identifier"]
    #     # print(isbn13)
    #
    #
    #     if "items" in obj and len(obj["items"]) > 0:
    #         volume_info = obj["items"][0]
    #         authors = volume_info["volumeInfo"].get("authors", [])     #list
    #         string_author=' '.join(authors)
    #
    #         # TO EXTRACT ISBN 10 and isbn 13 based on TYPE
    #
    #         identifiers = volume_info["volumeInfo"]["industryIdentifiers"]
    #
    #         isbn_10 = None
    #         isbn_13 = None
    #
    #     for identifier in identifiers:
    #         if identifier["type"] == "ISBN_10":
    #             isbn_10 = identifier["identifier"]
    #         elif identifier["type"] == "ISBN_13":
    #             isbn_13 = identifier["identifier"]
    #
    #         print(isbn_10)
    #         print(isbn_13)
