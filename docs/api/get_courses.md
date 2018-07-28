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
    "courses": Array[CourseInfo] <course info>
}
```

Course information format:

```
CourseInfo := {

    "id": Integer <course pk>,
    
    "language": String <language code>,
    "programming_language": String <programming language>,
    "tags": Array[String] <list of tags>,

    "description": {
        "title": String <course title>,
        "summary": Sting <course description>,
        "change_notes": Array[String] <all change notes between avail. & newest>
    },

    "last_modified": DateTime <last modification time of available ver>,
    "version": String <min required plugin version>,
    
}
```

Field `change_notes` is always present, if available version is the 
newest one this field is empty array.

If course available in different languages there are multiple objects
in results array for this course (each for separate language branch).

## Errors

There are no client errors.