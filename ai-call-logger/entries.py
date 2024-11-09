# pylint: disable=too-many-lines
"""
code expanding on structure fields and properties of each call log entry
"""


import os
import json
from datetime import datetime
from textwrap import indent
from typing import (
    Annotated,
    List,
    Literal,
    Optional,
    Union,
    Sequence,
)  # Added Sequence import

from pydantic import BaseModel, Field
from pydantic import ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber

import openai
from dotenv import load_dotenv

# import marvin
# import marvin.audio

# Removed invalid backtick expressions and fixed indentation
Service = Literal[
    "Microbiology", "Chemistry", "Laboratory Hematology", "Molecular", "Transfusion"
]

ClinicalService = Literal[
    "Allergy",
    "BMT",
    "Cardio Thoracic",
    "ED",
    "Endocrine",
    "GI",
    "GU",
    "Hematology",
    "Internal Med",
    "Neurology",
    "OB-GYN",
    "Orthopedics",
    "Pulmonary",
    "Renal",
    "Rheumatology",
    "SLCH",
    "Surgery",
    "Podiatry",
    "Psychiatry",
    "Other",
]


# class BJHPhoneNumberValidator(PhoneNumberValidator):
#     default_region: Optional[str] = "US"

# from util_json import json_indent

config = ConfigDict(
    str_to_lower=True,
    str_strip_whitespace=True,
    # json_encoders={datetime: lambda v: v.timestamp()}, # file looks like integer or s/t. not recognizable as datti
    json_schema_extra={"indent": 2},  # 4
)


class Person(BaseModel):  # noqa
    """A person"""

    model_config: ConfigDict = config

    last_name: str = Field(..., description="The last name of the person")
    first_name: str = Field(..., description="The first name of the person")


class Patient(Person):
    """The recipient of medical care and present discussion"""

    dob: datetime = Field(..., description="The date of birth of the patient")
    mrn: int = Field(..., gt=0, description="The medical record number of the patient")
    sex: Optional[Literal["M", "F"]] = Field(
        ..., description="The sex of the patient (None if unknown)"
    )
    age: Optional[int] = Field(
        ..., description="The age of the patient in years (None if unknown)"
    )


class Caller(Person):
    """The staff or faculty member initiating the call"""

    callback_number: str = Field(
        description="The phone number at which the caller can be reached"
    )
    clinical_service: Optional[ClinicalService] = Field(
        ...,
        description="The clinical service that the call was made to.\
            (Other if None of the above)(None if unsure)",
    )
    attending_doctor: Optional[Person] = Field(
        ...,
        description="The attending doctor on the case (often data not available -> '')",
    )
    caller_details: Optional[str] = Field(
        ...,
        description="Any additional details about the caller",
    )


class CallEntry(BaseModel):
    """A call log entry for the BJH Resident Pathology Service"""

    service: Service = Field(
        default="Chemistry",
        description="The pathology department service appropriate for handing the call",
    )

    patient: Optional[Patient] = Field(None, description="The patient information")

    caller: Optional[Caller] = Field(None, description="The caller information")

    laboratory_test: Optional[str] = Field(
        None,
        strip_whitespace=True,
        str_to_lower=True,
        max_length=100,
        description="The most relevant laboratory assay test or service",
    )

    call_category: Optional[
        Literal["Test Approval", "Lab Problem", "Alert", "Consult", "Feasibility"]
    ] = Field(
        None,
        description="The category of the call (None if unsure or not applicable)",
    )

    call_details: Optional[str] = Field(
        None,
        max_length=1000,
        description="The notes from the call. ( what is the situation, what is the question, etc )",
    )

    specimen_type: Optional[str] = Field(
        None,
        description="The relevant type of specimen under discussion in call,\
        common examples include: blood, urine, sputum, csf, serum, plasma, chyle, 'other', etc",
    )

    resolution: Literal["New", "Pending", "Complete", "Approval", "Cancel"] = Field(
        default="New", description="The resolution status of the call"
    )


class CallLog(BaseModel):
    """The current list of calls logged"""

    call_records: list[CallEntry] = Field(
        ..., description="The list of individual call log entries"
    )


toy_entry_dict = {
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


# call log database

if __name__ == "__main__":
    fake_data = {
        "service": "Hematology",
        "patient": {
            "last_name": "Johnson",
            "first_name": "Emily",
            "dob": "1995-05-15T00:00:00Z",
            "mrn": 987654321,
            "sex": "F",
            "age": 28,
        },
        "caller": {
            "last_name": "Brown",
            "first_name": "Michael",
            "callback_number": "(555) 123-4567",
            "clinical_service": "Emergency Medicine",
            "attending_doctor": "Dr. Garcia",
            "caller_details": "attending physician",
        },
        "laboratory_test": "Complete Blood Count",
        "call_category": "Urgent Result",
        "call_details": "Critically low platelet count detected.",
        "specimen_type": "blood",
        "resolution": "Pending",
    }
    entry = CallEntry(**fake_data)

    # Convert the entry to a JSON string
    json_data = entry.model_dump_json(indent=2)

    print("CallEntry as JSON:")
    print(json_data)

    # Convert the entry to a dictionary
    dict_data = entry.model_dump()

    print("\nCallEntry as dictionary:")
    print(json.dumps(dict_data, indent=2))
