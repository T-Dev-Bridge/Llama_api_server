from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database.connect.base import Base

class MarkeDownResult(Base):
  __tablename__ = "markdown_result"
  
  id = Column(Integer, primary_key=True, index=True)
  markdown= Column(String)
  
def create_mark_down_result(db: Session, markdownDto: MarkeDownResult):
  db_mark_down_result = MarkeDownResult(
    markdown = markdownDto.markdown
  )
  db.add(db_mark_down_result)
  db.commit()
  db.refresh(db_mark_down_result)
  return db_mark_down_result

def get_mark_down_result_by_id(db: Session, id: int) -> MarkeDownResult:
    return db.query(MarkeDownResult).filter(MarkeDownResult.id == id)

def update_mark_down_result(db: Session, id: int, markdownDto: MarkeDownResult):
    db_mark_down_result = db.query(MarkeDownResult).filter(MarkeDownResult.id == id).first()
    db_mark_down_result.markdown = markdownDto.markdown
    db.commit()
    db.refresh(db_mark_down_result)
    return db_mark_down_result

def delete_mark_down_result(db: Session, id: int):
    db_mark_down_result = db.query(MarkeDownResult).filter(MarkeDownResult.id == id).first()
    db.delete(db_mark_down_result)
    db.commit()
    return db_mark_down_result
