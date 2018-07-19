# Upload new version of the course

**Description:**
upload new version of the course in delta format. If minimal required plugin
version hasn't changed we update existing version, otherwise — create new.

**Require authorization!**

**No parameters.**

## Request

```
PUT /courses/<pk>/new

{
    "plugin_ver": String <min required plugin version>,
    "language": String <language code>,
    "programming_language": String <programming language>,
    
    "title": String <course title>,
    "summary": Sting <course description>,

    "change_notes": String <changes description>,
    
    "items": Array[Section || Lesson] <course items>,
    "course_files": Map <map: file path ⇒ content>
}
```

Structure of the course in delta format. If item and is unchanged
client only sends meta information with no sub items:

```
 
Task := {
    "format": Integer <task version format>,
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>
}

Lesson := {
    "type": "lesson",
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>
}

Section := {
 
    "type": "section",
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>
}
```

Item is unchanged if it and all it's sub items are unchanged.
Server assigns `id` and `last_modified` fields, their presence
means that is is unchanged element; `last_modified` is used for verification that client indeed hasn't changed anything.

> **??** Should there be some hash field for stronger check.

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
    "format": Integer <task version format>,
    "id": Integer <study item pk>,
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
* **401 Unauthorized** — authorization failed
* **409 Conflict** — wrong `last_modified` on unchanged item ⇒ item has been changed