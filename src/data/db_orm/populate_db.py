from sqlalchemy import text

from src.application.crypt.crypt_service import CryptService
from src.data.db_orm.query_obj import create_writing_session


def add_tbl_users() -> list:
    commands = [
        text(text=f"""insert into tbl_users (username, name, password) values ('john.doe', 'john doe', '{CryptService.encrypt('123')}');"""),
    ]
    return commands


def populate_db():
    try:
        with create_writing_session() as session:
            commands = []
            commands.extend(add_tbl_users())

            for command in commands:
                session.execute(command)
            session.commit()
    except:
        ...
