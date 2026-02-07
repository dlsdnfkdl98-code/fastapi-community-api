# Simple Community API (FastAPI + MySQL + JWT)

FastAPI 기반의 간단한 커뮤니티 백엔드 API입니다.
Docker Compose로 API 서버와 MySQL을 함께 실행하며, JWT 인증(회원가입/로그인/보호 API)을 구현했습니다.

## Tech Stack

- Python, FastAPI
- SQLAlchemy, PyMySQL
- MySQL 8.0 (Docker)
- JWT (python-jose)
- Password Hashing (bcrypt via passlib)
- Docker / Docker Compose

## Features

- 회원가입: `POST /auth/signup`
  - 이메일 중복 체크(409)
  - bcrypt로 비밀번호 해싱 저장
- 로그인: `POST /auth/login`
  - JWT access token 발급
- 인증/인가: `GET /me`
  - Bearer 토큰 기반 인증이 필요한 보호 API

## Project Structure

## Why This Project?

백엔드 개발자로서 인증(JWT), 보안(bcrypt), 컨테이너 기반 실행 환경(Docker)을
직접 구현해보기 위해 만든 학습/포트폴리오 프로젝트입니다.
