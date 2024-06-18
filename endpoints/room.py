"""room endpoints"""
from flask import jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from config import engine
from flask import Blueprint

# Create a blueprint
room_bp = Blueprint('room', __name__)

# # Servicio que muestra las habitaciones disponibles:
@room_bp.route('/habitaciones', methods=['GET'])
def room():
    """Muestra los datos de las habitaciones disponibles."""
    conn = engine.connect()
    query = """
        SELECT numero, precio, capacidad, descripcion, promocion
        FROM habitaciones;
    """
    try:
        result = conn.execute(text(query))
        conn.close()
        habitaciones = []
        for row in result:
            habitacion = {
                "numero": row.numero,
                "precio": row.precio,
                "capacidad": row.capacidad,
                "descripcion": row.descripcion,
                "promocion": row.promocion
            }
            habitaciones.append(habitacion)
        return jsonify(habitaciones), 200
    except SQLAlchemyError as e:
        return jsonify({'message': "Se ha producido un error"}), 500


#Servicio que agrega habitacion(admin):
@room_bp.route('/agregar_habitacion', methods = ['POST'])
def create_room():
    conn = engine.connect()
    new_room = request.get_json()

    query = f"""
        INSERT INTO habitaciones (numero, precio, capacidad, descripcion, promocion)
        VALUES (
            {new_room['numero']}, 
            {new_room['precio']}, 
            {new_room['capacidad']}, 
            '{new_room['descripcion']}', 
            '{new_room['promocion']}'
            );
    """
    validation_query = f"""
        SELECT numero 
        FROM habitaciones 
        WHERE numero = {new_room['numero']}
    """
    try:
        val_result = conn.execute(text(validation_query))

        if val_result.rowcount == 0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify(
                {"message": f"La habitacion numero {new_room['numero']} ya existe."}
                ), 400
    except SQLAlchemyError as err:
        return jsonify({'message': "Se ha producido un error"}), 500

    return jsonify(
        {'message': 'Se ha agregado correctamente'}
        ), 201


#Servicio que elimina habitacion(admin):
@room_bp.route('/eliminar_habitacion', methods = ['DELETE'])
def delete_room():
    conn = engine.connect()
    del_room = request.get_json()

    query = f"""
        DELETE FROM habitaciones 
        WHERE numero = {del_room['numero']};
    """
    validation_query = f"""
        SELECT * FROM habitaciones 
        WHERE numero = {del_room['numero']}
    """
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify(
                {"message": f"La habitacion numero {del_room['numero']} no existe."}
                ), 404
    except SQLAlchemyError as err:
        return jsonify({'message': "Se ha producido un error"}), 500
    return jsonify(
        {'message': 'Se ha eliminado correctamente'}
        ), 202


#Servicio que cambia el precio de una habitacion(modo admin):
@room_bp.route('/cambiar_precio', methods = ['PATCH'])
def change_price():
    conn = engine.connect()
    mod_room_price = request.get_json()

    query = f"""
        UPDATE habitaciones 
        SET precio = '{mod_room_price['nuevo_precio']}' 
        WHERE numero = {mod_room_price['numero']};
    """
    query_validation = f"""
        SELECT * FROM habitaciones 
        WHERE numero = {mod_room_price['numero']};
    """
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount != 0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify(
                {'message': f"No existe la habitacion numero {mod_room_price['numero']}"}
                ), 404
    except SQLAlchemyError as err:
        return jsonify({'message': "Se ha producido un error"}), 500

    return jsonify(
        {'message': 'Se ha modificado correctamente'}
        ), 200


#Servicio que cambia las promociones de las habitaciones(modo admin):
@room_bp.route('/cambiar_promocion', methods=['PATCH'])
def change_promo():
    try:
        # Obtener datos de la solicitud PATCH
        data = request.get_json()
        numero_habitacion = data.get('numero_habitacion')
        nueva_promocion = data.get('nueva_promocion')

        # Validar que los datos requeridos estén presentes
        if not numero_habitacion or not nueva_promocion:
            return jsonify(
                {'message': 'Se requieren el numero de habitacion y la nueva promocion.'}
                ), 400

        # Actualizar la promoción en la base de datos
        conn = engine.connect()
        query = f"""
            UPDATE habitaciones
            SET promocion = '{nueva_promocion}'
            WHERE numero = {numero_habitacion};
        """

        # Validar si la habitación existe en la base de datos
        query_validation = f"SELECT * FROM habitaciones WHERE numero = {numero_habitacion};"
        try:
            val_result = conn.execute(text(query_validation))
            if val_result.rowcount == 0:
                conn.close()
                return jsonify({'message': f"No existe la habitacion {numero_habitacion}"}), 404
        except SQLAlchemyError as err:
            return jsonify({'message': "Se ha producido un error"}), 500
        
        conn.execute(text(query))
        conn.commit()
        conn.close()

        return jsonify(
            {'message': f'Promocion actualizada para la habitacion {numero_habitacion}.'}
            ), 200

    except Exception as e:
        return jsonify({'message': "Se ha producido un error"}), 500




#Servicio que cambia la descripcion de una habitacion(modo admin):
@room_bp.route('/cambiar_descripcion', methods = ['PATCH'])
def change_description():
    conn = engine.connect()
    mod_room_description = request.get_json()

    query = f"""
        UPDATE habitaciones 
        SET descripcion = '{mod_room_description['nueva_descripcion']}' 
        WHERE numero = {mod_room_description['numero']};
    """
    query_validation = f"""
        SELECT * FROM habitaciones 
        WHERE numero = {mod_room_description['numero']};
    """
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount != 0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify(
                {'message': f"No existe la habitacion numero {mod_room_description['numero']}"}
                ), 404
    except SQLAlchemyError as err:
        return jsonify({'message': "Se ha producido un error"}), 500

    return jsonify(
        {'message': 'Se ha modificado correctamente'}
        ), 201
