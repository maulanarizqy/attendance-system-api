from sqlalchemy.orm import Session
import models, schemas


# CRUD Participants

def get_participant(db: Session, participant_id: int):
  return db.query(models.Participant).filter(models.Participant.id == participant_id).first()


def get_participants(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Participant).order_by(models.Participant.id.asc())\
                                     .offset(skip).limit(limit).all()


# def get_participants_by_course_id(db: Session, course_id: int, skip: int = 0, limit: int = 100):
#   return db.query(models.Participant).filter(models.Participant.status == "active")\
#                                      .filter(models.Participant.course_id == course_id)\
#                                      .order_by(models.Participant.id.asc())\
#                                      .offset(skip).limit(limit).all()


def get_participants_by_course_tag(db: Session, course_tag: int, skip: int = 0, limit: int = 100):
  return db.query(models.Participant).filter(models.Participant.status == "active",
                                             models.Participant.course_tag == course_tag)\
                                     .order_by(models.Participant.id.asc())\
                                     .offset(skip).limit(limit).all()


def get_participants_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
  return db.query(models.Participant).filter(models.Participant.status == "active",
                                             models.Participant.user_id == user_id)\
                                    .order_by(models.Participant.id.asc())\
                                    .offset(skip).limit(limit).all()


def create_participant(db: Session, participant = schemas.ParticipantCreate):
  db_participant = models.Participant(
    course_tag = participant.course_tag,
    user_id = participant.user_id,
    status = "active"
    )
  db.add(db_participant)
  db.commit()
  db.refresh(db_participant)
  return db_participant


def update_participant(db: Session, participant = schemas.ParticipantUpdate, participant_id = int):
  data_participant = participant.dict(exclude_unset=True)
    
  data_query = db.query(models.Participant).filter(models.Participant.id == participant_id)\
                                           .filter(models.Participant.status == "active")
  db_participant = data_query.first()

  data_query.update(data_participant, synchronize_session=False)

  db.commit()
  db.refresh(db_participant)
  return db_participant


def delete_participant(db: Session, participant_id: int):
  data_participant = {"status": "inactive"}
  data_query = db.query(models.Participant).filter(models.Participant.id == participant_id)

  data_query.update(data_participant, synchronize_session=False)

  db.commit()
  return {"detail": "Participant deleted successfully"}
