import abc
from typing import Optional


class Flare(abc.ABC):
    """
    A base tracker for classes.
    """

    @abc.abstractmethod
    def get_remaining_seats(
        self,
        term: Optional[str] = None,
        campus: Optional[str] = None,
        dept: Optional[str] = None,
        course_num: Optional[str] = None,
        section_num: Optional[str] = None,
    ) -> int:
        pass
