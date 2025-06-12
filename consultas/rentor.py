from flask import render_template, request, redirect, url_for, flash, session


def consultas_usuario(app, mysql): 
    @app.route('/')
    def rentor():
        logueado = session.get('logueado', False)
        id_usuario = session.get('id', False)
        cur_1= mysql.connection.cursor()
        cur_1.execute('select id_usuario from rentor where id_usuario={0}'.format(id_usuario))
        es_rentor=bool(cur_1.fetchone())
        cur_1.close()
        nombre = session.get('nombre', False)
        cur= mysql.connection.cursor()
        cur.execute('select * from rentor')
        rentors_data=cur.fetchall()
        cur.close()  
        return render_template('rentor.html', logueado=logueado, nombre=nombre, rentors=rentors_data, es_rentor=es_rentor)
    @app.route('/add_rentor', methods=['POST'])
    def add_rentor():
        if request.method=='POST':
            id_usuario =request.form['id_usuario']
            descripcion =request.form['descripcion']
            cur= mysql.connection.cursor()
            cur.execute('INSERT INTO usuario (id_usuario, descripcion) VALUES (%s, %s )',(id_usuario,descripcion))
            mysql.connection.commit()
            cur.close()
            flash('usuario agregado satisfactoriamente')
            return render_template('dvd.html')
    @app.route('/edit_rentor/<int:id_rentor>', methods=['GET', 'POST'])
    def edit_rentor(id_rentor):
        if request.method == 'POST':
            id_usuario = request.form['id_usuario']
            clasificacion = request.form['clasificacion']
            update_rentor(id_rentor, id_usuario, clasificacion)
            flash('Rentor actualizado correctamente')
            return redirect(url_for('rentors'))
        
        rentors_data = get_all_rentors()
        rentor = next((r for r in rentors_data if r[0] == id_rentor), None)
        return render_template('edit_rentor.html', rentor=rentor)
