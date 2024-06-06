from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root:scrumbeasts@localhost:3309/tp_database")



#Servicio que consulta disponibilidad:
@app.route('/disponibilidad', methods = ['GET'])
def disponibility():   
    conn = engine.connect()
    
    consulta = request.get_json() #diccionario que contiene fecha huespedes, ingreso y noches
    huespedes = consulta['huespedes'] 
    fecha_ingreso = datetime.strptime(consulta['fecha_ingreso'], '%Y-%m-%d')
    noches = consulta['cantidad_noches']
    fecha_salida = fecha_ingreso + timedelta(days=int(noches) + 1) 

    #query que pide todos los numeros de habitaciones que con capacidad mayor o igual a la de los huespedes pedidos.
    query_1 = f"""SELECT numero, precio FROM habitaciones WHERE capacidad >= {huespedes};"""
    #query que devuelve los numeros de las habitaciones que estan reservadas en las fechas solicitadas.
    query_2 = f"""SELECT numero_habitacion FROM reservas WHERE (DATE_ADD(fecha_ingreso, INTERVAL cantidad_noches + 1 DAY) > '{fecha_ingreso}' AND fecha_ingreso < '{fecha_salida}');"""
    
    try:
        result_1 = conn.execute(text(query_1))
        result_2 = conn.execute(text(query_2))
        
        conn.close() 
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})

    
    disponibilidad = []
    habitaciones_posibles = []
    reservas = []
    
    for row_1 in result_1:
        habitaciones_posibles.append((row_1.numero, row_1.precio))
    
    for row_2 in result_2:
        reservas.append(row_2.numero_habitacion)
    
    for numero, precio in habitaciones_posibles:
        entity = {}
        if numero in reservas:
            continue
        entity['numero_habitacion'] = numero
        entity['precio'] = precio
        
        disponibilidad.append(entity)

    return jsonify(disponibilidad), 200
    


#Servicio que verifica si existe el usuario y su contraseña:
@app.route('/usuario', methods = ['GET'])
def verify_user():   
    pass


#Servicio que muestre datos de habitaciones(promociones incluidas):
@app.route('/habitaciones', methods = ['GET'])
def room():   
    pass


#Servicio que hace reserva:
@app.route('/reserva', methods = ['POST'])
def booking():   
    pass


#Servicio que cancela reserva:
@app.route('/cancelar_reserva', methods = ['DELETE'])
def cancel_booking():   
    pass


#Servicio que cancela reserva:
@app.route('/eliminar_habitacion', methods = ['DELETE'])    
def delete_room():   
    pass


#Servicio que cambia cantidad de noches, o dia de check in:
@app.route('/cambiar_reserva', methods = ['PATCH'])
def change_booking():   
    pass


#Servicio que cambia el precio de una habitacion(modo admin):
@app.route('/cambiar_precio', methods = ['PATCH'])
def change_price():   
    pass


#Servicio que cambia las promociones de las habitaciones(modo admin):
@app.route('/cambiar_promocion', methods = ['PATCH'])
def change_promo():   
    pass




if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)