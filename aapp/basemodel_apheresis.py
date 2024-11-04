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


ApheresisTypes = Literal["Red Blood Cell Exchange", "Plasma Exchange"]
ReplacementFluidTypes = Literal["Plasma", "Albumin", "Red Blood Cells"]


class ApheresisProcedure(BaseModel):
    apheresis_type: ApheresisTypes = Field(
        description="The type of apheresis procedure to be performed"
    )
    volume_prebolus: int = Field(
        description="The volume to be infused before the procedure to prevent hypotension"
    )
    replacement_fluid: ReplacementFluidTypes = Field(
        description="The type of replacement fluid to be used"
    )
    grams_calcium: int = Field(
        examples=[
            1,
            2,
            3,
            4,
        ],
        description="how much supplementary calcium to use to prevent hypocalcemia due to citrate",
    )
    mid_ionized_calcium_drawn: bool = Field(
        description="Whether to draw mid-ionized calcium to check for hypocalcemia"
    )
    complications: list[str] = Field(
        description="A list of complications that have occurred during the procedure and how they were managed."
    )


class Correspondence(BaseModel):
    """A memo or note to the apheresis service made by the consulting provider or teammember"""

    content: str = Field(description="The memo or note to the apheresis service")
    call_back_number: PhoneNumber = Field(description="The phone number to call back")
    who: Person = Field(description="The person who made the memo")


class Consult(BaseModel):
    apheresis_type: ApheresisTypes = Field(
        description="The type of apheresis procedure to be performed on `patient`"
    )
    procedures_remaining: Optional[int] = Field(
        "The number of apheresis procedures remaining, given the initial amount consulted for (usually 5) and the amount performed so far"
    )
    patient: Patient = Field(description="The patient participating in `procedure`")

    consult_history: list[Union[ApheresisProcedure, Correspondence]] = Field(
        default=[],
        description="a list of records of the patient's present hospital stay relevant to the aphersis service. These include procedures or memo's (type str)  the apheresis procedures performed on `patient` during this hospital stay.",
    )
