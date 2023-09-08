from sqlalchemy.orm import Session
import models, schemas


# CRUD Logs

def get_log(db: Session, log_id: int):
  return db.query(models.Log).filter(models.Log.id == log_id).first()


def get_logs(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Log).order_by(models.Log.id.asc()).offset(skip).limit(limit).all()


def get_logs_by_course_id(db: Session, course_id: int, skip: int = 0, limit: int = 100):
  log_query = db.query(models.Log).filter(models.Log.course_id == course_id)\
                                  .order_by(models.Log.id.asc()).offset(skip).limit(limit).all()
  return log_query


def get_log_by_course_and_user(db: Session, course_id: int, user_id: int):
  return db.query(models.Log).filter(models.Log.course_id == course_id)\
                             .filter(models.Log.user_id == user_id).first()


def create_log(db: Session, log = schemas.LogCreate):
  db_log = models.Log(
    course_id = log.course_id,
    user_id = log.user_id
    )
  db.add(db_log)
  db.commit()
  db.refresh(db_log)
  return db_log


def record_log(db: Session, log = schemas.LogRecord, log_id = int):
  # data_log = log.dict(exclude_unset=True)
    
  data_query = db.query(models.Log).filter(models.Log.id == log_id)
  db_log = data_query.first()

  data_query.update(log, synchronize_session=False)

  db.commit()
  db.refresh(db_log)
  return db_log


def approve_log(db: Session, log = schemas.LogApprove, log_id = int):
  # data_log = log.dict(exclude_unset=True)
    
  data_query = db.query(models.Log).filter(models.Log.id == log_id)
  db_log = data_query.first()

  data_query.update(log, synchronize_session=False)

  db.commit()
  db.refresh(db_log)
  return db_log


# def delete_log(db: Session, log_id: int):
#   data_log = {"status": "deleted"}
#   data_query = db.query(models.Log).filter(models.Log.id == log_id)

#   data_query.update(data_log, synchronize_session=False)

#   db.commit()
#   return {"detail": "Log deleted successfully"}
