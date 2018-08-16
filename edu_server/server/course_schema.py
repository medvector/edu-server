post_course_schema = {
    "definitions": {
        "item_frame": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string"
                },
                "title": {
                    "type": "string"
                },
                "format": {
                    "type": "string"
                },
                "description_format": {
                    "type": "string"
                }
            }
        },
        "task": {
            "type": "object",
            "properties": {
                "item_frame": {"$ref": "#/definitions/item_frame"},
                "type": {
                    "type": "string",
                    "enum": ["edu", "theory", "output"]
                },
                "task_files": {
                    "type": "object"
                },
                "test_files": {
                    "type": "object"
                },
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
                "item_frame": {"$ref": "#/definitions/item_frame"},
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
                "item_frame": {"$ref": "#/definitions/item_frame"},
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
