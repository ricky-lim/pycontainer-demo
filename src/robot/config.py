class DatabaseConfig:
    def __init__(
        self,
        user: str = "postgres",
        password: str = "postgres",
        host: str = "localhost",
        port: str = "5432",
        db: str = "postgres",
    ):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    def __str__(self) -> str:
        return self.database_url
