# Upload new version of the course

**Description:**
upload new version of the course in delta format; 
always creating new version item.


**Require authorization!**

**No parameters.**

## Request

```
PUT /courses/<pk>/update

{
    "format": String <min required plugin version>,
    "language": String <language code>,
    "programming_language": String <programming language>,

    "title": String <course title>,
    "summary": Sting <course description>,
    "change_notes": String <changes description>,

    "items": Array[Section || Lesson] <course items>,
    "course_files": Map(String ⟶ String) <global course files>
}
```

Structure of the course in delta format. If item and is unchanged
client only sends meta information with no sub items:

```
 
Task := {
    "id": Integer <study item pk>
}

Lesson := {
    "type": "lesson",
    "id": Integer <study item pk>
}

Section := {
    "type": "section",
    "id": Integer <study item pk>
}
```

Item is unchanged if it and all it's sub items are unchanged.
Server assigns `id` and `last_modified` fields, presence of `id`
field means that is is unchanged element.

For new and changes items (`Section`, `Lesson`, `Task`) have formats 
described [here](formats.md), fields `id`, `last_modified` are not present.


## Response

```
201 Created

{
    "id": Integer <version pk>,
    "last_modified": DateTime <last modification time>,
    "items": Array[Section || Lesson] <course items>
}
```

All `items` fields have meta information with sub items. That way
IDE can assign id's and modification times to each item, so in next
update it will be able to use that info for unchanged items.

```
Task := {
    "id": Integer <study item pk>
}

Lesson := {
    "type": "lesson",
    "id": Integer <study item pk>,
    "items": Array[Task] <list of tasks>
}

Section := {
    "type": "section",
    "id": Integer <study item pk>,
    "items": Array[Lesson] <list of lessons>
}
```


## Errors

* **400 Bad Request** — bad request format
* **401 Unauthorized** — authorization failed
