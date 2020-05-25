import argparse
import smtplib
import json
from typing import NamedTuple

import flares

TCC = "tcc"
TAMU = "tamu"
SCHOOL_FLARES = {TCC: flares.TCCFlare(), TAMU: flares.TAMUFlare()}


class ConfigEntry(NamedTuple):
    dept: str
    course_num: str
    section_num: str


def load_desired_sections(config_filepath: str):
    with open(config_filepath, "r") as f:
        json_data = json.load(f)
    results = []
    for dept_course, section_nums in json_data.items():
        dept, course = dept_course.split("-")
        for section_num in section_nums:
            results.append(ConfigEntry(dept, course, section_num))
    return results


def main(config_filepath: str, school: str, term: str):
    campus = "1"
    SchoolFlare = SCHOOL_FLARES[school]
    config_data = load_desired_sections(config_filepath)
    for desired_section in config_data:
        remaining_seats = SchoolFlare.get_remaining_seats(
            term,
            campus,
            desired_section.dept,
            desired_section.course_num,
            desired_section.section_num,
        )
        if remaining_seats:
            print("-".join(desired_section), "has", remaining_seats, "seats remaining!")


def send_email(
    from_email: str, from_pass: str, to_email: str, subj: str, body: str
) -> None:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(from_email, from_pass)
    try:
        server.sendmail(from_email, [to_email], body)
        print(body)
    except Exception as e:
        print(e)
    server.quit()


def notify_of_availability(
    section, src_email: str, src_pass: str, dest_email: str
) -> None:
    """
    Notifies the user of the availability of a certain section via email.
    """
    send_email(
        src_email,
        src_pass,
        dest_email,
        f"{section['courseReferenceNumber']} OPENED.",
        f"{section['subjectCourse']} {section['sequenceNumber']} - CRN: {section['courseReferenceNumber']}",
    )

    print(section["subjectCourse"], section["sequenceNumber"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Monitors the specified sections for an available seat."
    )
    parser.add_argument(
        "config_filepath", type=str, help="Path to the configuration file."
    )
    parser.add_argument(
        "school", type=str, choices=SCHOOL_FLARES.keys(), help="The school to monitor."
    )
    parser.add_argument("term", type=str, help="The term to search in.")

    args = parser.parse_args()
    main(args.config_filepath, args.school, args.term)

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     dest="src_email",
    #     type=str,
    #     help="The Gmail address to send the email from. MAKE SURE LESS-SECURE APPS CAN ACCESS THIS EMAIL.",
    # )
    # parser.add_argument(
    #     dest="src_pass", type=str, help="The password to provide along wih src_email",
    # )
    # parser.add_argument(
    #     dest="term_code",
    #     type=str,
    #     help="The 6-digit code used by TAMU to represent terms. Term codes are formatted as YYYYSU, where YYYY is the 4-digit year, S is the season (1=Spring, 2=Summer, 3=Fall), and U is the university (1=College Station, 2=Galveston, 3=Qatar)",
    # )
    # parser.add_argument(
    #     "-dest_email",
    #     dest="dest_email",
    #     default=None,
    #     type=str,
    #     help="The address to send emails to, if it differs from src_email.",
    # )
    # main(parser.parse_args())
