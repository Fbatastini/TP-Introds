from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://usuario:scrumbeasts@localhost/tp_database")



#Servicio que consulta disponibilidad:
@app.route('/disponibilidad', methods = ['GET'])
def disponibility():   
    pass


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