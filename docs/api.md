# EduServer API

This is specification for EduServer API.

API uses REST guidelines and primarily flat structure.

Descriptions for some of object types can be found [here](api/formats.md).

Some requests have *Required authentication* or *Required authorization* marks. 
This requests must contain `Authorization` header with `Bearer` token obtained 
from server.



## Endpoints

**Common API:**
 
* `POST /auth` – Acquire token: *In progress ...*

**Learner API:**

* `GET /courses` — Get all courses: [details](api/get_courses.md)
* `GET /courses/<pk>/materials` — Get all course materials: [details](api/get_courses_pk_materials.md)
* `GET|HEAD /courses/<pk>/structure` — Get structure of the course: [details](api/get_courses_pk_structure.md)

* `GET /sections/<pk>` — Get single section: [details](api/get_sections_pk.md)
* `GET /lessons/<pk>` — Get single lesson: [details](api/get_lessons_pk.md)
* `GET /tasks/<pk>` — Get single task: [details](api/get_tasks_pk.md)

* `GET /comments/<pk>` — Get all comments for `<pk>` study item: *In progress ...*
* `POST /comments/<pk>` — Send comment for `<pk>` study item: *In progress ...*

**Educator API:**

* `POST /courses` — Create new course: [details](api/post_courses.md).
* `PUT /courses/<pk>` — Upload new version of the course: [details](api/put_courses_pk.md)

* `GET /courses/mine` — Get all courses available for editing: *In progress ...*
* `GET /courses/<pk>/full` — Get editing materials for this course: *In progress ...*
