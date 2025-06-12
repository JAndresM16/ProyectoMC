from flask import render_template, request, redirect, url_for, flash, session, make_response
from fpdf import FPDF
from datetime import date, timedelta
from consultas.dvd import register_dvd 

def register_routes(app, mysql):
    @app.route('/rentas')
    def rentas():
        logueado = session.get('logueado', False)
        id_usuario = session.get('id', False)
        cur_1= mysql.connection.cursor()
        cur_1.execute('select id_usuario from rentor where id_usuario={0}'.format(id_usuario))
        es_rentor=bool(cur_1.fetchone())
        cur_1.close() 
        nombre = session.get('nombre', False)
        cur= mysql.connection.cursor()
        cur.execute('select * from dvd')
        data=cur.fetchall()
        cur.close()
        return render_template('dvd.html', logueado=logueado, nombre=nombre, peliculas=data, es_rentor=es_rentor)

    @app.route('/add_renta/<int:id_dvd>/<int:id_rentor>', methods=['POST'])
    def add_renta(id_dvd, id_rentor):
        cantidad = request.form.get('cantidad')
        logueado = session.get('logueado', False)
        id_usuario = session.get('id', False)
        if not id_usuario:
            flash('Por favor, inicie sesión primero.', 'danger')
            return render_template('inicio_sesion.html')
        cur_2 = mysql.connection.cursor()
        cur_2.execute('SELECT * FROM dvd WHERE id_dvd = {0}'.format(id_dvd))
        pelicula = cur_2.fetchone()
        if not pelicula:
            flash('Película no encontrada.', 'danger')
            return redirect(url_for('rentas'))
        if request.method == 'POST':
            cantidad = int(request.form['cantidad'])
            fecha_renta = date.today()
            fecha_entrega = fecha_renta + timedelta(days=7)
            total = pelicula[6] * cantidad

            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO renta (id_rentor, id_dvd, id_usuario, fecha_renta, fecha_entrega, cantidad, total) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                        (id_rentor, id_dvd, id_usuario, fecha_renta, fecha_entrega, cantidad, total))
            id_renta = cur.lastrowid
            mysql.connection.commit()
            cur.close()

            flash('Película rentada satisfactoriamente.', 'success')
            return redirect(url_for('factura', id_renta=id_renta, id_dvd=id_dvd, id_rentor=id_rentor, cantidad=cantidad))
        return render_template("renta.html", pelicula=pelicula)

    @app.route('/factura/<id_renta>/<id_dvd>/<id_rentor>/<cantidad>')
    def factura(id_renta,id_dvd, id_rentor, cantidad):
        id_usuario = session.get('id', False)
        cur_2 = mysql.connection.cursor()
        cur_2.execute('SELECT * FROM usuario WHERE id_usuario = {0}'.format(id_usuario))
        nombre_usuario = cur_2.fetchone()
        cur_3 = mysql.connection.cursor()
        cur_3.execute('SELECT * FROM rentor WHERE id_rentor = {0}'.format(id_rentor))
        id_usuario_rentor = cur_3.fetchone()
        cur_4 = mysql.connection.cursor()
        cur_4.execute('SELECT * FROM usuario WHERE id_usuario = {0}'.format(id_usuario_rentor[0]))
        nombre_usuario_rentor = cur_4.fetchone()
        cur_5 = mysql.connection.cursor()
        cur_5.execute('SELECT * FROM renta WHERE id_renta = {0}'.format(id_renta))
        renta = cur_5.fetchone()
        cur_6 = mysql.connection.cursor()
        cur_6.execute('SELECT * FROM dvd WHERE id_dvd = {0}'.format(id_dvd))
        dvd = cur_6.fetchone()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título
        pdf.cell(200, 10, txt="Factura de Renta", ln=True, align='C')
        pdf.ln(10)

        # Información del cliente
        pdf.cell(200, 10, txt=f"Puesto en rento por: {nombre_usuario_rentor[1]}", ln=True)
        pdf.cell(200, 10, txt=f"Cliente: {nombre_usuario[1]}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha de renta: {renta[4]}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha de entrega: {renta[5]}", ln=True)
        pdf.ln(10)

        # Detalles de la renta
        total = renta[7]
        pdf.cell(200, 10, txt=f"Película: {dvd[2]}", ln=True)
        pdf.cell(200, 10, txt=f"Cantidad: {cantidad}", ln=True)
        pdf.cell(200, 10, txt=f"Precio unitario: ${dvd[6]}", ln=True)
        pdf.cell(200, 10, txt=f"Total: ${renta[7]}", ln=True)

        # Guardar el PDF
        response = make_response(pdf.output(dest='S').encode('latin1'))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=factura_{id_renta}.pdf'
        return response
