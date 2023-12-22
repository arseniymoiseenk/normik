from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
class Valentin(Base):
    __tablename__ = 'Valentins_table_olivie'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    lybit_olivie = Column(String)
Base.metadata.create_all(bind = engine)
Session = sessionmaker(bind=engine)
session = Session()
valentinchik1 = Valentin(name='VALentunchik', age=-90, lybit_olivie='KONECHNO ZHE')
valentinchuk2 = Valentin(name='molodoi_valentin', age=786, lybit_olivie='NET')
session.add(valentinchik1)
session.add(valentinchuk2)
session.commit()
valentichiks = session.query(Valentin).all()
for valentin in valentichiks:
    print(f"ID:{valentin.id},valentin_name:{valentin.name},Valentin_age:{valentin.age},olivie?:{valentin.lybit_olivie}")
