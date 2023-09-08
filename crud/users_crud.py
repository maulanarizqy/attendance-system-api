from sqlalchemy.orm import Session
import models, schemas


# CRUD Users

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).filter(models.User.status == "active").first()


def get_user_by_username(db: Session, username: int):
  return db.query(models.User).filter(models.User.username == username).filter(models.User.status == "active").first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).filter(models.User.status == "active").order_by(models.User.id.asc()).offset(skip).limit(limit).all()


def create_user(db: Session, user = schemas.UserCreate):
  # fake_hashed_password = user.password + "itisnothashed"
  db_user = models.User(
    name = user.name,
    username = user.username, 
    password = user.password,
    role = user.role,
    status = "active"
    )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


def update_user(db: Session, user = schemas.UserUpdate, user_id = int):
  data_user = user.dict(exclude_unset=True)

  # if user.password is not None:
  #   fake_hashed_password = user.password + "itisnothashed"

  #   data_user.update({"password": fake_hashed_password})
    
  data_query = db.query(models.User).filter(models.User.id == user_id)
  db_user = data_query.first()

  data_query.update(data_user, synchronize_session=False)

  db.commit()
  db.refresh(db_user)
  return db_user


def delete_user(db: Session, user_id: int):
  data_user = {"status": "deleted"}
  data_query = db.query(models.User).filter(models.User.id == user_id)

  data_query.update(data_user, synchronize_session=False)

  db.commit()
  return {"detail": "User deleted successfully"}
