# TP-Introds
Trabajo Practico Introducción al desarrollo de software

# Base de datos
## Para levantar el contenedor con la base de datos

Entrar al contenedor docker:
```
cd docker
```
Crear el contenedor con docker compose:
```
docker-compose up --build -d
```
Conectarlo a mysql database:
```
docker exec -it database_container mysql -u usuario -p
```
Salir de mysql:
```
exit;
```