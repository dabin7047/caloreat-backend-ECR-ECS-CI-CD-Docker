from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.settings import settings

# 비동기엔진 
async_engine = create_async_engine(settings.database_url, echo=False)

# 비동기엔진 세션연결
AsyncSessionLocal = sessionmaker(
    autocommit = False, autoflush=False, bind=async_engine, class_=AsyncSession
)
# 동기 엔진 (필요시)

# Base
Base=declarative_base()


# get_db 
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback() # 오류 발생 시 DB 작업취소 transaction
            raise                # 오류 발생 표시

#DB연결 경로 확인 (dev) -삭제예정
print("DB URL:", settings.database_url)


#middleware 추가여부