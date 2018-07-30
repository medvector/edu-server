# Get all course materials

**Description:** 
get all course materials for given plugin version and languages

**Require authentication!**

> In future: *Require authorization!*

**Parameters:**

* `pk` *(in path)* *(required)* — course pk
* `version` *(required)* — plugin version
* `lang` *(required)* — user language
* `plang` *(required)* — programming language


## Request

```
GET /courses/<pk>/materials
```

## Response

```
200 OK

{
    "id": Integer <course pk>,
    "last_modified": DateTime <last modification time>,

    "version": String <min required plugin version>,
    "language": String <language code>,
    "programming_language": String <programming language>,

    "title": String <course title>,
    "summary": Sting <course description>,

    "items": Array[Section || Lesson] <course items>,
    "course_files": Map <map: file path ⟶ content>
}
```

Objects `Section`, `Lesson`, `Task` have formats described [here](formats.md).



## Errors

* **400 Bad Request** — bad request format
* **404 Not Found** — course version matching given parameters not found


> In future: *401 Unauthorized* — if requested private course without
> invitation or paid course without payment. 
