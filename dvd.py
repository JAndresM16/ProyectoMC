from flask import render_template, request, redirect, url_for, flash, session, Blueprint
register_dvd = Blueprint('dvd', __name__)

def register_dvd(app, mysql):
    @app.route('/dvd')
    def dvd():
        logueado = session.get('logueado', False) 
        nombre = session.get('nombre', False)
        id_usuario = session.get('id', False)
        cur_1= mysql.connection.cursor()
        cur_1.execute('select id_usuario from rentor where id_usuario={0}'.format(id_usuario))
        es_rentor=bool(cur_1.fetchone())
        cur_1.close()
        cur= mysql.connection.cursor()
        cur.execute('select * from dvd')
        data=cur.fetchall()
        cur.close()
        return render_template('dvd.html', logueado=logueado, nombre=nombre, peliculas=data, es_rentor=es_rentor)
    
    @app.route('/add_dvd', methods=['POST'])
    def add_dvd():
        id = session.get('id', False)
        cur_1=mysql.connection.cursor()
        cur_1.execute('select id_rentor from rentor where id_usuario={0}'.format(id)  )
        id_usuario = session.get('id', False)
        cur_2= mysql.connection.cursor()
        cur_2.execute('select * from rentor where id_usuario={0}'.format(id_usuario))
        es_rentor=cur_2.fetchone()
        if request.method=='POST':
            id_rentor = es_rentor[0]
            nombre =request.form['nombre']
            descripcion =request.form['descripcion']
            fecha_salida =request.form['fecha_salida']
            genero =request.form['genero']
            precio =request.form['precio']        
            cur= mysql.connection.cursor()
            cur.execute('INSERT INTO dvd (id_rentor, nombre, descripcion, fecha_salida, genero, precio) VALUES (%s, %s ,%s, %s ,%s ,%s)',(id_rentor,nombre,descripcion,fecha_salida,genero,precio))
            mysql.connection.commit()
            cur.close()
            flash('usuario agregado satisfactoriamente')
        return redirect(url_for('dvd'))
    
    @app.route('/obtener_dvd/<id_dvd>')
    def get_dvd(id_dvd):
        cur=mysql.connection.cursor()
        cur.execute('select * from usuario where id_usuario={0}'.format(id_dvd)  )
        data=cur.fetchall()
        contact=data[0]
        print(data[0])
        return contact
    
    @app.route('/delete_dvd/<string:id>')
    def delete_dvd(id):
        cur=mysql.connection.cursor()
        cur.execute('delete from renta where id_dvd={0}'.format(id))
        cur.execute('delete from dvd where id_dvd={0}'.format(id))
        
        mysql.connection.commit()
        cur.close()
        flash('datos eliminados satisfactoriamente')
        return redirect(url_for('dvd'))
    
    @app.route('/dvd_agregar')
    def dvd_agregar():
        logueado = session.get('logueado', False)
        nombre = session.get('nombre', False)
        id_usuario = session.get('id', False)
        cur_1= mysql.connection.cursor()
        cur_1.execute('select id_rentor from rentor where id_usuario={0}'.format(id_usuario))
        es_rentor=bool(cur_1.fetchone())
        cur_1.close()
        cur= mysql.connection.cursor()
        cur.execute('select * from dvd')
        data=cur.fetchall()
        cur.close()
        return render_template('edit_dvd.html', logueado=logueado, nombre=nombre, peliculas=data, es_rentor=es_rentor)

