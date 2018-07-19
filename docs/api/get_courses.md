# Get all courses

**Description:** 
get all courses; if course have more recent version for newer 
version of plugin, include in course info all change notes 
between available version and newest, so learner can decide 
is it worth to update plugin itself.

> **??** We allow user to join old course versions.

**Parameters:**

* `version` — plugin version (default: *newest possible*)


## Request

```
GET /courses
```

## Response

```
200 OK

{
    "version": String <plugin version>,
    "courses": Array[CourseInfo] <course info>
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
    "tags": Array[String] <list of tags>,

    "last_modified": DateTime <last modification time of available ver>,
    "version": String <min required plugin version>,
    
    "change_notes": Array[String] <all change notes between avail. & newest>
}
```

Fields `newest_last_modified` and `change_notes` are always present. If
available version is the newest one, `newest_last_modified` equals
`last_modified` field and `change_notes` is empty array.

If course available in different languages there are multiple objects
in results array for this course (each for separate language branch).

## Errors

There are no client errors.