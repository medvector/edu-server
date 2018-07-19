# Get all courses

**Description:** 
get all courses matching parameters. If course have more recent 
version for newer version of plugin, include in course info all
change notes between available version and newest, so learner
can decide is it worth to update plugin itself.

**Parameters:**

* `ver` *(required)* — plugin version
* `lang[]` *(required)* — list of all languages user wants
* `plang[]` *(required)* — list of all programming languages user wants
* `query` — search string 
* `ds` — search in description too (default: no)

## Request

```
GET /courses
```

## Response

```
200 OK

{
    "ver": String <plugin version>,
    "lang": Array[String] <user languages>,
    "plang": Array[String] <user programming languages>,
    "query": String <search query string>,
    "ds": Boolean <search in description flag>,
    "results": Array[CourseInfo] <course info>
}
```

Course information format:

```
CourseInfo := {

    "course_id": Integer <course pk>,
    "title": String <course title>,
    "summary": Sting <course description>,
    "language": String <language code>,
    "programming_language": String <programming language>,

    "last_modified": DateTime <last modification time of availabal ver>,
    "plugin_ver": String <min required plugin version>,
    
    "newest_last_modified": DateTime <last modification time of newest ver>,
    "change_notes": Array[String] <all change notes between avail. & newest>
}
```

Fields `newest_last_modified` and `change_notes` are always present. If
available version is the newest one, `newest_last_modified` equals
`last_modified` field and `change_notes` is empty array.



## Errors

* **400 Bad Request** — bad request format