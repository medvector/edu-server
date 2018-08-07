# Create new course

**Description:** 
create new course with first version and this user as sole editor.

**Require authentication!**

**No parameters.**

## Request

```
POST /courses

{
    "format": String <min required plugin version>,
    "language": String <language code>,
    "programming_language": String <programming language>,

    "title": String <course title>,
    "summary": Sting <course description>,

    "items": Array[Section || Lesson] <course items>,
    "course_files": Map(String ⟶ String) <global course files>
}
```

Objects `Section`, `Lesson`, `Task` have formats described 
[here](formats.md), fields `id`, `last_modified` are not present.


## Response

```
201 Created

{
    "course_id": Integer <course pk>,
    "version_id": Integer <version pk>,
    "last_modified": DateTime <last modification time>,
    "items": Array[Section || Lesson] <course items>
}
```

All items fields have meta information with sub items. That way 
IDE can assign id's to each item, so in next update it will be 
able to use that info for unchanged items.

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
* **401 Unauthorized** — authentication failed


## Example

### Request

```
POST /courses
```

```json
{
    "format": "1.7-2018.1-119",
    "type": "course",
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
                    "format": "1.7-2018.1-119",
                    "type": "programming",
                    "title": "Hello, Rust",
                    "description": "...",
                    "description_format": "md"
                },
                {
                    "format": "1.7-2018.1-119",
                    "type": "programming",
                    "title": "Cargo Package Manager",
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
                    "title": "Core data types",
                    "description": "...",
                    "description_format": "md",
                    "items": [
                        {
                            "format": "1.7-2018.1-119",
                            "type": "programming",
                            "title": "Example 1",
                            "description": "...",
                            "description_format": "md"
                        },
                        {
                            "format": "1.7-2018.1-119",
                            "type": "programming",
                            "title": "Example 2",
                            "description": "..."
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
                            "format": "1.7-2018.1-119",
                            "type": "programming",
                            "title": "Example 1",
                            "description": "...",
                            "description_format": "md"
                        },
                        {
                            "format": "1.7-2018.1-119",
                            "type": "programming",
                            "title": "Example 2",
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
    "id": 41,
    "last_modified": "2018-07-19 17:25:25.512635",
    "items": [
        {
            "id": 1135,
            "type": "lesson",
            "items": [
                {"id": 1136}, {"id": 1137}
            ]
        },
        {
            "id": 1138,
            "type": "section",
            "items": [
                {
                    "id": 1139,
                    "type": "lesson",
                    "items": [
                        {"id": 1140}, {"id": 1141}
                    ]
                },
                {
                    "id": 1142,
                    "type": "lesson",
                    "items": [
                        {"id": 1143}, {"id": 1144}
                    ]
                }
            ]
        }
    ]
}

```