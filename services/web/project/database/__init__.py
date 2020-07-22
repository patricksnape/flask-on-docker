from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class BaseModel:
    def __repr__(self):
        columns = {i.name: getattr(self, i.name) for i in self.__table__.columns}
        columns_str = ", ".join(f"{k}={v}" for k, v in columns.items())
        return f"{self.__class__.__name__}({columns_str})"
