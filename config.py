from sqlalchemy import create_engine

# local
# engine = create_engine("mysql+mysqlconnector://root:scrumbeasts@localhost:3309/tp_database")

# docker
engine = create_engine("mysql+mysqlconnector://root:scrumbeasts@db:3306/tp_database")