all_bookings_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "date": {"type": "string", "format": "date"},
            "destination": {"type": "string"},
            "id": {"type": "integer"},
            "origin": {"type": "string"},
            "userId": {"type": "integer"},
        },
        "required": ["date", "destination", "id", "origin", "userId"],
        "additionalProperties": False,
    },
}
