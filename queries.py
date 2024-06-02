def get_query_verif(reserva):
    return f""" 
        SELECT '{reserva["check_in"]}' >= CURDATE();
    """


def get_query_cant_dias_reservados(reserva):
    return f"""
        SELECT 
        DATEDIFF('{reserva["check_out"]}', '{reserva["check_in"]}');
    """


def get_query_habitaciones(reserva):
    return f"""
        SELECT cantidad 
        FROM habitaciones 
        WHERE tipo_habitacion='{reserva["tipo_habitacion"]}';
    """


def get_query_siguiente_dia(reserva, i):
    return f"""
        SELECT 
        DATE_ADD(
            '{reserva["check_in"]}', 
            INTERVAL {i} DAY
        ); 
    """


def get_query_verif_disponibilidad(reserva, dia):
    return  f"""
        SELECT * 
        FROM dias_reservados WHERE tipo_habitacion='{reserva["tipo_habitacion"]}' 
        AND dia='{dia}'
        ;
    """


def get_query(reserva):
    return f"""
        INSERT INTO reservas 
        (nombre, mail, tipo_habitacion, cant_personas, check_in, check_out)
        VALUES (
            '{reserva["nombre"]}', 
            '{reserva["mail"]}', 
            '{reserva["tipo_habitacion"]}', 
            '{reserva["cant_personas"]}', 
            '{reserva["check_in"]}', 
            '{reserva["check_out"]}'
        );
    """


def get_query_nro_reserva(reserva):
    return f"""
        SELECT nro_reserva 
        FROM reservas 
        WHERE 
            nombre='{reserva["nombre"]}' 
            AND mail='{reserva["mail"]}' 
            AND tipo_habitacion='{reserva["tipo_habitacion"]}' 
            AND cant_personas={reserva["cant_personas"]} 
            AND check_in='{reserva["check_in"]}' 
            AND check_out='{reserva["check_out"]}'
        ;
    """


def get_query_dia_reservado(reserva, Id, dia):
    return f"""
        INSERT INTO dias_reservados 
        VALUES (
            {Id}, '{dia}', 
            '{reserva["tipo_habitacion"]}'
        );
    """