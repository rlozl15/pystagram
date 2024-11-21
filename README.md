# PyStagram 프로젝트
이 프로젝트는 이한영의 장고 입문에 실린 PyStagram 프로젝트를 기반으로 한 클론 코딩 프로젝트입니다.
앞선 PyLog 프로젝트에서 학습한 내용을 발전시켜 인증 시스템, Form 클래스, 다대다 DB 구조 등을 다루며 인스타그램의 기본 기능을 구현하였습니다.

## 기간
2024.10.31 ~ 2024.11.04

## 주요 기능
1. 회원 관리
    - 회원가입 및 로그인 기능
    - 사용자 프로필 관리
2. 피드 페이지
    - 전체 피드 페이지 조회 및 단일 피드 페이지 상세 조회
3. 댓글, 해시태그, 좋아요, 팔로잉 기능
    - 댓글 작성 및 삭제
    - 게시물 내 해시태그 추가
    - 좋아요 버튼 및 좋아요 수 관리
    - 사용자 팔로잉 및 팔로우 관리
4. Docker 기반 개발 환경 구성
    - Docker와 Docker Compose를 활용하여 일관된 개발 환경 구성

## 기술 스택
- 백엔드: Django
- 프론트엔드: HTML, CSS, Django 템플릿
- 데이터베이스: Django ORM (SQLite3)
- 컨테이너: Docker

## 설정 및 실행
1. **저장소 클론**
    ```bash
    git clone https://github.com/rlozl15/pystagram.git
    cd pystagram
    ```
2. **Docker 환경 준비**
    - Docker Desktop을 실행합니다.
3. **Docker 이미지 빌드 및 실행**
    ```
    docker-compose up -d --build
    ```
4. **Django 앱 마이그레이션**
    ```
    docker-compose exec django-service python manage.py migrate
    ```
5. **블로그 데이터 임의 추가**
    ```
    docker-compose exec django-service python manage.py loaddata data.json
    ```
  - 기본 계정 데이터
      - username: john_lee
      - password: 0000
6. **Django 서버 확인**
    - http://localhost:8000에서 Django 애플리케이션에 접근할 수 있습니다.
7. **관리자 계정 생성**
    - 필요시 admin 페이지 확인을 위해 superuser를 생성해야 합니다.
    ```
    docker-compose exec django-service python manage.py createsuperuser
    ```  

## 이미지 출처
- 이미지는 [Pixabay](https://pixabay.com/)에서 다운받았습니다.
