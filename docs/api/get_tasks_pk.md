# Get single task

**Description:** 
get all task materials

**Require authentication!**

> In future: *Require authorization!*

**Parameters.**
* `pk` *(in path)* *(required)* — task pk

## Request

```
GET /tasks/<pk>
GET /tasks/<pk_1>&...&<pk_n>
```

## Response

```
200 OK

{
    "tasks": [...]
}
```

Object `Task` has format described [here](formats.md).

## Errors

* **400 Bad Request** — bad request format
* **404 Not Found** — study item with one of those `pk` doesn't exists
* **409 Conflict** — study item with one of those `pk` exists, but that is not task


> In future: *401 Unauthorized*
