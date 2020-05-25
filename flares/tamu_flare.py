import argparse
import json
import smtplib
import time
from pprint import pprint
from typing import Dict, List, Optional

import requests

from flares import flare


class TAMUFlare(flare.Flare):
    """
    A Flare for Texas A&M University
    """

    HOME_URL = "https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/registration"

    POST_TERM_CODE_URL = "https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/term/search?mode=courseSearch"

    GET_SECTION_INFO_URL = "https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_subjectcoursecombo={}&txt_term={}&pageOffset=0&pageMaxSize=500&sortColumn=subjectDescription&sortDirection=asc"

    def get_remaining_seats(
        self, term: str, campus: str, dept: str, course_num: str, section_num: str,
    ) -> Optional[int]:
        r: requests.Response = requests.get(TAMUFlare.HOME_URL)
        r: requests.Response = requests.post(
            TAMUFlare.POST_TERM_CODE_URL, data={"dataType": "json", "term": term}
        )
        cookies = r.cookies

        r: requests.Response = requests.get(
            TAMUFlare.GET_SECTION_INFO_URL.format(dept + "" + course_num, term),
            cookies=cookies,
        )
        sections = r.json()["data"]
        for section in sections:
            if section["sequenceNumber"] == section_num:
                return section["seatsAvailable"]
