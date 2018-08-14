post_course_schema = {
    "definitions": {
        "task": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string"
                },
                "type": {
                    "type": "string",
                    "enum": ["edu", "theory", "output"]
                },
                "description": {
                    "type": "string"
                },
                "description_format": {
                    "type": "string"
                },
                "task_files": {
                    "type": "object"
                },
                "test_files": {
                    "type": "object"
                },
                "format": {
                    "type": "string"
                }
            },
            "required": ["title", "type", "description", "description_format"]
        },
        "lesson": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "const": "lesson"
                },
                "title": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
                "description_format": {
                  "type": "string"
                },
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "$ref": "#/definitions/task"
                    }
                }
            },
            "required": ["title", "type", "items"]
        },
        "section": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "const": "section"
                },
                "title": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
                "description_format": {
                  "type": "string"
                },
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "$ref": "#/definitions/lesson"
                    }
                }
            },
            "required": ["title", "type", "items"]
        }
    },
    "id": "course",
    "properties": {
        "type": {
            "type": "string",
            "const": "course"
        },
        "language": {
            "type": "string"
        },
        "programming_language": {
            "type": "string"
        },
        "change_notes": {
            "type": "string"
        },
        "summary": {
          "type": "string"
        },
        "course_files": {
          "type": "object"
        },
        "items": {
            "type": "array",
            "items": {
                    "type": "object",
                    "oneOf": [{"$ref": "#/definitions/lesson"}, {"$ref": "#/definitions/section"}]
            }
        },
        "title": {
            "type": "string"
        },
        "format": {
            "type": "string"
        }
    },
    "required": ["language", "programming_language", "title", "format"],
    "additionalProperties": False
}
