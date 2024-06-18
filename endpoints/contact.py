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
    except SQLAlchemyError:
        return jsonify({'message': "An error has occurred."}), 500
    

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
            return jsonify({'message':'An identical contact already exists.'}), 404

    except SQLAlchemyError as e:
        return jsonify({'message': "An error has occurred."}), 500

    return jsonify(
        {'message':f'Contact has been added successfully.'}
        ), 201


#Servicio que elimina el mensaje de la tabla de contactos.
@contact_bp.route('/eliminar_contacto', methods = ['DELETE'])
def delete_contact():
    conn = engine.connect()
    del_cont = request.get_json()
    id = del_cont.get('id',None)
    if not id:
        return jsonify(
            {'message': 'Id is required to delete contact.'}
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
                {"message": f"Contact id: {id} does not exist."}
                ), 404
    except SQLAlchemyError as err:
        return jsonify({'message': "An error has occurred."}), 500
    return jsonify(
        {'message': 'Has been deleted successfully.'}
        ), 202