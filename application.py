from flask import Flask,render_template, make_response,request, jsonify,redirect,url_for,session,escape,send_file,Response,abort,send_from_directory
import pymysql.cursors
import requests
import re
import os
import json
import socket    
 

dbconfig={'host':'127.0.0.1',
                 'user':'root',
                 'password':'admin',
                 'db':'user',
                 'charset':'utf8mb4',
                 'cursorclass':pymysql.cursors.DictCursor}


#context manager
from mySQLconnection import MySQLConnection
#password verification module
from passwordVerification import Verify
#login verification module 
from loginDecorator import verify_login

application = Flask(__name__)
application.secret_key=os.urandom(24)


@application.route("/")
def main():
    return render_template('registration_page.html')
    
@application.route('/loginForm')
def loginForm():
    return render_template('login_page.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    
    error = None
    username=None
    password=None
    
    if request.method == 'POST':      
        username  = request.form['username']
        password  = request.form['password']
       
        with MySQLConnection(dbconfig) as cursor:                
            cursor.execute("SELECT COUNT(Username) as count FROM user_profile WHERE Username = %s;", [username]) # CHECKS IF USERNAME EXSIST
            userCount=cursor.fetchone().get('count')
            
            if userCount==1 :
                cursor.execute("SELECT Password FROM user_profile WHERE Username = %s;", [username]) # FETCH THE HASHED PASSWORD
                for row in cursor.fetchall():  
                    if(Verify.verify_password(row.get('Password'), password)):
                        
                        session['username'] = username
                        session['logged_in'] = True
                        cursor.execute("SELECT FirstName,LastName FROM user_profile WHERE Username = %s;",[username])
                        name=cursor.fetchone() 
                        firstName= name.get('FirstName')          
                        lastName = name.get('LastName')          
                        return render_template('logged_in.html',firstName=firstName,lastName=lastName,username=username)
                    else:
                        error = "Invalid Credential"            
            else:
                error = "Invalid Credential"
            
        
        return render_template('login_page.html', error=error,username=username,password=password)
    else:
        return redirect(url_for('loginForm'))
        

        
@application.route('/logout')
def logout():
    
    session.pop('username', None)
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('main'))


@application.route('/userRegistrationForm')
def userRegistrationForm():
    return render_template('registration_page.html')



@application.route('/registerUser',methods=['POST'])
def registerUser():  
    firstName=request.form.get('firstName')    
    lastName=request.form.get('lastName')    
     
    username=request.form.get('username')  
    password=request.form.get('password')  
    secondaryEmail=request.form.get('secondaryEmail') 
    password = Verify.hash_password(password)
    hostname = socket.gethostname()    
    IP = socket.gethostbyname(hostname) 
   
    
    with MySQLConnection(dbconfig) as cursor:
        sql = "INSERT INTO user_profile (FirstName,LastName,Username,SecondaryEmail,Password,IP) VALUES (%s,%s,%s,%s,%s,%s)";
        cursor.execute(sql, (firstName,lastName,username,secondaryEmail,password,IP))  
    
    return render_template('saved.html')
    




# run the app.
if __name__ == "__main__":
   
    application.debug = True
    application.run()
   

    
