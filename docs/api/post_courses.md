# Create new course


**Description:** 
create new course with this user as sole editor.

**Require authentication!**


## Request

```
POST /courses

{

    "title": LText <title of the course>,
    "summary": LText <description of the course>,
    "language": Array[LangCode] <available translations>,
    "programming_language": Array[PLangCode] <available programming languages>

}
```

## Response

```
201 Created

{
    "id": Integer <study item pk>,
    "last_modified": DateTime <course creation datetime>
}
```


## Errors

* **400 Bad Request** — bad requests format
* **401 Unauthorized** — authentication failed
* **409 Conflict** — course with that title already exists (?)