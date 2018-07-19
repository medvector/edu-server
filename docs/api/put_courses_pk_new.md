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


## Example 1

### Request

```
PUT /courses/7/new
```

```json
{
    "plugin_ver": "1.7-2018.1-119",
    "language": "en",
    "programming_language": "rust",
    "title": "Introduction to Rust",
    "summary": "This is beginers course for Rust",
    "change_notes": "initial version",
    "course_files": {
        "Cargo.toml": "...",
        "tests.rs": "..."
    },
    "items": [
        {
            "type": "lesson",
            "title": "Introduction",
            "description": "...",
            "description_format": "md",
            "items": [
                {
                    "format": 1,
                    "type": "programming",
                    "name": "Hello, Rust",
                    "description": "...",
                    "description_format": "md"
                },
                {
                    "format": 1,
                    "type": "programming",
                    "name": "Cargo Package Manager",
                    "description": "...",
                    "description_format": "md"
                }
            ]
        },
        {
            "type": "section",
            "title": "Types and Variables",
            "description": "...",
            "description_format": "md",
            "items": [
                {
                    "type": "lesson",
                    "title": "Core data types",
                    "description": "...",
                    "description_format": "md",
                    "items": [
                        {
                            "format": 1,
                            "type": "programming",
                            "name": "Example 1",
                            "description": "...",
                            "description_format": "md"
                        },
                        {
                            "format": 1,
                            "type": "programming",
                            "name": "Example 2",
                            "description": "...",
                            "description_format": "md"
                        }
                    ]
                },
                {
                    "type": "lesson",
                    "title": "Variables and Mutability",
                    "description": "...",
                    "description_format": "md",
                    "items": [
                        {
                            "format": 1,
                            "type": "programming",
                            "name": "Example 1",
                            "description": "...",
                            "description_format": "md"
                        },
                        {
                            "format": 1,
                            "type": "programming",
                            "name": "Example 2",
                            "description": "...",
                            "description_format": "md"
                        }
                    ]
                }
            ]
        }
    ]
}

```

### Response

```
201 Created
```

```json
{
    "id": 42,
    "last_modified": "2018-07-19 17:25:25.455201",
    "items": [
        {
            "id": 1135,
            "type": "lesson",
            "last_modified": "2018-07-19 17:25:25.455077",
            "items": [
                {
                    "id": 1136,
                    "format": 1,
                    "last_modified": "2018-07-19 17:25:25.455090",
                },
                {
                    "id": 1137,
                    "format": 1,
                    "last_modified": "2018-07-19 17:25:25.455104",
                }
            ]
        },
        {
            "id": 1138,
            "type": "section",
            "last_modified": "2018-07-19 17:25:25.455127",
            "items": [
                {
                    "id": 1139,
                    "type": "lesson",
                    "last_modified": "2018-07-19 17:25:25.455141",
                    "items": [
                        {
                            "id": 1140,
                            "format": 1,
                            "last_modified": "2018-07-19 17:25:25.455155",
                        },
                        {
                            "id": 1141,
                            "format": 1,
                            "last_modified": "2018-07-19 17:25:25.455160",
                        }
                    ]
                },
                {
                    "id": 1142,
                    "type": "lesson",
                    "last_modified": "2018-07-19 17:25:25.455179",
                    "items": [
                        {
                            "id": 1143,
                            "format": 1,
                            "last_modified": "2018-07-19 17:25:25.455196",
                        },
                        {
                            "id": 1144,
                            "format": 1,
                            "last_modified": "2018-07-19 17:25:25.455201",
                        }
                    ]
                }
            ]
        }
    ]
}

```