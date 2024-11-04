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
import openai, marvin



# class Labs(BaseModel):
#     abs:
# CBC
# Date	WBC	Hgb	Hct	Plt
