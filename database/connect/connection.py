import os
from dotenv import load_dotenv
# sqlalchemy : ORM 라이브러리
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = (
  f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
  f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# create_engine: DB 연결을 생성한다. application.yml과 동일한 역할
## URL : Database URL
## pool_pre_ping : DB 연결이 끊겼을 때, 자동으로 감지하고 재연결 수행
## connect_args : 연결 시 추가적인 옵션을 설정한다. timezone과 search_path를 설정한다.
engine = create_engine(
	DATABASE_URL,
	pool_pre_ping=True,
	connect_args={"options": "-c timezone=Asia/Seoul -c search_path=design"},
)

# Python에서는 각 요청마다 세션을 생성하고, 요청이 끝나면 세션을 종료한다.
SessionLocal = sessionmaker(
	autocommit=False, 
	autoflush=False, 
	bind=engine
)