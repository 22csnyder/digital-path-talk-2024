
import os
from pathlib import Path
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

import marvin


report_uds = Path("screen_result.txt")
report_uds_w_names = Path("screen_result_w_names.txt")

text_uds = report_uds.read_text()
text_uds_w_names = report_uds_w_names.read_text()


# @marvin.extract()
# def extract_uds_screen_results(text: str) -> list[str]:
#     """Extract UDS screen results from a text file"""
#     return text

@marvin.fn
def parse_uds_screen_results(text: str) -> list[str]:
    """Parse UDS screen results for positive drugs"""


if __name__ == "__main__":

    extracted_text = \
    marvin.extract(
        data=text_uds,
        instructions="extract drug name results from series of UDS screens",
        target=list[str],
    )

    pprint(extracted_text)



# marvin.classify(proposed_parse, labels=["drug","junk", "unsure"])
