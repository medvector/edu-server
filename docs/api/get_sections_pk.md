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
GET /sections/<pk_1>&...&<pk_n>
```

## Response

```
200 OK

{
    "sections": [...]
}
```

Objects `Section`, `Lesson`, `Task` have formats described [here](formats.md).

## Errors

* **400 Bad Request** — bad request format
* **404 Not Found** — study item with one of those `pk` doesn't exists
* **409 Conflict** — study item with one of those `pk` exists, but that is not section


> In future: *401 Unauthorized*
