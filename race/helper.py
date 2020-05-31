from django.db import models
from time import gmtime, strftime

RACE_LENGTH = [(5, 5), (10, 10), (21, 21.1), (42, 42.2), (50, 50), (100, 100)] #TODO change to strings (5, fun), (10, short), (21, halfmartahon)
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
        seconds (int):

    Returns:
        dict[int, int, int]: Contains `hours`, `minutes`, `seconds`
    """
    h, m, s = strftime("%H:%M:%S", gmtime(seconds)).split(":")
    return {"hours": h, "minutes": m, "seconds": s}


def human_to_seconds(hours, minutes, seconds):
    hours = int(hours) if hours else 0
    minutes = int(minutes) if minutes else 0
    seconds = int(seconds) if seconds else 0
    race_time = hours * 3600 + minutes * 60 + seconds

    return race_time
