CREATE TABLE reservas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    numero_habitacion INT NOT NULL,
    huespedes INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    cantidad_noches INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    mail VARCHAR(120) NOT NULL
);

CREATE TABLE habitaciones (
    numero INT NOT NULL PRIMARY KEY,
    precio INT NOT NULL,
    capacidad INT NOT NULL,
    descripcion VARCHAR(500),
    promocion VARCHAR(100)
);

CREATE TABLE usuarios (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(30) NOT NULL,
    clave VARCHAR(20) NOT NULL
);

CREATE TABLE contactos (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    mail VARCHAR(120) NOT NULL,
    asunto VARCHAR(30) NOT NULL,
    mensaje VARCHAR(750) NOT NULL 
);

/* Agrego datos a tabla usuarios */ 
INSERT INTO usuarios (usuario, clave) VALUES ("admin1", "1234");
INSERT INTO usuarios (usuario, clave) VALUES ("admin2", "5678");


SET PASSWORD FOR 'usuario'@'%' = 'scrumbeasts';
FLUSH PRIVILEGES;