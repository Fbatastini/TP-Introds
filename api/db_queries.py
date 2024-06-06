# db table queries
create_habitaciones_table = """
    CREATE TABLE IF NOT EXISTS habitaciones (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tipo_habitacion VARCHAR(50),
        cantidad INT
    )
"""


create_reservas_table = """
    CREATE TABLE IF NOT EXISTS reservas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100),
        mail VARCHAR(100),
        tipo_habitacion VARCHAR(50),
        cant_personas INT,
        check_in DATE,
        check_out DATE
    )
"""


create_dias_reservados_table = """
    CREATE TABLE IF NOT EXISTS dias_reservados (
        id_reserva INT,
        dia DATE,
        tipo_habitacion VARCHAR(50),
        FOREIGN KEY (id_reserva) REFERENCES reservas(id)
    )
"""

from sqlalchemy import text


def fill_tables(engine):
    # Execute SQL statements to create tables
    with engine.connect() as conn:

        # Execute SQL queries to insert data
        conn.execute(text("""
            INSERT INTO habitaciones (tipo_habitacion, cantidad)
            VALUES
                ('Individual', 10),
                ('Doble', 15),
                ('Triple', 8),
                ('Suite', 5);
        """))


        conn.execute(text("""
            INSERT INTO reservas (nombre, mail, tipo_habitacion, cant_personas, check_in, check_out)
            VALUES
                ('John Doe', 'john.doe@example.com', 'Doble', 2, '2023-06-15', '2023-06-18'),
                ('Jane Smith', 'jane.smith@example.com', 'Triple', 3, '2023-07-01', '2023-07-05'),
                ('Michael Johnson', 'michael.johnson@example.com', 'Suite', 4, '2023-08-10', '2023-08-15');
        """))


        conn.execute(text("""
            INSERT INTO dias_reservados (id_reserva, dia, tipo_habitacion)
            SELECT
                r.id,
                DATE_ADD(r.check_in, INTERVAL @dia_count := @dia_count + 1 DAY) AS dia,
                r.tipo_habitacion
            FROM
                reservas r
                CROSS JOIN (SELECT @dia_count := -1) AS vars
            WHERE
                @dia_count < DATEDIFF(r.check_out, r.check_in);
        """))