from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import extract
import models, schemas


# CRUD Courses

def get_course(db: Session, course_id: int):
  return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Course).order_by(models.Course.id.asc()).offset(skip).limit(limit).all()


def get_course_by_tag(db: Session, course_tag: int):
  return db.query(models.Course).filter(models.Course.course_tag == course_tag).order_by(models.Course.id.asc()).limit(20).all()


def get_courses_by_date(db: Session, date: date, skip: int = 0, limit: int = 100):
  return db.query(models.Course).filter(extract('year', models.Course.start_time) == date.year,
                                        extract('month', models.Course.start_time) == date.month,
                                        extract('day', models.Course.start_time) == date.day)\
                                        .order_by(models.Course.id.asc())\
                                        .offset(skip).limit(limit).all()


def create_course(db: Session, session_number: int, course_tag: int, secret_key: str, course = schemas.CourseCreate):
  db_course = models.Course(
    course_name = course.course_name,
    start_time = course.start_time,
    duration_in_minutes = course.duration_in_minutes,
    session_number = session_number,
    course_tag = course_tag,
    secret_key = secret_key,
    status = "active"
    )
  db.add(db_course)
  db.commit()
  db.refresh(db_course)
  return db_course


def update_course(db: Session, course = schemas.CourseUpdate, course_id = int):
  data_course = course.dict(exclude_unset=True)
    
  data_query = db.query(models.Course).filter(models.Course.id == course_id)
  db_course = data_query.first()

  data_query.update(data_course, synchronize_session=False)

  db.commit()
  db.refresh(db_course)
  return db_course


def assign_lecturer_course(db: Session, lecturer_id: int, course_tag: int):
  data_course = {"lecturer_id": lecturer_id}
  data_query = db.query(models.Course).filter(models.Course.course_tag == course_tag)
  db_course = data_query.all()


  data_query.update(data_course, synchronize_session=False)

  db.commit()
  return db_course


def set_course_room(db: Session, room_id: int, course_tag: int):
  data_course = {"room_id": room_id}
  data_query = db.query(models.Course).filter(models.Course.course_tag == course_tag)
  db_course = data_query.all()


  data_query.update(data_course, synchronize_session=False)

  db.commit()
  return db_course


def delete_course(db: Session, course_id: int):
  data_course = {"status": "deleted"}
  data_query = db.query(models.Course).filter(models.Course.id == course_id)

  data_query.update(data_course, synchronize_session=False)

  db.commit()
  return {"detail": "Course deleted successfully"}
