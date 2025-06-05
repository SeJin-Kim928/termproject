from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Database 지정
engine = create_engine('sqlite:///classtalk.db')

# ORM 사용
Base = declarative_base()

# User 모델 정의
from classtalk.models import Question, Answer
# 엔진과 연결된 DB에 테이블 생성
Base.metadata.create_all(engine)

# 세션 생성
Session = sessionmaker(bind=engine)
session = Session()

# 새로운 Question 객체 생성
# q1 = Question(subject='텀 프로젝트 계획서에 대한 질문입니다.', content='계획서를 언제까지 작성해야하나요?', create_date=datetime.now())
# q2 = Question(subject='풀스택 개발에 대한 질문입니다.', content='중간고시는 언제입니까?', create_date=datetime.now())

# 세션에 추가하고 커밋
# session.add_all([q3, q]) #하나만 추가할 때는 add
# session.add(q2)
# session.commit()

#query
# item = session.query(Question).filter(Question.id == 3).one()
# item.subject = 'test question!'
# session.add(item)
# print(item.id, item.subject, item.content, item.create_date)
# session.delete(item)
# q = session.query(Question).all()
# print(q)
# session.commit()

for i in range(20):
    q = Question(subject='테스트 데이터입니다:[{i:03d}]', content='내용무', create_date=datetime.now())
    session.add(q)

session.commit()