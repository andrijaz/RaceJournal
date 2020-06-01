from django.db import models
from time import gmtime, strftime

RACE_LENGTH = [(5, "fun"),
               (10, "10k"),
               (21, "halfmarathon"),
               (42, "marathon"),
               (50, "ultra"),
               (100, "long ultra")]

RACE_TYPE = [("road", "road"),
             ("trail", "trail"),
             ("triathlon", "triathlon")]

CLUB_CHOICES = [("BRC", "BRC"), ("TRIBE", "TRIBE"), ("ADIDAS", "ADIDAS")]
TROPHY_CHOICES = [("first halfmarathon", "first halfmarathon"),
                  ("first marathon", "first marathon"),
                  ("first race", "first race"),
                  ("first trail", "first trail")]


class RaceType(models.TextChoices):
    road = "road"
    trail = "trail"
    triathlon = "triathlon"


class RaceLength(models.IntegerChoices):
    # Mozda ostaviti jer je lepse za rad, ali kako da se dodaju nove duzine
    five = 5
    ten = 10
    halfmarathon = 21
    marathon = 42
    ultra = 50
    longultra = 100


def sec_to_human(seconds):
    """Format seconds to hours, minutes, seconds for it to bee human readable.

    Args:
        seconds (float or int): Seconds to convert.

    Returns:
        dict[int, int, int]: {"hours": h, "minutes": m, "seconds": s}
    """
    h, m, s = strftime("%H:%M:%S", gmtime(seconds)).split(":")
    return {"hours": h, "minutes": m, "seconds": s}


def human_to_seconds(h=0, m=0, s=0) -> int:
    """Convert hours, minutes and seconds to seconds for storing in db.

    Args:
        h (int): Hours, optional.
        m (int): Minutes, optional.
        s (int): Seconds, optional

    Returns:
        race_time (int): Race time in seconds.
    """
    hours = int(h)
    minutes = int(m)
    seconds = int(s)
    race_time = hours * 3600 + minutes * 60 + seconds

    return race_time

def get_type_from_length(race_len: int) -> str:
    """Convert race length from number to str.

    Examples:
        21 -> halfmarathon

    Args:
        race_len (int): Number to search and convert.

    Returns:
        name_len (str): Name of race length or None.
    """
    for number_len, name_len in RACE_LENGTH:
        if number_len==race_len:
            return name_len
    return None