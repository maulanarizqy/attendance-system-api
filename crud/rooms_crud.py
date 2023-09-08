from sqlalchemy.orm import Session
import models, schemas


# CRUD Rooms

def get_room(db: Session, room_id: int):
  return db.query(models.Room).filter(models.Room.id == room_id).first()


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Room).order_by(models.Room.id.asc()).offset(skip).limit(limit).all()


def get_room_by_room_name(db: Session, room: schemas.RoomSearch):
  room_query = db.query(models.Room).filter(models.Room.building == room.building)\
                                    .filter(models.Room.floor == room.floor)\
                                    .filter(models.Room.room_name == room.room_name)\
                                    .first()
  return room_query


def create_room(db: Session, room = schemas.RoomCreate):
  db_room = models.Room(
    building = room.building,
    floor = room.floor,
    room_name = room.room_name,
    capacity = room.capacity,
    status = "available"
    )
  db.add(db_room)
  db.commit()
  db.refresh(db_room)
  return db_room


def update_room(db: Session, room = schemas.RoomUpdate, room_id = int):
  data_room = room.dict(exclude_unset=True)
    
  data_query = db.query(models.Room).filter(models.Room.id == room_id)
  db_room = data_query.first()

  data_query.update(data_room, synchronize_session=False)

  db.commit()
  db.refresh(db_room)
  return db_room


def delete_room(db: Session, room_id: int):
  data_room = {"status": "deleted"}
  data_query = db.query(models.Room).filter(models.Room.id == room_id)

  data_query.update(data_room, synchronize_session=False)

  db.commit()
  return {"detail": "Room deleted successfully"}
