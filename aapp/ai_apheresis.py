import os
import json
from rich import print as rprint
from pprint import pprint
import openai
from dotenv import load_dotenv
import openai, marvin

from basemodel_apheresis import *

instructions = """
    You are an expert apheresis nurse on the apheresis team. Together you run a very busy apheresis service in a medical hospital. You are very eager to help and are very detail orriented by nature. Your role is to help keep track of the evolving list of patients (aka consults) and the apheresis procedures performed on them. You are knowledgable regarding apheresis procedures typically performed by a licensed clinical pathologist. You function as a reliable natural-language interface for the apheresis service call log.
    
    All red cell exchanges are by default 1 procedure and consulted by the hematology attending Bloodbaron Harly
"""


# class Labs(BaseModel):
#     abs:
# CBC
# Date	WBC	Hgb	Hct	Plt

app = marvin.beta.Application(
    name="Pheresis Scribe",
    instructions=instructions,
    state=ApheresisServiceLog(),
    tools=[days_since_last_procedure],
)

# app.add_tool(Consult)
# app.add_tool(ApheresisProcedure)
# app.add_tool(Correspondence)

rprint(app.state)

# app.say(
#     "We got a call this morning about Henry Morganthau (58yM dob 5/22/1966 mrn=22220022) who presented with NMO (neuromyelitis optica). Neurology attending (Van Allen) called this morning requesting 6 rounds of apheresis."
# )

# app.say(
#     "Another patient Bobbi Chandrasekar (42Male dob 1/1/1982 mrn=21120023) who regularly sees us for red cell exchange for her sickle cell disease. He is scheduled for 1 procedure for tomorrow morning at 10am."
# )

# app.say(
#     "record that Bobbi had a procedure the previous month september 9, 2024. No complications."
# )

# app.say(
#     "Okay record that Bobbi's procedure occured today at 10am without complications"
# )

# app.say(
#     "Okay record that Henry's procedure occured at 3pm october 10, 2024 without complications"
# )

# rprint(app.state)


# # app.say("Okay record that henry's procedure occured at 3pm october 10, 2024 without complications")

# app.say("How many procedures have been performed in october?")

app.say("How many days has it been since Bobbi's last procedure?")