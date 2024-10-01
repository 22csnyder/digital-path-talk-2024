import json

json_indent = 4
json_path = "call_log.json"
import json

from entries import *

import os
import json
from datetime import datetime
from typing import (
    Annotated,
    List,
    Literal,
    Optional,
    Union,
    Sequence,
)  # Added Sequence import

from pydantic import BaseModel, Field

import openai
from dotenv import load_dotenv

load_dotenv()

def validate_json_path(file_path: str) -> None:
    if not file_path.endswith('.json'):
        raise ValueError(f"Invalid file path: {file_path}. The file path must end with '.json'.")

def dump_json(file_path: str, basemodel: BaseModel) -> None:
    validate_json_path(file_path)
    with open(file_path, "w") as f:
        json.dump(basemodel.model_dump(indent=json_indent), f)

def read_logs(indent: int = json_indent) -> list[str]:
    """
    get all entries from the json file
    """
    validate_json_path(json_path)
    with open(json_path, "r") as f:
        data = f.read()
    return json.loads(data)


def append_log(entry: CallEntry):
    """
    append an entry to the json file
    """
    validate_json_path(json_path)
    json_entry = entry.model_dump_json(indent=json_indent)
    with open(json_path, "a") as f:
        f.write(json_entry)

    # # return all json entries
    # logs: list[str] = read_logs(indent=json_indent)
    # return logs


def append_to_json_file(call_entry: CallEntry, file_path: str = json_path) -> None:
    validate_json_path(file_path)
    new_entry = call_entry.model_dump_json(indent=json_indent)
    with open(file_path, mode="r+") as file:
        # Load existing data
        data = json.load(file)
        # Append new entry
        data.append(new_entry)
        # Move file pointer to the beginning
        file.seek(0)
        # Write updated data
        json.dump(data, file, indent=json_indent)

new_entry = {
    "service": "Chemistry",
    "patient": {
        "last_name": "doe",
        "first_name": "john",
        "dob": "1980-01-01T00:00:00Z",
        "mrn": 123456789,
        "sex": "M",
        "age": 41,
    },
    "caller": {
        "last_name": "smith",
        "first_name": "jane",
        "callback_number": "(123) 456-7890",
        "clinical_service": "Cardiology",
        "attending_doctor": "Dr. Who",
        "caller_details": "resident",
    },
    "laboratory_test": "Troponin",
    "call_category": "Critical Value",
    "call_details": "Critical troponin value reported.",
    "specimen_type": "blood",
    "resolution": "Reported",
}

if __name__ == "__main__":

    # Example usage
    append_to_json_file("ai-call-logger/call_log.json", new_entry)
