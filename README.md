# Simple Community API

FastAPI + MySQL + JWT 기반의 커뮤니티 백엔드 API

FastAPI로 구현한 RESTful API 프로젝트입니다.
Docker Compose를 사용해 API 서버와 MySQL을 함께 실행하며,
JWT 인증을 기반으로 한 회원가입 / 로그인 / 보호 API를 구현했습니다.

---

## Tech Stack

- **Language**: Python 3
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: MySQL 8.0 (Docker)
- **Auth**: JWT (python-jose)
- **Security**: bcrypt (passlib)
- **Infra**: Docker, Docker Compose

---

## Features

### Authentication

- **회원가입** `POST /auth/signup`
  - 이메일 중복 체크 (409 Conflict)
  - bcrypt를 이용한 비밀번호 해싱 저장
- **로그인** `POST /auth/login`
  - JWT Access Token 발급
- **내 정보 조회** `GET /me`
  - Bearer Token 기반 인증이 필요한 보호 API

### Posts (CRUD)

- 게시글 목록 조회
- 게시글 생성 (인증 필요)
- 게시글 단건 조회
- 게시글 수정 (작성자만 가능)
- 게시글 삭제 (작성자만 가능)

---

## API Documentation

- Swagger UI
  👉 <http://localhost:8000/docs>

---

## Project Structure

```text
app/
 ├─ main.py              # FastAPI app & routing
 ├─ config/
 │   └─ db.py            # DB 연결 설정
 ├─ domain/
 │   ├─ user.py          # User ORM 모델
 │   └─ post.py          # Post ORM 모델
 ├─ repository/          # DB 접근 로직
 ├─ service/             # 비즈니스 로직

1. 환경 변수 설정
cp .env.example .env

2. Docker Compose 실행
docker compose up --build

3. 확인

API: http://localhost:8000

Docs: http://localhost:8000/docs
