from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

inicio = [
    {
        'author': 'Bienvenido',
        'titulo': 'Trabajo de Fin de Grado',
        'mensaje': 'Por favor, inicie sesión para entrar al portal'
    }
]

ejemploDiccionario = [
    {
        'author': 'Renato Sosa García',
        'titulo': 'Trabajo de Fin de Grado',
        'mensaje': 'Buenos días!'
    }
]

app = Flask(__name__)


# MYSQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'


@app.route('/')
def home():

    return render_template('index.html', ejemplo=ejemploDiccionario)


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts WHERE email = %s", (email,))
        user = cur.fetchone()
        print(user)
        cur.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                return render_template("main.html")
        else:
            return "Error : Contraseña o email incorrectos"
    else:
        return render_template("index.html", ejemplo=inicio)


@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route('/registro')
def registro():
    return render_template('registro.html', title='Registro')


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Se ha borrado el contacto correctamente')
    return redirect(url_for('lista'))


@app.route('/edit/<id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('edit-contact.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""

            UPDATE contacts
            SET fullname=% s,
                phone=% s,
                email=% s
            WHERE ID= % s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash('El contacto ha sido actualizado correctamente ')
        return redirect(url_for('lista'))


@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')


@app.route('/lista')
def lista():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('lista.html', contactos=data, title='Lista')


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['pass'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO contacts (fullname, phone, email, pass) VALUES(%s, %s, %s, %s)', (fullname, phone, email, hash_password))
        mysql.connection.commit()
        # session['fullname'] = fullname
        # session['email'] = email
        flash('El contacto ha sido agregado correctamente ')
        return redirect(url_for('lista'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)


#
# https://bootswatch.com/
# https://uigradients.com
# https://www.youtube.com/watch?v=tZTpKF2pkQo
# https://www.youtube.com/watch?v=QnDWIZuWYW0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=2
# alertas : https://www.youtube.com/watch?v=raqN7Il3Tr0
# login : https://www.youtube.com/watch?v=fOj16SIa02U
