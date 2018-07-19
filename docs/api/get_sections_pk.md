# Get single section

**Description:** 
get all section materials

**Require authentication!**

> In future: *Require authorization!*

**Parameters.**
* `pk` *(in path)* *(required)* — section pk

## Request

```
GET /sections/<pk>
```

## Response

```
200 OK

Section
```

Objects `Section`, `Lesson`, `Task` have formats described [here](formats.md).

## Errors

* **400 Bad Request** — bad request format
* **404 Not Found** — study item with that `pk` doesn't exists
* **409 Conflict** — study item with that `pk` exists, but that is not section


> In future: *401 Unauthorized*
