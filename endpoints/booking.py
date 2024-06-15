
#Servicio que hace reserva:
from flask import jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, date
from config import engine

from flask import Blueprint

# Crea la blueprint del booking
booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/reserva', methods=['POST'])
def booking():
    """Realiza una reserva en la base de datos."""
    conn = engine.connect()
    new_booking = request.get_json()

    cantidad_noches = new_booking['cantidad_noches']
    fecha_ingreso = new_booking['fecha_ingreso']
    test_fecha_ingreso = datetime.strptime(fecha_ingreso, '%Y-%m-%d')
    fecha_actual = datetime.strptime(str(date.today()), '%Y-%m-%d')

    #Chequeo que la fecha sea mayor a la fecha actual
    if fecha_actual > test_fecha_ingreso:
        return jsonify({'message': 'No se puede reservar en una fecha pasada.'}), 400

    query = """
        INSERT INTO reservas (numero_habitacion, huespedes, fecha_ingreso, cantidad_noches, nombre, mail)
        VALUES (:numero_habitacion, :huespedes, :fecha_ingreso, :cantidad_noches, :nombre, :mail)
    """

    validation_date_query = """
        SELECT numero_habitacion
        FROM reservas
        WHERE numero_habitacion = :numero_habitacion
        AND DATE_ADD(fecha_ingreso, INTERVAL :cantidad_noches DAY) > :fecha_ingreso
        AND fecha_ingreso < DATE_ADD(:fecha_ingreso, INTERVAL :cantidad_noches DAY)
    """

    validation_capacity_query = """
        SELECT *
        FROM habitaciones
        WHERE capacidad >= :huespedes AND numero = :numero_habitacion
    """

    try:
        val_cap_result = conn.execute(text(validation_capacity_query), {
            'huespedes': new_booking['huespedes'],
            'numero_habitacion': new_booking['numero_habitacion']
        })


        if val_cap_result.rowcount == 0:
            conn.close()
            return jsonify(
                {"message": f"La habitacion numero {new_booking['numero_habitacion']} no cuenta con la suficiente capacidad"}
                ), 400
        
        val_date_result = conn.execute(text(validation_date_query), {
            'numero_habitacion': new_booking['numero_habitacion'],
            'fecha_ingreso': fecha_ingreso,
            'cantidad_noches': cantidad_noches,
        })


        if val_date_result.rowcount == 0:
            conn.execute(text(query), {
                'numero_habitacion': new_booking['numero_habitacion'],
                'huespedes': new_booking['huespedes'],
                'fecha_ingreso': fecha_ingreso,
                'cantidad_noches': cantidad_noches,
                'nombre': new_booking['nombre'],
                'mail': new_booking['mail']
            })
            conn.commit()
            conn.close()
            return jsonify(
                {"message": "Reserva realizada con exito"}
                ), 201
        else:
            conn.close()
            return jsonify(
                {"message": f"La habitacion numero {new_booking['numero_habitacion']} ya se encuentra reservada en las fechas seleccionadas"}
                ), 400
    except Exception as e:
        conn.close()
        return jsonify({'message': "Se ha producido un error"}), 500


#Servicio que muestre datos de reservas:
@booking_bp.route('/reservas', methods=['GET'])
def bookings():
    conn = engine.connect()
    query = """
        SELECT * FROM reservas;
    """
    try:
        result = conn.execute(text(query))
        conn.close()
        reservas = []
        for row in result:
            reserva = {
                "id": row.id,
                "numero_habitacion": row.numero_habitacion,
                "huespedes": row.huespedes,
                "fecha_ingreso": row.fecha_ingreso,
                "cantidad_noches": row.cantidad_noches,
                "nombre": row.nombre,
                "mail": row.mail
            }
            reservas.append(reserva)
        return jsonify(reservas), 200
    except SQLAlchemyError as e:
        return jsonify({'message': "Se ha producido un error"}), 500


#Servicio que cancela reserva:
@booking_bp.route('/cancelar_reserva', methods=['DELETE'])
def cancel_booking():
    """Cancela reserva de la db a partir de id"""
    conn = engine.connect()
    cancel_data = request.get_json()

    query = """
        DELETE FROM reservas
        WHERE id = :id
    """

    validation_query = """
        SELECT *
        FROM reservas
        WHERE id = :id
    """

    try:
        val_result = conn.execute(text(validation_query), {
            'id': cancel_data['id']
        })

        if val_result.rowcount > 0:
            conn.execute(text(query), {
                'id': cancel_data['id']
            })
            conn.commit()
            conn.close()
            return jsonify(
                {"message": "Reserva cancelada con éxito"}
                ), 202
        else:
            conn.close()
            return jsonify(
                {"message": "No se encontro una reserva con el ID proporcionado"}
                ), 404
    except Exception as e:
        conn.close()
        return jsonify({'message': "Se ha producido un error"}), 500


#Servicio que cambia cantidad de noches, o dia de check in:
@booking_bp.route('/cambiar_reserva', methods=['PATCH'])
def change_booking():
    conn = engine.connect()
    mod_booking_data = request.get_json()

    id_reserva = mod_booking_data.get('id')
    numero_habitacion = mod_booking_data.get('numero_habitacion')
    nueva_fecha_ingreso = mod_booking_data.get('nueva_fecha_ingreso')
    nuevas_noches = mod_booking_data.get('nuevas_noches')

    # Validar si la habitación existe en la base de datos
    query_validation = f"SELECT * FROM reservas WHERE id = {id_reserva};"
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount == 0:
            conn.close()
            return jsonify({'message': f"No existe la reserva id {id_reserva}"}), 404
    except SQLAlchemyError:
        return jsonify({'message': "Se ha producido un error"}), 500

    # Validar si la habitación está disponible en esa fecha
    validation_date_query = f"""
            SELECT numero_habitacion
            FROM reservas
            WHERE numero_habitacion = {numero_habitacion}
            AND DATE_ADD(fecha_ingreso, INTERVAL {nuevas_noches} DAY) > '{nueva_fecha_ingreso}'
            AND fecha_ingreso < DATE_ADD('{nueva_fecha_ingreso}', INTERVAL {nuevas_noches} DAY)
        """
    
    try:
        val_date_result = conn.execute(text(validation_date_query))
        print(val_date_result.rowcount)
        if val_date_result.rowcount != 0:
            return jsonify(
                {"message": f"La habitacion numero {numero_habitacion} ya se encuentra reservada en las fechas seleccionadas"}
                ), 400
    except SQLAlchemyError:
        conn.close()
        return jsonify({'message': "Se ha producido un error"}), 500


    # Actualizar la reserva
    query = f"""
                UPDATE reservas
                SET fecha_ingreso = '{nueva_fecha_ingreso}', cantidad_noches = {nuevas_noches}
                WHERE id = {id_reserva};
            """
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError:
        conn.close()
        return jsonify({'message': "Se ha producido un error"}), 500

    return jsonify({'message': 'Se ha modificado la reserva correctamente'}), 200