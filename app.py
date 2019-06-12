from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


@app.route('/main')
def main():

    return render_template('main.html')


@app.route('/logOut')
def logOut():

    return render_template('index.html')



if __name__ == '__main__':
    app.run(port=5000, debug=True)
