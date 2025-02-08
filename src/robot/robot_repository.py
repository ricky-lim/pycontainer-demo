from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select


class Robot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str


class RobotRepository:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)

    def init_db(self):
        SQLModel.metadata.create_all(self.engine)

    def add_robot(self, name: str, description: str) -> int:
        robot = Robot(name=name, description=description)
        with Session(self.engine) as session:
            session.add(robot)
            session.commit()
            session.refresh(robot)
            return robot.id

    def get_robot_by_id(self, robot_id: int) -> Robot:
        with Session(self.engine) as session:
            return session.get(Robot, robot_id)

    def get_robot_by_name(self, name: str) -> Robot:
        with Session(self.engine) as session:
            statement = select(Robot).where(Robot.name == name)
            return session.exec(statement).first()
