from flask import jsonify, request, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, date
from config import engine

verifications_bp = Blueprint('verifications', __name__)

#Servicio que consulta disponibilidad:
@verifications_bp.route('/disponibilidad', methods = ['GET'])
def disponibility():
    """Consulta la disponibilidad de habitaciones en una fecha y cantidad de noches dadas."""
    conn = engine.connect()

    consulta = request.get_json() #diccionario que contiene fecha huespedes, ingreso y noches
    huespedes = consulta['huespedes']

    #Chequeo que la fecha sea correcta
    try:
        fecha_ingreso = datetime.strptime(consulta['fecha_ingreso'], '%Y-%m-%d')
    except Exception:
        return jsonify({'message': 'La fecha ingresada no existe.'}), 400

    noches = consulta['cantidad_noches']
    fecha_salida = fecha_ingreso + timedelta(days=int(noches) + 1)
    fecha_actual = datetime.strptime(str(date.today()), '%Y-%m-%d')

    #Chequeo que la fecha sea mayor a la fecha actual
    if fecha_actual > fecha_ingreso:
        return jsonify({'message': 'No se puede reservar en una fecha pasada.'}), 400

    #query que pide todos los numeros de habitaciones que con capacidad mayor o igual a la de los huespedes pedidos.
    query_1 = f"""
        SELECT numero, precio 
        FROM habitaciones 
        WHERE capacidad >= {huespedes};
    """
    #query que devuelve los numeros de las habitaciones que estan reservadas en las fechas solicitadas.
    query_2 = f"""
        SELECT numero_habitacion 
        FROM reservas 
        WHERE (DATE_ADD(fecha_ingreso, INTERVAL cantidad_noches + 1 DAY) > '{fecha_ingreso}' 
        AND fecha_ingreso < '{fecha_salida}');
    """

    try:
        result_1 = conn.execute(text(query_1))
        result_2 = conn.execute(text(query_2))

        conn.close()
    except SQLAlchemyError as err:
        return jsonify(
            {'message': 'Se ha producido un error' + str(err.__cause__)}
            ), 500


    disponibilidad = []
    reservas = []

    for row_2 in result_2:
        reservas.append(row_2.numero_habitacion)

    for row_1 in result_1:
        entity = {}
        if row_1.numero in reservas:
            continue
        entity['numero_habitacion'] = row_1.numero
        entity['precio'] = row_1.precio

        disponibilidad.append(entity)

    return jsonify(disponibilidad), 200


#Servicio que verifica si existe el usuario y su contraseña:
@verifications_bp.route('/user/<user>/<password>', methods=['GET'])
def verificar_usuario(user, password):
    """Verifica si el usuario y contraseña existen en la base de datos."""
    conn = engine.connect()

    query = f"""
        Select * FROM usuarios 
        WHERE usuario = '{user}' 
        and clave = '{password}'
    """

    try:
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as e:
        return jsonify(str(e.__cause__)), 500

    if result.rowcount != 0:
        return jsonify({'message':'exists'}), 200
    else:
        return jsonify({'message':'does not exist'}), 404