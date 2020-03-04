# 버드뷰 API 설계 과제 

- AWS Lambda, AWS API Gateway를 통해 서버리스 방식으로 구현
- sample 데이터 파일(.json)을 RDS에 업로드하여 구성

## 주요 사용 기술
- [Django REST framework](https://www.django-rest-framework.org/)
- [zappa](https://github.com/Miserlou/Zappa)
  - python serverless framework

## Docker로 로컬 postgreSQL DB 설정하기

```shell script
docker run --rm --name birdview-project -e POSTGRES_PASSWORD=birdview -d -p 5432:5432 -v ~/docker/volumes/postgres/birdview-project:/var/lib/postgresql/data postgres:10.6
```

## 참고 링크
- 프로젝트 관련 스터디 문서 링크 : https://www.notion.so/BirdView-708bc35c381e4072b4d0c6de8294be59