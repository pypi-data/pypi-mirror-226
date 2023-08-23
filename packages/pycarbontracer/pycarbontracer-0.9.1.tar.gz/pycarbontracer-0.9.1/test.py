from unittest import TestCase, main
from configparser import ConfigParser

import json

from pycarbontracer import *

class TestHTTPRequest(TestCase):
    def test_http_request(self):
        http = HTTPRequest("https://httpbin.org/get")
        response = http.execute()
        self.assertEqual(response["headers"]["User-Agent"], http.USER_AGENT)

class TestCarbonTracer(TestCase):
    def setUp(self):
        self.config = ConfigParser()
        self.config.read("config.ini")
        self.carbontracer = CarbonTracer.from_config(self.config)

    def test_carbontracer_location(self):
        response = self.carbontracer.location("Graz")
        self.assertEqual(response["response"]["data"]["country"], "AT")

    def test_carbontracer_address(self):
        response = self.carbontracer.address("8010", "Graz", "Gartengasse")
        self.assertEqual(response["response"]["data"]["country"], "Austria")

    def test_carbontracer_routing(self):
        response = self.carbontracer.routing("car", "8010 Graz", "1010 Wien", waypoints=True)
        self.assertTrue("wayPoints" in response["response"]["data"])
        self.assertEqual(response["response"]["data"]["requestType"], "car")
        self.assertEqual(response["response"]["data"]["startLocation"]["postalCode"], "8010")

    def test_carbontracer_co2only(self):
        response = self.carbontracer.co2only("car", 100)
        self.assertEqual(response["response"]["data"]["distance"], 100)
        self.assertEqual(response["response"]["data"]["requestType"], "car")