error_schema = {
    "type": "object",
    "properties": {
        "errors": {
            "type": ["null", "array"],
            "items": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "object",
                        "properties": {
                            "in": {"type": "string"},
                            "name": {"type": "string"},
                            "docPath": {"type": "string"},
                            "path": {"type": "string"},
                        },
                        "required": ["in", "name", "docPath", "path"],
                    },
                    "message": {"type": "string"},
                },
                "required": ["location", "message"],
            },
        },
        "message": {"type": "string"},
    },
    "required": ["message"],
    "additionalProperties": False,
}
