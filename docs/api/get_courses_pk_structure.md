# Get all course materials

**Description:** 
get course structure for given plugin version and languages; there are 2 methods
allowed for this resource: 
* `HEAD` — used for requesting last modification date (update check)
* `GET` — used for delta update


**Require authentication!**

> In future: *Require authorization!*

**Parameters:**

* `pk` *(in path)* *(required)* — course pk
* `version` *(required)* — plugin version
* `lang` *(required)* — user language
* `plang` *(required)* — programming language


## Request

```
GET /courses/<pk>/structure
```

or 

```
HEAD /courses/<pk>/structure
```

## Response

```
200 OK
Last Modified: DateTime <last modification time>

{
    "type": "course",
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>,
    "format": String <min required plugin version>,
    "items": Array[Section || Lesson] <course items>
}
```

Objects `Section`, `Lesson`, `Task` have this formats:

```
Task := {
    "type": String <task version>,
    "format": String <task version format>,
    "id": Integer <study item pk>,
    "version_id": Integer <study item version pk>,
    "last_modified": DateTime <last modification time>
}

Lesson := {
    "type": "lesson",
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>,
    "items": Array[Task] <list of tasks>
}

Section := {
    "type": "section",
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>,
    "items": Array[Lesson] <list of lessons>
}
```



## Errors

* **400 Bad Request** — bad request format
* **404 Not Found** — course version matching given parameters not found


> In future: *401 Unauthorized* — if requested private course without
> invitation or paid course without payment. 
