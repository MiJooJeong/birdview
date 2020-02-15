# Docker로 로컬 postgreSQL DB 설정하기

```shell script
docker run --rm --name birdview-project -e POSTGRES_PASSWORD=birdview -d -p 5432:5432 -v ~/docker/volumes/postgres/birdview-project:/var/lib/postgresql/datva postgres:10.6
```