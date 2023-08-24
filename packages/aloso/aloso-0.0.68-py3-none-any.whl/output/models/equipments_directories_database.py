import logging

from sqlalchemy import Column, Integer, String, ForeignKey, inspect
from sqlalchemy.orm import sessionmaker, relationship

from domain.equipments_directories import EquipmentsDirectories
from output.database.database_base import Base, engine


class EquipmentsDirectoriesData(Base, EquipmentsDirectories):
    __tablename__ = "EquipmentsDir"

    id = Column(Integer, primary_key=True)
    frequency = Column(Integer, default=1)
    name_equipment_directory = Column(String(50))
    directory_path = Column(String(50), default="")
    server_host = Column(String(50), default="")
    server_user = Column(String(50), default="")

    @staticmethod
    def get_all():
        try:
            with sessionmaker(bind=engine)() as session:
                data = session.query(EquipmentsDirectoriesData).all()
                json_all_directories = {}
                for equipment_dir in data:
                    json_all_directories[equipment_dir.id] = {
                        "id": equipment_dir.id,
                        "name_equipment_directory": equipment_dir.name_equipment_directory,
                        "directory_path": equipment_dir.directory_path,
                        "server_host": equipment_dir.server_host,
                        "server_user": equipment_dir.server_user,
                        "frequency": equipment_dir.frequency}
                return json_all_directories
        except Exception as e:
            logging.error(e)

    @staticmethod
    def get_equipment_by_id(id_equipment):
        try:
            with sessionmaker(bind=engine)() as session:
                return session.query(EquipmentsDirectoriesData).filter(
                    EquipmentsDirectoriesData.id == id_equipment).first()
        except Exception as e:
            logging.error(e)

    def create(self):
        try:
            with sessionmaker(bind=engine)() as session:
                session.add(self)
                session.commit()
                logging.info("Equipment Directories database : create : ok")
                return True
        except Exception as e:
            logging.error(e)
            return False

    def update(self):
        try:
            with sessionmaker(bind=engine)() as session:
                session.merge(self)
                session.commit()
                logging.info("Equipment Directories database : update : ok")
                return True
        except Exception as e:
            logging.error(e)
            return False

    def delete(self):
        try:
            with sessionmaker(bind=engine)() as session:
                session.delete(self.get_equipment_by_id(self.id))
                session.commit()
                logging.info("Equipment Directories database : delete : ok")
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    inspector = inspect(engine.connect())
    print(inspector.get_table_names())
    equipment_dir_table = inspector.get_columns('EquipmentsDir')
    print("\033[1m\033[32mEquipmentsDir\033[0m")
    for column in equipment_dir_table:
        print('\t', column["name"], column["type"])


