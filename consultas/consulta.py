from flask import render_template, request, redirect, url_for, flash

def registrar_consultas(app, mysql):
    @app.route('/')
    def Index():
        cur= mysql.connection.cursor()
        cur.execute('select * from usuario')
        data=cur.fetchall()
        cur.close()
        return render_template('index.html',usuario=data) 
    @app.route('/add_contact', methods=['POST'])
    def add_contact(): 
        if request.method=='POST':
            id_usuario=request.form['id_usuario']
            nombre=request.form['phone']
            apellido=request.form['email']
            email=request.form['email']
            contraseña=request.form['email']
            fecha_nac=request.form['email']
            descripcion=request.form['email']
            cur= mysql.connection.cursor()
            cur.execute('INSERT INTO usuario (id_usuario,nombre,apellido,email,contraseña,fecha_nac,descripcion) VALUES (%s, %s ,%s)',(id_usuario,nombre,apellido,email,contraseña,fecha_nac,descripcion))
            mysql.connection.commit()
            cur.close()
            flash('contacto agregado satisfactoriamente')
            return redirect(url_for('Index'))
    @app.route('/edit/<id>')
    def get_contact(id):
        cur=mysql.connection.cursor()
        cur.execute('select * from usuario where id={0}'.format(id)  )
        data=cur.fetchall()
        print(data[0])
        return render_template('edit-contact.html',contact=data[0])
    @app.route('/update/<id>', methods=['POST'] )
    def update_contact(id):
        if request.method=='POST':
            fullname=request.form['fullname']
            phone=request.form['phone']
            email=request.form['email']
            cur=mysql.connection.cursor()
            cur.execute('update contacts set fullname=%s, phone=%s, email=%s where id={0}'.format(id), (fullname,phone,email)) 
            mysql.connection.commit()
            print(id)
            cur.close()
            flash('datos actualizados satisfactoriamente')
            return redirect(url_for('Index'))
    @app.route('/delete/<string:id>')
    def delete_contact(id):
        cur=mysql.connection.cursor()
        cur.execute('delete from contacts where id={0}'.format(id))
        mysql.connection.commit()
        cur.close()
        flash('datos eliminados satisfactoriamente')
        return redirect(url_for('Index'))