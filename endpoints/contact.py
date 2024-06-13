from flask import jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint
from config import engine

# Create a blueprint
contact_bp = Blueprint('contact', __name__)

#Servicio que muestre datos de consultas:
@contact_bp.route('/contactos', methods=['GET'])
def contacts():
    conn = engine.connect()
    query = """
        SELECT * FROM contactos;
    """
    try:
        result = conn.execute(text(query))
        conn.close()
        contactos = []
        for row in result:
            contacto = {
                "id": row.id,
                "asunto": row.asunto,
                "mensaje": row.mensaje,
                "nombre": row.nombre,
                "mail": row.mail
            }
            contactos.append(contacto)
        return jsonify(contactos), 200
    except SQLAlchemyError as e:
        return jsonify(
            {'message': f'Error al obtener datos de contactos: {str(e)}'}
            ), 500
    

#Servicio que agrega el mensaje con su nombre mail y asunto a la tabla de contactos.
@contact_bp.route('/agregar_contacto', methods = ['POST'])
def create_contact():
    conn = engine.connect()
    contacto = request.get_json()
    query = f"""
        INSERT INTO contactos (nombre, mail, asunto, mensaje) 
        VALUES (
            '{contacto['nombre']}',
            '{contacto['mail']}', 
            '{contacto['asunto']}', 
            '{contacto['mensaje']}'
        );
    """
    query_validation = f"""
        SELECT * FROM contactos 
        WHERE nombre = '{contacto['nombre']}' 
        AND mail = '{contacto['mail']}' 
        AND asunto = '{contacto['asunto']}' 
        AND mensaje = '{contacto['mensaje']}' ;
    """
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount == 0:
            result = conn.execute(text(query))

            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message':'Ya agregaste el mensaje de ese contacto.'}), 404

    except SQLAlchemyError as e:
        return jsonify(
            {'message':f'Ocurrio un error al agregar contactos: {str(e)}'}
            ), 500

    return jsonify(
        {'message':f'Se ha agregado correctamente el contacto'}
        ), 200


#Servicio que elimina el mensaje de la tabla de contactos.
@contact_bp.route('/eliminar_contacto', methods = ['DELETE'])
def delete_contact():
    conn = engine.connect()
    del_cont = request.get_json()
    id = del_cont.get('id',None)
    if not id:
        return jsonify(
            {'message': 'Se requiere id para eliminar el contacto'}
            ), 400

    query = f"""
        DELETE FROM contactos 
        WHERE id = {id};
    """
    validation_query = f"""
        SELECT * FROM contactos 
        WHERE id = {id};
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
                {"message": f"La consulta numero {id} no existe."}
                ), 404
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__)), 500
    return jsonify(
        {'message': 'Se ha eliminado correctamente'}
        ), 202