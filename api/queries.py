def get_query_nueva_reserva(reserva):
    return f"""
        INSERT INTO reservas
        (numero_habitacion, huespedes, fecha_ingreso, cantidad_noches, nombre, mail)
        VALUES (
            {reserva["numero_habitacion"]},
            {reserva["huespedes"]},
            '{reserva["fecha_ingreso"]}',
            {reserva["cantidad_noches"]},
            '{reserva["nombre"]}',
            '{reserva["mail"]}'
        );
    """

def get_query_verif_disponibilidad(reserva, dia):
    return f"""
        SELECT COUNT(*) AS reservas_existentes
        FROM reservas
        WHERE numero_habitacion = {reserva["numero_habitacion"]}
        AND fecha_ingreso <= '{dia}' AND DATE_ADD(fecha_ingreso, INTERVAL cantidad_noches DAY) > '{dia}';
    """

def get_query_nro_reserva(reserva):
    return f"""
        SELECT id
        FROM reservas
        WHERE
            numero_habitacion = {reserva["numero_habitacion"]}
            AND huespedes = {reserva["huespedes"]}
            AND fecha_ingreso = '{reserva["fecha_ingreso"]}'
            AND cantidad_noches = {reserva["cantidad_noches"]}
            AND nombre = '{reserva["nombre"]}'
            AND mail = '{reserva["mail"]}'
        ;
    """