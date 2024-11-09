import os
import json
from datetime import datetime
from re import L
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

# config = ConfigDict(
#     str_to_lower=True,
#     str_strip_whitespace=True,
#     # json_encoders={datetime: lambda v: v.timestamp()}, # file looks like integer or s/t. not recognizable as datti
#     json_schema_extra={"indent": 2},  # 4
# )


class Person(BaseModel):  # noqa
    """A person"""

    # model_config: ConfigDict = config

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


ApheresisType = Literal["Red Blood Cell Exchange", "Plasma Exchange"]
ReplacementFluidType = Literal["Plasma", "Albumin", "Red Blood Cells"]


class Procedure(BaseModel):
    date_time: datetime = Field(description="The date and time of the procedure")  # type: ignore
    apheresis_type: Optional[ApheresisType] = Field(
        description="The type of apheresis procedure to be performed"
    )
    volume_prebolus: Optional[int] = Field(
        description="The volume to be infused before the procedure to prevent hypotension"
    )
    replacement_fluid: Optional[ReplacementFluidType] = Field(
        description="The type of replacement fluid to be used"
    )
    grams_calcium: Optional[int] = Field(
        examples=[
            1,
            2,
            3,
            4,
        ],
        description="how much supplementary calcium to use to prevent hypocalcemia due to citrate",
    )
    mid_ionized_calcium_drawn: Optional[bool] = Field(
        description="Whether to draw mid-ionized calcium to check for hypocalcemia"
    )
    complications: list[str] = Field(
        default=[],
        examples=[
            "No complications",
            "Hypotension",
            "Rash managed with benedril",
        ],
        description="A list of complications that have occurred during the procedure and how they were managed.",
    )


class Correspondence(BaseModel):
    """A memo or note to the apheresis service made by the consulting provider or teammember"""

    content: str = Field(description="The memo or note to the apheresis service")

    call_back_number: Optional[PhoneNumber] = Field(
        description="The phone number to call back"
    )
    who: Optional[Person] = Field(description="The person who made the memo")


class Consult(BaseModel):
    apheresis_type: ApheresisType = Field(
        description="The type of apheresis procedure to be performed on `patient`"
    )
    procedures_remaining: int = Field(
        default=5,
        examples=[1, 2, 3, 4, 5],
        description="The number of apheresis procedures remaining, given the initial amount consulted for (usually 5) and the amount performed so far",
    )
    patient: Patient = Field(description="The patient participating in `procedure`")

    procedure_history: List[Procedure] = Field(
        default=[],
        description="a list of procedures performed on `patient` during this hospital stay.",
    )


# ERROR
#  marvin.Runs: Error calling tool
#  days_since_last_procedure: 'dict' object   runs.py:201
#  has no attribute 'procedure_history'
def days_since_last_procedure(consult: Consult) -> int:
    """The number of days since the last procedure.
    Return -1 if no procedures have been performed."""
    if not consult.procedure_history:
        return -1
    return (datetime.now() - consult.procedure_history[-1].datetime).days


class ApheresisServiceLog(BaseModel):
    """A log of the apheresis service"""

    consults: list[Consult] = Field(
        default=[], description="a list of all the consults for the apheresis service"
    )
