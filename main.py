from flask import Flask, flash, redirect, url_for, render_template, request
from datetime import datetime
from flask_mysqldb import MySQL


app = Flask(__name__)

app.secret_key = 'clave_secreta_flask'
# Conexion DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyectoflask'

mysql = MySQL(app)
# context processors

@app.context_processor
def date_now():
    return {
        'now':datetime.utcnow(),
    }

# endpoints

@app.route('/')
def index():
    edad = 18
    return render_template('index.html',
                            edad = edad,
                            )

@app.route('/informacion')
@app.route('/informacion/<string:nombre>/<apellidos>')
def informacion(nombre = 'Juan',apellidos='Herrera'):
    return render_template('informacion.html',
                            nombre=nombre,
                            apellidos=apellidos,
                            )

@app.route('/contacto')
@app.route('/contacto/<nombre>')
def contacto(nombre = None):
    texto = f"<h1>Pagina de contacto</h1>"
    if nombre != None:
        texto = f"<h1>Pagina de contacto {nombre}</h1>"
    return render_template('contacto.html')

@app.route('/redireccionar')
@app.route('/redireccionar/<redireccion>')
def redireccionar(redireccion = None):
    if redireccion is not None:
        return redirect(url_for('lenguajes'))
    return render_template('redireccionar.html')


@app.route('/lenguajes-de-programacion')
def lenguajes():
    return render_template('lenguajes.html')

@app.route('/crear-coche', methods=['GET','POST'])
def crear_coche():
    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        precio =request.form['precio']
        ciudad = request.form['ciudad']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO coches VALUES(NULL,%s,%s,%s,%s)",(marca,modelo,precio,ciudad))
        cursor.connection.commit()
        flash('Has creado el coche correctamente')
        return redirect(url_for('index'))
    return render_template('crear_coche.html')

@app.route('/coches')
def coches():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches ORDER BY id DESC")
    coches = cursor.fetchall()
    cursor.close()
    return render_template('coches.html',coches=coches)

@app.route('/coches/<int:coche_id>')
def coche(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches WHERE id = %s",(coche_id,))
    coche = cursor.fetchall()
    cursor.close()
    return render_template('coche.html',coche=coche[0])

@app.route('/borrar-coche/<int:coche_id>')
def borrar_coche(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM coches WHERE id = %s",(coche_id,))
    cursor.connection.commit()

    flash('El coche ha sido borrado')
    return redirect(url_for('coches'))

@app.route('/editar-coche/<int:coche_id>',methods=['GET','POST'])
def editar_coche(coche_id):
    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        precio =request.form['precio']
        ciudad = request.form['ciudad']
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE coches 
            SET marca = %s,
                modelo = %s,
                precio = %s,
                ciudad = %s
            WHERE id = %s
        """,(marca,modelo,precio,ciudad,coche_id))
        cursor.connection.commit()
        flash('Has editado el coche correctamente')
        return redirect(url_for('coches'))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches WHERE id = %s",(coche_id,))
    coche = cursor.fetchall()
    cursor.close()
    return render_template('crear_coche.html',coche=coche[0])
if __name__=='__main__':
    app.run(debug=True)