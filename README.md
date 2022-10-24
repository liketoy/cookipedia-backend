# COOKIPEDIA

## 설명

내가 가지고 있는 재료들로 만들 수 있는 레시피를 추천받는 서비스

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

### 👩‍🍳👨‍🍳네번째 할 일(2022.10.24까지)

- [x] api 만들기([링크참조](https://github.com/orgs/liketoy/teams/cookipedia/discussions/4))

### 👩‍🍳👨‍🍳다섯번째 할 일(2022.10.31까지)

- [ ] ingredient db 웹스크랩핑([링크참조](https://sauce.foodpolis.kr/home/specialty/foodDbSearch.do?PAGE_MN_ID=SIS-030101))
- [ ] food db 웹스크랩핑

## 새로운 할 일을 시작하기 전 필독 사항

⚠️ 마지막 작업한 branch를 지우고, 새로운 branch로 시작할 것. 아래 코드 참고

```console
$ git checkout develop
$ git branch -D [삭제할 branch 이름] ([]는 빼고 작성)
$ git push origin --delete [삭제할 원격저장소 branch 이름] ([]는 빼고 작성)
$ git pull origin develop
$ git checkout -b [새로 만들 branch 이름] ([]는 빼고 작성)

# 만약, pull 해 올 branch에 model을 수정한 이슈가 있다면
$ rm db.sqlite3
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```
