### PaperApp

|func.|description|input|output|note|
|---|---|---|---|---|
|get_paper|논문 1개의 세부 정보를 조회|paper_id|Paper|댓글 세부 정보 또한 가져와야 함|
|get_paper_list|모든 논문을 최신순으로 조회|limit, offset|Papers|정렬 기능을 추후에 구현할 수 있음|
|get_paper_list|저자 1명의 등록된 논문을 최신순으로 조회|limit, offset, author|Papers|@overriding|
|create_paper|논문 1개를 등록|keyword, access_token||구글 스칼라를 크롤링 하여 맨 위의 검색 결과를 파싱함|
|delete_paper|논문 1개를 삭제|paper_id, access_token||admin만 삭제 가능하도록 구현할 수도 있음|

### CommentApp

|func.|description|input|output|note|
|---|---|---|---|---|
|get_comment_list|논문 1개의 모든 댓글을 최신순으로 조회|paper_id, limit, offset|Comments|정렬 기능을 추후에 구현할 수 있음|
|create_comment|댓글 1개를 등록|paper_id, content, access_token|||
|update_comment|댓글 1개를 변경|comment_id, content, access_token|||
|delete_comment|댓글 1개를 삭제|comment_id, access_token|||

### UserApp

|func.|description|input|output|note|
|---|---|---|---|---|
|get_user|유저 1명의 정보를 조회|access_token|User||
|create_user|계정 생성|username, password, password2, email||추후에는 소셜 로그인 구현할 지 고민중|
|delete_user|계정 삭제|access_token|||
|login|로그인|username, password|access_token, refresh_token|token을 어디에 저장할 지 고민 필요|
|logout|로그아웃|access_token||해당 유저의 refresh token 제거|
|authenticate|access token의 유효 여부 검사|access_token|||
|update_refresh_token|refresh token 갱신|refresh_token||refresh token은 Redis에 따로 저장|
|update_password|유저 1명의 비밀번호 변경|access_token, prev_password, new_password||CSRF를 방지하기 위한 prev_password 추가|

### ProfileApp

|func.|description|input|output|note|
|---|---|---|---|---|
|get_profile|유저 1명의 프로필 정보 조회|user_id|Profile||
|update_profile_image|유저 1명의 프로필 이미지 갱신|image, access_token||AWS S3에 이미지 저장, DB에는 URI 저장|
|update_profile_message|유저 1명의 프로필 메시지 갱신|message, access_token|||

### Paper, Comment - LikeApp, DislikeApp (생략)

|func.|description|input|output|note|
|---|---|---|---|---|
|create_like|좋아요 추가|paper_id, access_token||싫어요가 추가되어 있었으면 제거하고 좋아요 추가|
|delete_like|좋아요 취소|paper_id, access_token|||
|update_total_like|전체 좋아요 컬럼을 실제 값으로 갱신|access_token||admin만 사용 가능해야함, 추후 airflow로 구현 예정|
|get_paper_list|유저 1명이 좋아요한 모든 논문을 최신순으로 조회|user_id, limit, offset|Papers||