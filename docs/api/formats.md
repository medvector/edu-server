# EduServer JSON formats

This document describes base object formats, user in API documentation.

## Multiple translations

To support courses with multiple languages available all titles and descriptions are stored in `LText` object type, which represents map from language code (en, ru, etc.) to translation in that language.

When materials are accessed through Learner API, `LText`replaced 
with `String` containing translation for chosen language.

```
LText := {
    "lang_code_1": "translation_1",
    "lang_code_N": "translation_N"
}
```

## Task format

Task is basic block for all courses. Generalized format:

```
Task := TaskFull || TaskMeta

TaskFull := {
    "format": Integer <task format version>,
    "id": Integer <study item pk>,
    "type": String <lesson type>,
    "name": LText <task name>,
    "description": LText <task description>,
    "description_format": String <description format: html, md, etc.>,
    "last_modified": DateTime <last modification time>,

    ... type & version specific fields ...
}

TaskMeta := {
    "format": Integer <task format version>,
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>
}
```

Format for tasks will have versions matching plugin version. This will
allow to add new type of task, graders, etc.

## Course format

Task are grouped into lessons, lessons can be grouped into sections.
Course consists of sections and lessons. Lesson and section have almost
the same format, except `type` and `items` fields content.

```
Lesson := LessonFull || LessonMeta

LessonFull := {
    "type": "lesson",
    "id": Integer <study item pk>,
    "title": LText <lesson title>,
    "description": LText <lesson description>,
    "description_format": String <description format>,
    "last_modified": DateTime <last modification time of this lesson items>,
    "items": Array[Task] <lesson tasks list> 
}

LessonMeta := {
    "type": "lesson",
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time of this lesson items>
}
```

```
Section := SectionFull || SectionMeta

SectionFull := {
    "type": "section",
    "id": Integer <study item pk>,
    "title": LText <section title>,
    "description": LText <section description>,
    "description_format": String <description format>,
    "last_modified": DateTime <last modification time of this section items>,
    "items": Array[Lesson] <section lessons list> 
}

SectionMeta := {
    "type": "section",
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time of this section items>
}
```

Courses have different versions for different plugin versions. This is
done because we want to support all versions of EduTools plugin, not
just newest one.

Course have one version per version of plugin (or version of task 
format). If update doesn't change minimal required version of plugin,
we update version, otherwise — create new.

Generalized course format:

```
Course := {
    "id": Integer <study item pk>,
    "version": String <min required version of plugin>,
    "last_modified": DateTime <last modification time of the course>,
    "title": LText <title of the course>,
    "summary": LText <description of the course>,
    "language": Array[LangCode] <available translations>,
    "programming_language": Array[LangCode] <available programming languages>,
    "items": Array[Section || Lesson] <course items>
}
```

## Format variations

Field `last_modified` are set by the server and missing if course is uploading. If course materials are uploaded, newly created or changed elements won't have `id` field, old unchanged elements will have only
id and meta information (`*Meta` formats).

If format is different from described above, it will be present in request
documentation page.