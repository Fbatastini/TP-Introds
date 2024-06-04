CREATE TABLE reservas (
    numero_reserva INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    mail VARCHAR(120) NOT NULL,
    tipo_habitacion VARCHAR(10) NOT NULL,
    cantidad_personas INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE NOT NULL
);

CREATE TABLE habitaciones (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tipo_habitacion VARCHAR(10) NOT NULL,
    cantidad_total INT NOT NULL
);

/* Agregamos datos a la tabla reservas */
INSERT INTO reservas (numero_reserva, nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES (1, "Manuel", "manuel@fi.uba.ar", "normal", 4, "2024-05-29", "2024-05-31");
INSERT INTO reservas (numero_reserva, nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES (2, "Carlos", "carlos@fi.uba.ar", "deluxe", 2, "2024-05-30", "2024-06-05");
INSERT INTO reservas (numero_reserva, nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES (3, "Juan", "juanP@fi.uba.ar", "normal", 1, "2024-05-31", "2024-06-04");
INSERT INTO reservas (numero_reserva, nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES (4, "Fabricio", "fabricio@fi.uba.ar", "premium", 3, "2024-06-01", "2024-06-04");
INSERT INTO reservas (numero_reserva, nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES (5, "Valentin", "valentin@fi.uba.ar", "normal", 5, "2024-06-02", "2024-06-05");
INSERT INTO reservas (numero_reserva, nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES (6, "Julieta", "julieta@fi.uba.ar", "premium", 3, "2024-06-03", "2024-06-08");
INSERT INTO reservas (numero_reserva, nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES (7, "Florencia", "florencia@fi.uba.ar", "normal", 4, "2024-06-04", "2024-06-10");
INSERT INTO reservas (numero_reserva, nombre, mail, tipo_habitacion, cantidad_personas, fecha_ingreso, fecha_salida) VALUES (8, "Carla", "carla@fi.uba.ar", "deluxe", 2, "2024-06-04", "2024-06-09");

/* Agregamos datos a la tabla habitaciones */
INSERT INTO habitaciones (tipo_habitacion, cantidad_total) VALUES ("normal", 10);
INSERT INTO habitaciones (tipo_habitacion, cantidad_total) VALUES ("premium", 8);
INSERT INTO habitaciones (tipo_habitacion, cantidad_total) VALUES ("deluxe", 5);