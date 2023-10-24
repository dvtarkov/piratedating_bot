from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///pirate_dating.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    chat_id = Column(Integer)
    profile_picture = Column(String(255))
    has_profile = Column(Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'


Base.metadata.create_all(engine)


