from pathlib import Path
from re import U

import marvin

from entries import CallEntry

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
    Self,
    Union,
    Sequence,
)  # Added Sequence import

from pydantic import BaseModel, Field

import openai
from dotenv import load_dotenv

load_dotenv()


import marvin
import marvin.audio
from marvin import Image as aiImage
from marvin.audio import Audio as aiAudio


def validate_json_path(file_path: str) -> None:
    if not file_path.endswith(".json"):
        raise ValueError(
            f"Invalid file path: {file_path}. The file path must end with '.json'."
        )


class CallApp(BaseModel):
    records: CallLog = Field(
        ..., description="The CallLog records instance to be stored and manipulated"
    )
    json_path: Optional[Union[str, Path]] = Field(
        default=None,
        description="Path to the JSON file which stores CallLog `records` instance",
    )

    def log_artifact(self, inputs: Union[aiAudio, str, aiImage, CallEntry]):
        if isinstance(inputs, aiAudio):
            self.log_audio(inputs)
        elif isinstance(inputs, str):
            self.log_text(inputs)
        elif isinstance(inputs, aiImage):
            self.log_image(inputs)
        elif isinstance(inputs, CallEntry):
            self.log_entry(inputs)

    def log_audio(self, inputs: aiAudio):
        text: str = marvin.transcribe(inputs)
        self.log_text(text)

    def log_text(self, inputs: str):
        entry: CallEntry = marvin.cast(
            inputs,
            target=CallEntry,
            instructions="parse log entry details, being especially thorough",
        )
        self.log_entry(entry)

    def log_image(self, inputs: aiImage):
        instructions = """\
        You are an expert in image processing and analysis. 
        You are given an image of a form that needs to be approved. 
        Your task is to analyze the image and provide a detailed report on the form's content 
        """
        entry: CallEntry = marvin.cast(
            data=inputs, target=CallEntry, instructions=instructions
        )
        self.log_entry(entry)

    def log_entry(self, inputs: CallEntry):
        self.records.append(inputs)

    @property
    def json_path_as_path(self) -> Path:
        return Path(self.json_path)

    class Config:
        json_encoders: dict[type[Path], type[str]] = {Path: str}

    def save(self):
        validate_json_path(self.json_path)
        self.json_path_as_path.write_text(data=self.model_dump_json())

    def save_as(self, set_new_path: Union[str, Path]):
        new_path = Path(set_new_path)
        validate_json_path(str(new_path))
        new_path.write_text(data=self.model_dump_json())
        self.json_path = new_path

    @classmethod
    def load(cls, json_path: Union[str, Path] = json_path):
        json_path = Path(json_path)
        # validate_json_path(str(json_path))
        if not json_path.exists():
            raise FileNotFoundError(f"File not found: {json_path}")
        print("data")
        data: Union[dict, list[dict]] = json.loads(json_path.read_text())
        if isinstance(data, dict):
            if "call_records" in data:
                clog = CallLog(**data)
            else:
                data = [data]  # ? single entry maybe
        elif isinstance(data, list):
            clog = CallLog(call_records=data)
        new_app = cls(records=clog, json_path=json_path)
        return new_app


from entries import toy_entry_dict

if __name__ == "__main__":
    app = CallApp(
        records=CallLog(call_records=[toy_entry_dict]), json_path="toy_json_path.json"
    )

    app.save()
    print("success")
