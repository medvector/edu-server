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
GET /lessons/<pk_1>&...&<pk_n>
```

## Response

```
200 OK

{
	"lessons": [...]
}
```

Objects `Lesson`, `Task` have formats described [here](formats.md).

## Errors

* **400 Bad Request** — bad request format
* **404 Not Found** — study item with one of those `pk` doesn't exists
* **409 Conflict** — study item with one of those `pk` exists, but that is not lesson


> In future: *401 Unauthorized*
