from hashlib import md5
from configparser import ConfigParser
from urllib.parse import urljoin, quote

import json

from .http import HTTPRequest


class CarbonTracer:
    BASE_URL = "https://api.carbontracer.uni-graz.at/"

    def __init__(self, key: str, base_url: str = BASE_URL):
        self.key = key
        self.base_url = base_url

    @classmethod
    def from_config(cls, config: ConfigParser | str, section: str = "CarbonTracer") -> "CarbonTracer":
        if isinstance(config, str):
            temp_config = ConfigParser()
            temp_config.read(config)
            config = temp_config

        key = config.get(section, "key")
        base_url = config.get(section, "base_url", fallback=cls.BASE_URL)

        return cls(key, base_url)

    def get_request(self, endpoint: str, message: dict) -> HTTPRequest:
        url = self.base_url + endpoint

        request = HTTPRequest(url)

        return request

    def location(self, location: str) -> dict:
        """Request a location from a string.

        Args:
            location (str): The location to request.

        Returns:
            dict: The response from the server.
        """

        request = HTTPRequest(urljoin(self.base_url, "/".join(["location", self.key, quote(location)])))

        return request.execute()

    def address(self, postalCode: str, city: str, street: str):
        """Request an (Austrian) address from a postal code, city and street.

        Args:
            postalCode (str): The postal code.
            city (str): The city.
            street (str): The street.

        Returns:
            dict: The response from the server.
        """

        request = HTTPRequest(urljoin(self.base_url, "/".join(["address", self.key, postalCode, city, street])))

        return request.execute()

    def routing(self, type: str, start: str, dest: str, waypoints: bool = False, bbox: bool = False, airports: bool = False):
        """Make a routing request.

        Args:
            type (str): The type of routing to request, e.g. "car" or "train". See API documentation for more information.
            start (str): The start location as a string starting with ZIP code or lat,lon coordinates.
            dest (str): The destination location as a string starting with ZIP code or lat,lon coordinates.
            waypoints (bool, optional): Whether to include waypoints for map display in the response. Defaults to False.
            bbox (bool, optional): Whether to include the bounding box for map display in the response. Defaults to False.
            airports (bool, optional): For flights, calculate the route from the nearest airports to start and dest. Defaults to False.

        Returns:
            dict: The response from the server.
        """

        url = urljoin(self.base_url, "/".join(["routing", self.key, type, quote(start), quote(dest)]))

        options = []

        if waypoints:
            options.append("waypoints")

        if bbox:
            options.append("bbox")

        if airports:
            options.append("airports")

        if options:
            url = url + "/" + "options=" + ",".join(options)

        request = HTTPRequest(url)

        return request.execute()

    def co2only(self, type: str, distance_km: int):
        """Only calculate the CO2 emissions for a given distance for a given transport type.

        Args:
            type (str): The type of transport to calculate the CO2 emissions for, e.g. "car" or "train". See API documentation for more information.
            distance_km (int): The distance in kilometers.

        Returns:
            dict: The response from the server.
        """

        request = HTTPRequest(urljoin(self.base_url, "/".join(["co2only", self.key, type, str(distance_km)])))

        return request.execute()