
#Servicio que hace reserva:
from flask import jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def booking(engine):
    """Realiza una reserva en la base de datos."""
    conn = engine.connect()
    new_booking = request.get_json()

    cantidad_noches = new_booking['cantidad_noches']
    fecha_ingreso = new_booking['fecha_ingreso']
    # fecha_salida = f"DATE_ADD('{fecha_ingreso}', INTERVAL {cantidad_noches} DAY)"

    query = """
        INSERT INTO reservas (numero_habitacion, huespedes, fecha_ingreso, cantidad_noches, nombre, mail)
        VALUES (:numero_habitacion, :huespedes, :fecha_ingreso, :cantidad_noches, :nombre, :mail)
    """

    validation_query = """
        SELECT numero_habitacion
        FROM reservas
        WHERE numero_habitacion = :numero_habitacion
        AND DATE_ADD(fecha_ingreso, INTERVAL :cantidad_noches DAY) > :fecha_ingreso
        AND fecha_ingreso < DATE_ADD(:fecha_ingreso, INTERVAL :cantidad_noches DAY)
    """

    try:
        val_result = conn.execute(text(validation_query), {
            'numero_habitacion': new_booking['numero_habitacion'],
            'fecha_ingreso': fecha_ingreso,
            'cantidad_noches': cantidad_noches
        })

        if val_result.rowcount == 0:
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
                {"message": "Reserva realizada con éxito"}
                ), 200
        else:
            conn.close()
            return jsonify(
                {"message": f"La habitación número {new_booking['numero_habitacion']} ya se encuentra reservada en las fechas seleccionadas"}
                ), 400
    except Exception as e:
        conn.close()
        return jsonify(
            {'message': f"Error al realizar la reserva: {str(e)}"}
            ), 500


#Servicio que muestre datos de reservas:
def bookings(engine):
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
        return jsonify(
            {'message': f'Error al obtener datos de reservas: {str(e)}'}
            ), 500


#Servicio que cancela reserva:
def cancel_booking(engine):
    """"""
    conn = engine.connect()
    cancel_data = request.get_json()

    query = """
        DELETE FROM reservas
        WHERE numero_habitacion = :numero_habitacion
        AND fecha_ingreso = :fecha_ingreso
        AND nombre = :nombre
        AND mail = :mail
    """

    validation_query = """
        SELECT *
        FROM reservas
        WHERE numero_habitacion = :numero_habitacion
        AND fecha_ingreso = :fecha_ingreso
        AND nombre = :nombre
        AND mail = :mail
    """

    try:
        val_result = conn.execute(text(validation_query), {
            'numero_habitacion': cancel_data['numero_habitacion'],
            'fecha_ingreso': cancel_data['fecha_ingreso'],
            'nombre': cancel_data['nombre'],
            'mail': cancel_data['mail']
        })

        if val_result.rowcount > 0:
            conn.execute(text(query), {
                'numero_habitacion': cancel_data['numero_habitacion'],
                'fecha_ingreso': cancel_data['fecha_ingreso'],
                'nombre': cancel_data['nombre'],
                'mail': cancel_data['mail']
            })
            conn.commit()
            conn.close()
            return jsonify(
                {"message": "Reserva cancelada con éxito"}
                ), 200
        else:
            conn.close()
            return jsonify(
                {"message": "No se encontró una reserva con los datos proporcionados"}
                ), 404
    except Exception as e:
        conn.close()
        return jsonify(
            {"message": f"Error al cancelar la reserva: {str(e)}"}
            ), 500


#Servicio que cambia cantidad de noches, o dia de check in:
def change_booking(engine):
    conn = engine.connect()
    mod_booking_data = request.get_json()

    room_number = mod_booking_data.get('numero_habitacion')
    new_checkin_date = mod_booking_data.get('nueva_fecha_checkin')
    new_nights = mod_booking_data.get('nuevas_noches')

    # Validar si la habitación existe en la base de datos
    query_validation = f"""
        SELECT * FROM habitaciones 
        WHERE numero = {room_number};
    """
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount == 0:
            conn.close()
            return jsonify(
                {'message': f"No existe la habitación número {room_number}"}
                ), 404
    except SQLAlchemyError as err:
        return jsonify(
            {'message': str(err.__cause__)}
            ), 500

    # Actualizar la reserva
    query = f"""
        UPDATE reservas
        SET fecha_checkin = '{new_checkin_date}', noches = {new_nights}
        WHERE numero_habitacion = {room_number};
    """
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(
            {'message': str(err.__cause__)}
            ), 500

    return jsonify(
        {'message': 'Se ha modificado la reserva correctamente'}
        ), 200
