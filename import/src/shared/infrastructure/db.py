from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


class DataBase:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = create_async_engine(connection_string, echo=False)
        self.session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    def get_connection(self) -> AsyncSession:
        return self.session()
