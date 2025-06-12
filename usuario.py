from flask import render_template, request, redirect, url_for, flash, session
import MySQLdb.cursors
from bd import iniciar_bd

def consultas_usuario(app, mysql): 
    @app.route('/')
    def Index():
        logueado = session.get('logueado', False)
        id_usuario = session.get('id', False)
        cur_1= mysql.connection.cursor()
        cur_1.execute('select id_usuario from rentor where id_usuario={0}'.format(id_usuario))
        es_rentor=bool(cur_1.fetchone())
        cur_1.close()
        nombre = session.get('nombre', False)
        return render_template('index.html', logueado=logueado, nombre=nombre, es_rentor=es_rentor)
    @app.route('/add_usuario', methods=['POST'])
    def add_usuario():
        if request.method=='POST':
            nombre =request.form['nombre']
            apellido =request.form['apellido']
            email =request.form['email']
            contraseña =request.form['contraseña']
            fecha_nac =request.form['fecha_nac']
            descripcion =request.form['descripcion']
            cur= mysql.connection.cursor()
            cur.execute('INSERT INTO usuario (nombre, apellido, email, contraseña, fecha_nac, descripcion) VALUES (%s, %s ,%s, %s ,%s ,%s)',(nombre,apellido,email,contraseña,fecha_nac,descripcion))
            mysql.connection.commit()
            cur.close()
            flash('usuario agregado satisfactoriamente')
        return render_template("inicio_sesion.html", mensaje="Inicie Sesion")

    @app.route('/edit_usuario/<id>')
    def get_usuario(id):
        cur=mysql.connection.cursor()
        cur.execute('select * from usuario where id_usuario={0}'.format(id)  )
        data=cur.fetchall()
        print(data[0])
        return render_template('edit_usuario.html',contact=data[0])
    @app.route('/update/<id>', methods=['POST'] )
    def update_usuario(id):
        if request.method=='POST':
            nombre =request.form['nombre']
            apellido =request.form['apellido']
            email =request.form['email']
            contraseña =request.form['contraseña']
            fecha_nac =request.form['fecha_nac']
            descripcion =request.form['descripcion']
            cur=mysql.connection.cursor()
            cur.execute('update usuario set nombre=%s, apellido=%s, email=%s, contraseña=%s, fecha_nac=%s, descripcion=%s where id_usuario={0}'.format(id), (nombre,apellido,email,contraseña,fecha_nac,descripcion)) 
            mysql.connection.commit()
            print(id)
            cur.close()
            flash('datos actualizados satisfactoriamente')
            return redirect(url_for('Index'))
    @app.route('/delete/<string:id>')
    def delete_usuario(id):
        cur=mysql.connection.cursor()
        cur.execute('delete from dvd where id_rentor={0}'.format(id))
        cur.execute('delete from rentor where id_usuario={0}'.format(id))
        
        cur.execute('delete from usuario where id_usuario={0}'.format(id))
        
        mysql.connection.commit()
        cur.close()
        flash('datos eliminados satisfactoriamente')
        return redirect(url_for('Index'))
    @app.route('/acceso-login', methods=["GET","POST"])
    def login():
        app, mysql = iniciar_bd()
        if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword':
            _correo = request.form['txtCorreo']
            _contraseña = request.form['txtPassword']
            
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM usuario WHERE email = %s AND contraseña = %s',(_correo, _contraseña,))
            account = cur.fetchone()
            if account:
                session['logueado'] = True
                session['id'] = account['id_usuario']
                session['nombre'] = account['nombre']
                return redirect(url_for('Index'))
            else:
                return render_template("inicio_sesion.html", mensaje="Correo o Contraseña Incorrecta")
        return render_template ("index.html")
    
    @app.route('/iniciar_sesion')
    def Iniciar_sesion():
        return render_template ("inicio_sesion.html")
    
    @app.route('/registro')
    def registro():
        return render_template ("registro_usuario.html")
    
    @app.route('/cerrar_sesion')
    def logout():
        session.clear()
        return render_template ("index.html")