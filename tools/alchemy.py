from typing import List
import sqlalchemy, os

def sclite_engine(path: str, autocommit: bool = True) -> sqlalchemy.engine.base.Engine:
    path = path.strip('\\').strip('/')

    if not os.path.exists(path): 
        open(path, 'w+').close()

    eng = sqlalchemy.create_engine(
        f"sqlite:///{path}",
        isolation_level = "AUTOCOMMIT" if autocommit else None
    )
    return eng