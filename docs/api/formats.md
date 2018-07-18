# EduServer JSON formats

## Multiple translations

To support courses with multiple languages available 
all titles and descriptions are stored in `LText` object
type, which represents map from language code (en, ru, etc.)
to translation in that language.

When materials are accessed through Learner API, `LText`
replaced with `String` containing translation for chosen 
language.

```json

LText := {
    "lang_code_1": "translation_1",
    "lang_code_N": "translation_N"
}

```


## Course structure format

Basic element is Task. Tasks grouped in lessons, lessons 
can be grouped in sections. Course consists of sections 
and lessons. Lesson and section have almost the same format, 
except `type` and `items` field.

```json
Lesson := {
    "type": "lesson",
    "id": Integer <study item pk>,
    "title": LText <title of the section>,
    "description": LText <description of the section>,
    "last_modified": DateTime <last modification time of this lesson items>,
    "items": Array[Task] <section items> 
}
```

```json
Section := {
    "type": "section",
    "id": Integer <study item pk>,
    "title": LText <title of the section>,
    "description": LText <description of the section>,
    "last_modified": DateTime <last modification time of this section items>,
    "items": Array[Lesson] <section items>
}
```

Courses can have different versions for different plugin version.
This is done because we want to support all versions of EduTools
plugin, not just newest one.

Course have one version per version of plugin (or version of task
format). If update doesn't change minimal required version of plugin,
we update version, otherwise — create new.

There are different formats describing course. Exact variation will
be given for each request. Generalized version: 

```json
Course := {
    "id": Integer <study item pk>, 
    "title": LText <title of the course>,
    "summary": LText <description of the course>,
    "language": Array[LangCode] <available translations>,
    "programming_language": Array[LangCode] <available programming languages>,
    "last_modified": DateTime <last modification time of the course>,
    "version": String <min required version of plugin>,
    "items": Array[Section || Lesson] <course items>
}
```

Variations:

* Just course info (`POST /courses`)
* New course version (`PUT /courses/<pk>/current`)
* Course info with change notes and versioning info (`GET /courses`)
* etc.


## Tasks

Basic task format:

```json
Lesson := {

    "format": Integer <task format version>,

    "id": Integer <study item pk>,
    "type": String <lesson type>,
    "name": LText <title of the section>,
    "description": LText <description of the section>,
    "description_format": String,
    "last_modified": DateTime <last modification time>,
    
    ... type & version specific fields ...

}
```

Format for tasks will have versions matching plugin version.
This will allow to add new type of lesson, graders, etc.
