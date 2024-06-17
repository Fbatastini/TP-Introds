# TP-Introds
## Trabajo Practico Introducción al desarrollo de software
### Integrantes

| Nombre | Padrón |
| --- | --- |
| Fabricio Agustin Batastini | 111828 |
| Marlon Stiven Molina Buitrago | 112018 |
| Juan Ignacio Moore | 112479 |
| Manuel Peñalva | 111696 |
| Thiago Pla | 112461 |
| Ulises Valentín Tripaldi | 111919 |
| Máximo Augusto Calderón Vasil | 111810 | 

### Correr el proyecto haciendo uso de archivo "init.sh" 🐧
> [!WARNING]
> Tener docker abierto (desktop o de terminal).

**Ejecutar el comando:**
  ```
  bash init.sh
 ```

> [!NOTE]
>Estará disponible en el localhost:5000

Para más información de Docker, visitar su [documentación](https://docs.docker.com/manuals/).

### Sin uso de docker 🐍
Es necesario crear un entorno virtual e instalar las dependencias necesarias para el proyecto si no se usa Docker.
> [!TIP]
> **Recomendado**
1. Crear un entorno virtual:
    ```sh
    python3 -m venv .venv
    ```
2. Instalar dependencias utilizando pipenv:
    ```sh
    pipenv install -r requirements.txt
    ```

### Correr proyecto (dos terminales) 🚀 
Terminal 1:
```
flask run --debug
```
Terminal 2:
```
export FLASK_APP=api.py
flask run --port 5001
```

Para más información de Flask, visitar su [documentación](https://flask.palletsprojects.com/).



### **Hecho por ScrumBeasts**
<img src="https://cdn.discordapp.com/attachments/1244366941003583572/1244368858467536917/OIG4.png?ex=666e918f&is=666d400f&hm=871f5da6c18690ee4e785ebed79862264421edd96ecccbca122db933a9d17b93&" alt="ScrumBeasts Logo" width="200"/>
