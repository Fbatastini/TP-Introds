from datetime import date, timedelta, datetime
from flask import jsonify
from sqlalchemy import text
from api.queries import get_query_verif_disponibilidad
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime, timedelta

def verificar_disponibilidad(conn, reserva):
    capacidad_habitacion_query = f"""
        SELECT capacidad
        FROM habitaciones
        WHERE numero = {reserva["numero_habitacion"]};
    """
    capacidad_habitacion = conn.execute(text(capacidad_habitacion_query)).fetchone()[0]
    fecha_ingreso = datetime.strptime(reserva["fecha_ingreso"], "%Y-%m-%d").date()  # Convierte string a datetime.date
    cantidad_noches = reserva["cantidad_noches"]


    for i in range(cantidad_noches):
        dia = fecha_ingreso + timedelta(days=i)
        dia_str = dia.strftime("%Y-%m-%d")  # Convierte datetime.date a string
        verif_disponibilidad_query = get_query_verif_disponibilidad(reserva, dia_str)
        habitaciones_reservadas = conn.execute(text(verif_disponibilidad_query)).fetchone()[0]
        if habitaciones_reservadas >= capacidad_habitacion:
            return jsonify({'message': f'The room number {reserva["numero_habitacion"]} is not available for {dia_str}.'}), 400


def verificar_fecha_pasada(conn, reserva):
    fecha_ingreso = datetime.strptime(reserva["fecha_ingreso"], "%Y-%m-%d").date()
    fecha_actual = date.today()
    if fecha_ingreso < fecha_actual:
        return jsonify({'message': 'It is not possible to make a reservation to a past date.'}), 400