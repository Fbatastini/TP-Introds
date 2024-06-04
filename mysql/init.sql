CREATE TABLE reservas (
    numero_reserva INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    mail VARCHAR(120) NOT NULL,
    tipo_habitacion VARCHAR(10) NOT NULL,
    cantidad_personas INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE NOT NULL
);

CREATE TABLE reservas_diarias (
    numero_reserva INT NOT NULL,
    dia DATE NOT NULL,
    tipo_habitacion varchar(10) NOT NULL
);

CREATE TABLE habitaciones (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tipo_habitacion VARCHAR(10) NOT NULL,
    cantidad_total INT NOT NULL
);

/* Agregamos datos a la tabla reservas */
INSERT INTO reservas (nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES ("Manuel", "manuel@fi.uba.ar", "normal", 4, "2024-06-15", "2024-05-22");
INSERT INTO reservas (nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES ("Carlos", "carlos@fi.uba.ar", "deluxe", 2, "2024-06-16", "2024-06-23");
INSERT INTO reservas (nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES ("Juan", "juanP@fi.uba.ar", "normal", 1, "2024-06-18", "2024-06-22");
INSERT INTO reservas (nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES ("Fabricio", "fabricio@fi.uba.ar", "premium", 3, "2024-06-19", "2024-06-24");
INSERT INTO reservas (nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES ("Valentin", "valentin@fi.uba.ar", "normal", 5, "2024-06-19", "2024-06-25");
INSERT INTO reservas (nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES ("Julieta", "julieta@fi.uba.ar", "premium", 3, "2024-06-20", "2024-06-25");
INSERT INTO reservas (nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES ("Florencia", "florencia@fi.uba.ar", "normal", 4, "2024-06-21", "2024-06-28");


/* Agregamos datos a la tabla reservas diarias*/
/* Dias de reserva numero 1 */ 
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (1, "2024-06-15", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (1, "2024-06-16", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (1, "2024-06-17", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (1, "2024-06-18", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (1, "2024-06-19", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (1, "2024-06-20", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (1, "2024-06-21", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (1, "2024-06-22", "normal");
/* Dias de reserva numero 2 */
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (2, "2024-06-16", "deluxe");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (2, "2024-06-17", "deluxe");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (2, "2024-06-18", "deluxe");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (2, "2024-06-19", "deluxe");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (2, "2024-06-20", "deluxe");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (2, "2024-06-21", "deluxe");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (2, "2024-06-22", "deluxe");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (2, "2024-06-23", "deluxe");
/* Dias de reserva numero 3 */
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (3, "2024-06-18", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (3, "2024-06-19", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (3, "2024-06-20", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (3, "2024-06-21", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (3, "2024-06-22", "normal");
/* Dias de reserva numero 4 */
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (4, "2024-06-19", "premium");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (4, "2024-06-20", "premium");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (4, "2024-06-21", "premium");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (4, "2024-06-22", "premium");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (4, "2024-06-23", "premium");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (4, "2024-06-24", "premium");
/* Dias de reserva numero 5 */
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (5, "2024-06-19", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (5, "2024-06-20", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (5, "2024-06-21", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (5, "2024-06-22", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (5, "2024-06-23", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (5, "2024-06-24", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (5, "2024-06-25", "normal");
/* Dias de reserva numero 6 */
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (6, "2024-06-20", "premium");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (6, "2024-06-21", "premium");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (6, "2024-06-22", "premium");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (6, "2024-06-23", "premium");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (6, "2024-06-24", "premium");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (6, "2024-06-25", "premium");
/* Dias de reserva numero 7 */
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (7, "2024-06-21", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (7, "2024-06-22", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (7, "2024-06-23", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (7, "2024-06-24", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (7, "2024-06-25", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (7, "2024-06-26", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (7, "2024-06-27", "normal");
INSERT INTO reservas_diarias (numero_reserva, dia, tipo_habitacion) VALUES (7, "2024-06-28", "normal");



/* Agregamos datos a la tabla habitaciones */
INSERT INTO habitaciones (tipo_habitacion, cantidad_total) VALUES ("normal", 10);
INSERT INTO habitaciones (tipo_habitacion, cantidad_total) VALUES ("premium", 8);
INSERT INTO habitaciones (tipo_habitacion, cantidad_total) VALUES ("deluxe", 5);

GRANT ALL PRIVILEGES ON tp_database.* TO 'usuario'@'%' IDENTIFIED BY 'scrumbeasts';
FLUSH PRIVILEGES;