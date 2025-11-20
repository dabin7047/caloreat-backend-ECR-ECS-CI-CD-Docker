from app.schemas.user import UserCreate, UserUpdate
# from app.core.security import hash_password # security.py 파일 만든뒤 활성화
from app.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import select


# email로 유저 조회
def get_user_by_email(db: Session, email: str):
    return db.scalar(select(User).where(User.email == email)) 
    # scalar(select(...)) -> 결과 중 첫 번째(row 1개)를 가져오는 SQLAlchemy 방식
    # DB : SELECT * FROM users WHERE email=:email LIMIT 1

# id(PK)로 유저 조회
def get_user_by_id(db: Session, id: int):
    return db.get(User, id)
    # db.get(Model, pk) -> pk기반 조회(가장 빠르고 기본적인 조회 방식)

# 회원가입 (비밀번호 해시 후 저장)
def create_user(db: Session, user_in: UserCreate):
    hashed_pw = user_in.password                  # 지금은 security.py파일이 없어 임시로 쓴다.
    # hashed_pw = hash_password(user_in.password) # 만약에 security.py을 만든다면 이 코드를 쓴다.

    user = User(
        email=user_in.email,         # unique + NOT NULL
        username=user_in.username,   # unique + NOT NULL
        password_hash=hashed_pw,     # hash값 저장해야 함 (추후 security적용 해야함)
        phone=user_in.phone,
        nickname=user_in.nickname,
        provider=user_in.provider    # 기본값 Email / 소셜 로그인도 가능
    )

    db.add(user)     # 세션에 저장 예약 (INSERT 준비)
    db.commit()      # 실제 DB 반영 (commit 해야 INSERT 실행)
    db.refresh(user) # commit 이후 생성된 id, create_at, ...값 불러오려면 refresh 필수

    return user

# 회원정보 수정 (PATCH 방식)
def update_user(db: Session, db_user: User, user_in: UserUpdate):
    update_data = user_in.model_dump(exclude_unset=True)
    # exclude_unset=True -> 사용자가 보낸 값만 추출 (부분 수정 가능)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()         # 변경내용을 DB에 반영
    db.refresh(db_user) # 갱신된 객체 다시 읽어오기 (DB 최신 상태)
    return db_user

# 회원 삭제
def delete_user(db: Session, db_user: User):
    db.delete(db_user)  # 세션에서 해당 객체 삭제 처리
    db.commit()         # DB에서 실제 삭제 실행