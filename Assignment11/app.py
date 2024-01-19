# Queens College
# CSCI 355 - Internet and Web Technology 
# Winter 2024
# Shah Bhuiyan
# Assignment 11 - Web-Based Application
# Worked with the class


import os
from flask import Flask, render_template, request, redirect, url_for, session
import webbrowser

app = Flask(__name__)
logged_in = False


@app.route('/')
def home_page():
    return render_template('login.html')


@app.route('/hello/<name>')
def hello_name(name):
    return f'Hello {name}!'

def read_file(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        states = [line.strip().split(",") for line in lines]
        return states[0], states[1:]
@app.route('/states')
def states():
    title = 'The United States'
    headers, data, = read_file('states.csv')
    return render_template('results.html', title=title, headers=headers, data=data)


@app.route('/my_state', methods=['GET', 'POST'])
def my_state():
    if request.method.upper() == 'POST':
        state = request.form['state']
        title = 'The United States'
        headers, data = read_file('states.csv')
        headers.append('selected')
        for row in data:
            row.append('')
            if row[0] == state:
                row[4] = '##############'
        return render_template('results.html', title=title, headers=headers, data=data)


@app.route('/login', methods=['POST'])
def login():
    global logged_in
    if request.method.upper() == 'POST':
        login = request.form['login']
        password = request.form['password']
    if login == 'shahjacob' and password == '355':
        logged_in = True
        headers, data = read_file('states.csv')
        states = [row[0] for row in data]
        # definitely do not uncomment below. return ends execution of the current function, so rendering choose_state.html will never even happen
        # return f'User {login} has successfully logged in.'
        return render_template('choose_state.html', states=states)
    else:
        return f'User {login} has been rejected.'








def open_file_in_browser(file_name):
    url = 'file:///' + os.getcwd() + '/' + file_name
    print(url)
    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    app.run()
