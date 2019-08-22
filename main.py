import requests
import json
import argparse
from typing import Dict, List


HOME_URL = "https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/registration"

POST_TERM_CODE_URL = "https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/term/search?mode=courseSearch"

GET_SECTION_INFO_URL = "https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_subjectcoursecombo={}&txt_term=201931&pageOffset=0&pageMaxSize=500&sortColumn=subjectDescription&sortDirection=asc"


def get_sections_for(dept: str, course_num: str, term_code: str):
    r: requests.Response = requests.get(HOME_URL)
    r: requests.Response = requests.post(
        POST_TERM_CODE_URL, data={"dataType": "json", "term": term_code}
    )
    cookies = r.cookies

    r: requests.Response = requests.get(
        GET_SECTION_INFO_URL.format(dept + "" + course_num), cookies=cookies
    )
    json_data = json.loads(r.content)
    return json_data["data"]


def load_config(filepath: str) -> Dict[str, List[str]]:
    """
    Loads a JSON configuration from a provided filepath. The configuration should be in the format:
    {
        "DEPT-COURSE": [CRN, CRN],
        ...
    }
    """
    return json.load(open(filepath, "r"))


def notify_of_availability(
    section, src_email: str, src_pass: str, dest_email: str
) -> None:
    """
    Notifies the user of the availability of a certain section via email.
    """
    print(section["subjectCourse"], section["sequenceNumber"])


def main(args):

    if not args.dest_email:
        # Assume the user would like to send the email to themselves.
        args.dest_email = args.src_email

    config = load_config("./config.json")
    for deptcrs, crns in config.items():
        dept, course_num = deptcrs.split("-")
        print("Checking for availability", dept, course_num)
        sections = get_sections_for(dept, course_num, term_code)
        for section in sections:
            if (
                section["courseRegistrationNumber"] in crns
                and section["seatsAvailable"] > 0
            ):
                notify_of_availability(
                    section, args.src_email, args.src_pas, args.dest_email
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="src_email",
        nargs=1,
        type=str,
        help="The Gmail address to send the email from. MAKE SURE LESS-SECURE APPS CAN ACCESS THIS EMAIL.",
    )
    parser.add_argument(
        dest="src_pass",
        nargs=1,
        type=str,
        help="The password to provide along wih src_email",
    )
    parser.add_argument(
        dest="term_code",
        nargs=1,
        type=str,
        help="The 6-digit code used by TAMU to represent terms. Term codes are formatted as YYYYSU, where YYYY is the 4-digit year, S is the season (1=Spring, 2=Summer, 3=Fall), and U is the university (1=College Station, 2=Galveston, 3=Qatar)",
    )
    parser.add_argument(
        "-dest_email",
        dest="dest_email",
        default=None,
        type=str,
        help="The address to send emails to, if it differs from src_email.",
    )
    main(parser.parse_args())
