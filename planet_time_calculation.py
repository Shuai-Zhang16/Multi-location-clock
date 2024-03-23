# coding: utf-8
from datetime import datetime, timedelta
from math import floor


class PlanetTimeCalculator:
    """Class to calculate the time on different planets in the solar system."""
    def __init__(self):
        # Initialize the length of a day and a year for each planet (relative to Earth)\
        # From https://spaceplace.nasa.gov/days/en/
        self.planet_day_lengths = {
            'Mercury': 58.6,    # A day on Mercury (in Earth days)
            'Venus': 243,       # A day on Venus
            'Earth': 1,         # A day on Earth in hours
            'Mars': 1.042,      # A day on Mars
            'Jupiter': 0.417,   # A day on Jupiter
            'Saturn': 0.458,    # A day on Saturn
            'Uranus': 0.708,    # A day on Uranus
            'Neptune': 0.67,    # A day on Neptune
            'Moon': 29.5        # A day on the Moon
        }

        # From https://spaceplace.nasa.gov/years-on-other-planets/en/
        self.planet_year_lengths = {
            'Mercury': 88,      # A year on Mercury (in Earth days)
            'Venus': 225,       # A year on Venus
            'Earth': 365,       # A year on Earth
            'Mars': 687,        # A year on Mars
            'Jupiter': 4333,    # A year on Jupiter
            'Saturn': 10759,    # A year on Saturn
            'Uranus': 30687,    # A year on Uranus
            'Neptune': 60190,   # A year on Neptune
            'Moon': 27          # A year on the Moon (orbit around Earth in days)
        }

    def calculate_planet_time(self, planet_name: str) -> str:
        """Calculate the current time on a planet in the solar system.

        :param planet_name: The name of the planet (e.g., 'Mars', 'Venus')
        :return: The string representing the current time on the planet
        """

        # Calculate planet time based on Earth time and planet name
        earth_time_now = datetime.utcnow()
        year_ratio = self.planet_year_lengths[planet_name] / self.planet_year_lengths['Earth']
        planet_year = int(earth_time_now.year * year_ratio)

        # Calculate the day of the year for the planet based on the Earth time
        earth_day_of_year = earth_time_now.timetuple().tm_yday
        planet_day_of_year = int(earth_day_of_year * self.planet_year_lengths[planet_name] / self.planet_year_lengths['Earth'])

        # Assume each planet month has equal days
        planet_day_per_month = floor(self.planet_year_lengths[planet_name] / 12)
        planet_month = int(planet_day_of_year / planet_day_per_month) + 1
        planet_day = int(planet_day_of_year % planet_day_per_month)

        # Adjust hours, minutes, and seconds based on planet day length based on Earth time
        planet_total_seconds = 86400 * self.planet_day_lengths[planet_name]
        earth_current_seconds = earth_time_now.hour * 3600 + earth_time_now.minute * 60 + earth_time_now.second
        planet_current_seconds = int(earth_current_seconds * planet_total_seconds / 86400)
        planet_current_hour = int(planet_current_seconds / 3600)
        planet_current_minute = int((planet_current_seconds % 3600) / 60)
        planet_current_second = (planet_current_seconds % 3600) % 60

        return (f"{planet_year}/{planet_month:02d}/{planet_day:02d} - "
                f"{planet_current_hour:02d}:{planet_current_minute:02d}:{planet_current_second:02d}")