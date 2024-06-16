from sqlalchemy import create_engine

# Local dev
# API_URL = 'http://127.0.0.1:5001'
# Docker
API_URL = ' http://api:5001'

# local
# engine = create_engine("mysql+mysqlconnector://root:scrumbeasts@localhost:3309/tp_database")
# docker
engine = create_engine("mysql+mysqlconnector://root:scrumbeasts@db:3306/tp_database")
