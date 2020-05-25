import enum
from typing import Optional

import bs4
import requests

from flares import flare


class Campus(enum.Enum):
    ALL = "All"
    TCC_CONNECT = "CN"
    ELEARNING_ONLY = "DL"
    NORTHEAST = "NE"
    NORTHWEST = "NW"
    SOUTHEAST = "SE"
    SOUTH = "SO"
    TRINITY_RIVER = "TR"


class TCCFlare(flare.Flare):
    """
    A Flare for Tarrant County College (https://www.tccd.edu/)
    """

    HOSTNAME = "https://waj.tccd.edu"
    PATH = "/TCC/WebAdvisor3/getSection.jsp"
    SEARCH_URL = HOSTNAME + PATH

    @classmethod
    def get_remaining_seats(
        self, term: str, campus: str, dept: str, course_num: str, section_num: str,
    ) -> int:
        params = {
            "term": term,
            "selectCampus": campus,
            "course": f"{dept}-{course_num}",
        }
        r = requests.get(TCCFlare.SEARCH_URL, params=params)
        soup = bs4.BeautifulSoup(r.content, "lxml")
        rows = soup.select("#courseForm > table:nth-child(1) > tr")
        rows = rows[4:]
        expected_code = "-".join([dept, course_num, section_num])
        for row in rows:
            cells = row.select("td")
            if len(cells) == 1:
                continue
            dept_course_section_cell = cells[3]
            seats_remaining_cell = cells[8]
            dept_course_section = dept_course_section_cell.text.strip()
            seats_remaining = int(seats_remaining_cell.text.strip())

            if expected_code == dept_course_section:
                return seats_remaining
