import re


def parse_reports(text):
    # Split the text into individual reports based on the repeating phrase
    reports = re.split(r"The following compounds were detected:", text)

    # Clean up each report by removing unnecessary parts and splitting drugs into a list
    parsed_reports = []
    for report in reports:
        # Extract all lines that contain drug names by removing known footer texts
        report_cleaned = re.sub(
            r"Repeated and verified\.\n?Medical Director review to follow\.", "", report
        ).strip()

        # Extract drug names using regex, assuming drug names can be followed by optional parentheses
        drugs = re.findall(r"([A-Za-z0-9\-\(\)]+)", report_cleaned)

        if drugs:
            parsed_reports.append(drugs)

    return parsed_reports


# Sample input text
text = """
The following compounds were detected: 
Tetrahydrocannabinol (THC)
Repeated and verified.
Medical Director review to follow.
The following compounds were detected: 
Benzoylecgonine (BEG)
Fentanyl
Tramadol
O-Desmethyl tramadol
Repeated and verified.
Medical Director review to follow.
The following compounds were detected: 
Amphetamine
Methamphetamine
Alprazolam (Xanax)
Lorazepam-glucuronide
Repeated and verified.
Medical Director review to follow.
"""

if __name__ == "__main__":
    # Parse the reports
    parsed_reports = parse_reports(text)

    # Output the parsed reports and drugs
    for idx, drugs in enumerate(parsed_reports, start=1):
        print(f"Report {idx}: {drugs}")
