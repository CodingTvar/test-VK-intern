**Описание запуска:
Как запустить сервер описан в файле README.md корневого каталога.


**Примеры использования API:
http://127.0.0.1:8000/api/v1/auth/signup/ POST - зарегистрировать пользователя

![[Pasted image 20230511020331.png]]
<br>

http://127.0.0.1:8000/api/v1/users/ GET, POST, PUTCH, DELETE- пользователи

![[Pasted image 20230511021419.png]]
<br>

http://127.0.0.1:8000/api/v1/users/user-id/ GET, POST, PUTCH, DELETE - конкретный пользователь

![[Pasted image 20230511021522.png]]
<br>

http://127.0.0.1:8000/api/v1/profiles/ GET, PUTCH, DELETE - профили пользователей

![[Pasted image 20230511021625.png]]
<br>

http://127.0.0.1:8000/api/v1/profiles/profile-id/friends/ GET - друзья конкретного пользователя

<br>
http://127.0.0.1:8000/api/v1/profiles/profile-id/friends/friend-id/ GET, DELETE - друг конкретного пользователя и его удаление

<br>
http://127.0.0.1:8000/api/v1/profiles/profile-id/users/user-id/send-request/ POST - отправить заявку в друзья

![[Pasted image 20230511023354.png]]
<br>

http://127.0.0.1:8000/api/v1/profiles/profile-id/users/user-id/status-friend/ GET - получить пользователю статус дружбы с другим пользователем

<br>

http://127.0.0.1:8000/api/v1/profiles/profile-id/send_requests/ GET - посмотреть исходящие заявки

![[Pasted image 20230511023743.png]]
<br>

http://127.0.0.1:8000/api/v1/profiles/profile-id/incoming_requests/ GET - посмотреть входящие заявки

![[Pasted image 20230511023814.png]]
<br>

http://127.0.0.1:8000/api/v1/profiles/profile-id/incoming_requests/request-id/accept_request/ POST - принять заявку в друзья от другого пользователя

![[Pasted image 20230511024706.png]]
<br>
<br>
http://127.0.0.1:8000/api/v1/profiles/profile-id/incoming_requests/request-id/accept_request/ PATCH - отклонить заявку в друзья от другого пользователя

![[Pasted image 20230511024957.png]]
<br>

 - если заявки отправлены друг другу, то добавляются в друзья автоматически