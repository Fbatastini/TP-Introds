from sqlalchemy import create_engine


engine = create_engine("mysql+mysqlconnector://root:scrumbeasts@localhost:3309/tp_database")