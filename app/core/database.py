from sqlalchemy import inspect, text
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL : str = 'sqlite:///database.db'

connect_args : dict = {'check_same_thread' : False}

engine = create_engine(DATABASE_URL,connect_args=connect_args)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
    if 'car' in inspect(engine).get_table_names() and 'daily_price' not in {column['name'] for column in inspect(engine).get_columns('car')}:
        with engine.begin() as connection:
            connection.execute(text('ALTER TABLE car ADD COLUMN daily_price NUMERIC DEFAULT 0'))

def get_session():
    with Session(engine) as session:
        yield session