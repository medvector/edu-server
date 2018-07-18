# EduServer API

This is specification for EduServer API.

API uses REST guidelines and primarily flat structure.

Descriptions for some of object types can be found [here](api/formats.md). 

Some requests have *Required authentication* or *Required authorization* marks. This requests must contain `Authorization`
header with `Bearer` token obtained from server.



## Endpoints

**Common API:**

* `POST /authorize` – Acquire token: *In progress ...*

**Learner API:**

* `GET /courses` — Get all courses: *In progress ...*
* `GET /courses/<pk>/materials` — Get all course materials: *In progress ...*
* `GET /courses/<pk>/structure` — Get structure of the course: *In progress ...*

* `GET /section/<pk>` — Get single section: *In progress ...*
* `GET /lesson/<pk>` — Get single lesson: *In progress ...*
* `GET /task/<pk>` — Get single task: *In progress ...*

* `GET /comments/<pk>` — Get all comments for `<pk>` study item: *In progress ...*
* `POST /comments/<pk>` — Send comment for `<pk>` study item: *In progress ...*

**Educator API:**

* `GET /courses/mine` — Get all courses available for editing: *In progress ...*
* `GET /courses/<pk>/full` — Get editing materials for this course: *In progress ...*

* `POST /courses` — Create new course: [details](api/post_courses.md)
* `PUT /courses/<pk>/current` — Upload current version of the course: [details](api/put_courses_pk_current.md)

