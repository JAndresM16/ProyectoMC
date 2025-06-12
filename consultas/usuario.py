from flask import render_template, request, redirect, url_for, flash, session
import pymysql.cursors
from bd import iniciar_bd  # Asumo que aquí defines la conexión MySQL

def consultas_usuario(app, mysql): 
    @app.route('/')
    def Index():
        logueado = session.get('logueado', False)
        id_usuario = session.get('id', False)

        cur_1 = mysql.connection.cursor()
        cur_1.execute('SELECT id_usuario FROM rentor WHERE id_usuario = %s', (id_usuario,))
        es_rentor = bool(cur_1.fetchone())
        cur_1.close()

        nombre = session.get('nombre', False)
        return render_template('index.html', logueado=logueado, nombre=nombre, es_rentor=es_rentor)
 
    @app.route('/add_usuario', methods=['POST'])
    def add_usuario():
        if request.method == 'POST':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            contraseña = request.form['contraseña']
            fecha_nac = request.form['fecha_nac']
            descripcion = request.form['descripcion']

            cur = mysql.connection.cursor()
            cur.execute(
                'INSERT INTO usuario (nombre, apellido, email, contraseña, fecha_nac, descripcion) VALUES (%s, %s, %s, %s, %s, %s)',
                (nombre, apellido, email, contraseña, fecha_nac, descripcion)
            )
            mysql.connection.commit()
            cur.close()
            flash('Usuario agregado satisfactoriamente')

        return render_template("inicio_sesion.html", mensaje="Inicie Sesion")

    @app.route('/edit_usuario/<int:id>')
    def get_usuario(id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id,))
        data = cur.fetchall()
        cur.close()
        if data:
            print(data[0])
            return render_template('edit_usuario.html', contact=data[0])
        else:
            flash('Usuario no encontrado')
            return redirect(url_for('Index'))

    @app.route('/update/<int:id>', methods=['POST'])
    def update_usuario(id):
        if request.method == 'POST':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            contraseña = request.form['contraseña']
            fecha_nac = request.form['fecha_nac']
            descripcion = request.form['descripcion']

            cur = mysql.connection.cursor()
            cur.execute(
                'UPDATE usuario SET nombre = %s, apellido = %s, email = %s, contraseña = %s, fecha_nac = %s, descripcion = %s WHERE id_usuario = %s',
                (nombre, apellido, email, contraseña, fecha_nac, descripcion, id)
            )
            mysql.connection.commit()
            cur.close()
            flash('Datos actualizados satisfactoriamente')
            return redirect(url_for('Index'))

    @app.route('/delete/<int:id>')
    def delete_usuario(id):
        cur = mysql.connection.cursor()
        # Borrar en tablas relacionadas primero para evitar errores de integridad referencial
        cur.execute('DELETE FROM dvd WHERE id_rentor = %s', (id,))
        cur.execute('DELETE FROM rentor WHERE id_usuario = %s', (id,))
        cur.execute('DELETE FROM usuario WHERE id_usuario = %s', (id,))
        mysql.connection.commit()
        cur.close()
        flash('Datos eliminados satisfactoriamente')
        return redirect(url_for('Index'))

    @app.route('/acceso-login', methods=["GET", "POST"])
    def login():
        if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
            _correo = request.form['txtCorreo']
            _contraseña = request.form['txtPassword']

            cur = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cur.execute('SELECT * FROM usuario WHERE email = %s AND contraseña = %s', (_correo, _contraseña))
            account = cur.fetchone()
            cur.close()

            if account:
                session['logueado'] = True
                session['id'] = account['id_usuario']
                session['nombre'] = account['nombre']
                return redirect(url_for('Index'))
            else:
                return render_template("inicio_sesion.html", mensaje="Correo o Contraseña Incorrecta")
        return render_template("index.html")

    @app.route('/iniciar_sesion')
    def Iniciar_sesion():
        return render_template("inicio_sesion.html")

    @app.route('/registro')
    def registro():
        return render_template("registro_usuario.html")

    @app.route('/cerrar_sesion')
    def logout():
        session.clear()
        return render_template("index.html")
