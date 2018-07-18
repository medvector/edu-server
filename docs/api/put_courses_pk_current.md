# Upload current version of the course

**Description:** 
upload new version of the course in delta format.
If minimal required plugin version hasn't changed 
we update existing version, otherwise — creating new.

**Require authorization!**


## Request

```
PUT /courses/<pk>/current

{
    "version": String <min required version of plugin>,
    "change_notes": LText <changes between versions>,
    "items": Array[Section || Lesson] <course items>
}
```

If `Section` / `Lesson` / `Task` unchanged they represented
in `*Meta` formats.

***Note:*** presence of `id` field means that is unchanged
element, `last_modified` field is used for verification that
client indeed hasn't changed anything.

Otherwise (if they newly created or changed) they represented 
in `*Full` formats, without `id` and `last_modified` fields.


## Response

```
201 Created

{
    "id": Integer <version pk>,
    "items": Array[Section || Lesson] <course items>
}
```

All `items` fields contain study items in `*Meta` format with 
items field. That way IDE can assign id's and modification times
to each item, so in next update it will be able to use that info
for unchanged items.

## Errors

* **400 Bad Request** — bad requests format
* **401 Unauthorized** — authorization failed
* **409 Conflict** — wrong `last_modified` on 
  unchanged item ⇒ item has been changed
