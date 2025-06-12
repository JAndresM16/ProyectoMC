from consultas.usuario import consultas_usuario
from consultas.dvd import register_dvd
from consultas.renta import register_routes
from bd import iniciar_bd
app, mysql = iniciar_bd()

consultas_usuario(app, mysql)
register_dvd(app, mysql)
register_routes(app, mysql) 

if __name__ == '__main__':
    app.run(port=3000, debug=True)
