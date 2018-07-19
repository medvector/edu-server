# Get single lesson

**Description:** 
get all lesson materials

**Require authentication!**

> In future: *Require authorization!*

**Parameters.**
* `pk` *(in path)* *(required)* — lesson pk

## Request

```
GET /lessons/<pk>
```

## Response

```
200 OK

Lesson
```

Objects `Lesson`, `Task` have formats described [here](formats.md).

## Errors

* **400 Bad Request** — bad request format
* **404 Not Found** — study item with that `pk` doesn't exists
* **409 Conflict** — study item with that `pk` exists, but that is not lesson


> In future: *401 Unauthorized*
