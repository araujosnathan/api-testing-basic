all_users_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email"},
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "surname": {"type": "string"},
        },
        "required": ["email", "id", "name", "surname"],
        "additionalProperties": False,
    },
}
