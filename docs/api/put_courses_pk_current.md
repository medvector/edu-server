# Upload current version of the course

**Description:** 
upload new version of the course in delta format.
If minimal required plugin version hasn't changed — update
existing version, otherwise — create new version.  

**Require authorization!**

## Request

```
PUT /courses/<pk>/current

{
    "format": Integer <json format version>,
    "title": LText <title of the course>,
    "summary": LText <description of the course>,
    "language": Array[LangCode] <available translations>,
    "programming_language": Array[PLangCode] <available programming languages>,
    "version": String <min required version of plugin>,
    "change_notes": LText <changes between versions>
    

    "items": Array[Section || Lesson] <course items>
}
```

If `Section` / `Lesson` / `Tasks` are changed, they have base format without `id` fields. Otherwise:

```
Lesson := {
    "type": "lesson",
    "id": Integer <study item pk>
}

Section := {
    "type": "section",
    "id": Integer <study item pk>
}

Tasks := {
    "id": Integer <study item pk>,
}
```

## Response

```
201 Created

{
    "id": Integer <study item pk>,
    "version": String <min required version of plugin>,
    
    "items": Array[Section || Lesson] <course items>
}
```