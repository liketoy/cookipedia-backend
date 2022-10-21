# COOKIPEDIA

## 설명

재료를 검색하면 그에 맞는 자취생 요리를 레시피와 함께 보여주는 사이트

## 부가기능

- 커뮤니티
- 공동구매
- 레시피위키

### 👩‍🍳👨‍🍳첫번째 할 일(2022.10.03까지)

- [x] DB 설계(우선 부가기능 제외하고 설계)
- [x] app 생성 후 models.py 작성

### 👩‍🍳👨‍🍳두번째 할 일(2022.10.10까지)

- [x] 코드 리뷰 받은 것을 토대로 새로운 branch에 push 하고 PR 요청하기

### 👩‍🍳👨‍🍳세번째 할 일(2022.10.17까지)

- [x] admin 페이지 만들기([링크참조](https://github.com/orgs/liketoy/teams/cookipedia/discussions/3))

## 새로운 할 일을 시작하기 전 필독 사항

⚠️ 마지막 작업한 branch를 지우고, 새로운 branch로 시작할 것. 아래 코드 참고

```console
$ git checkout develop
$ git branch -D [삭제할 branch 이름] ([]는 빼고 작성)
$ git pull origin develop
$ git checkout -b feature/admin/[본인 이름] ([]는 빼고 작성)
$ rm db.sqlite3
```
