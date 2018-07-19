# Create new course

**Description:** create new course with this user as sole editor.

**Require authentication!**

**No parameters.**

## Request

```
POST /courses
```

## Response

```
201 Created

{
    "id": Integer <study item pk>,
    "last_modified": DateTime <course creation time>
}
```

## Errors

* **401 Unauthorized** — authentication failed