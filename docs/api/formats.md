# EduServer JSON formats

This document describes base object formats used in API documentation.


## Task format

Task is basic block for all courses. Generalized format:

```

Task := {

    "format": String <task version format>,
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>,

    "type": String <task type>,
    "name": String <lesson title>,
    "description": String <lesson description>,
    "description_format": String <lesson description format>,
    
    ... type & version specific fields ...
}

```

Format for tasks will have versions matching plugin version. 
This will allow to add new type of task, graders, etc.


## Course structure format

Task are grouped into lessons, lessons can be grouped into sections.
Lesson and section have almost the same format, except type and 
items fields content.

```

Lesson := {

    "type": "lesson",
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>,

    "title": String <lesson title>,
    "description": String <lesson description>,
    "description_format": String <lesson description format>,
    
    "items": Array[Task] <list of tasks>
}

```
  
```

Section := {

    "type": "section",
    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>,

    "title": String <section title>,
    "description": String <section description>,
    "description_format": String <section description format>,
    
    "items": Array[Lesson] <list of lessons>
}

```

Course consists of sections and lessons. 

Course can have multiple versions for different plugin versions,
languages and programming languages.
This is done because we want to support all versions of EduTools
plugin, not just newest one.

Course have one version per version of plugin (or version of task 
format). If update doesn't change minimal required version of plugin,
we update version, otherwise — create new.

> **??** See [update query](put_courses_pk.md) for question.

If we want to create version of the course for new natural or 
programming language, we request newest (?) version of the course
for some base languages in IDE for target language (for translation 
this will be same IDE), and there make change. After that upload
version for new language. This basically creates new branch for
new language. For next versions of that branch you can:

* make changes to translated version (task can differ)
* request newest version for base language (translations for
  unchanged version saved) 


```

CourseVersion := {

    "id": Integer <study item pk>,
    "last_modified": DateTime <last modification time>,

    "version": String <min required plugin version>,
    "language": String <language code>,
    "programming_language": String <programming language>,

    "title": String <course title>,
    "summary": Sting <course description>,

    "items": Array[Section || Lesson] <course items>
    "course_files": Map <map: file path ⟶ content>

}

```

Courses are simply bundles for course version, they don't store
any information. 

