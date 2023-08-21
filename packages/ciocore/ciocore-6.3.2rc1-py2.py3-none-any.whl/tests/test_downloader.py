
from ciocore.downloader import Downloader
import unittest
from unittest import mock

class TestDownloaderFlatten(unittest.TestCase):
    
    def test_flatten_single_job_id(self):
        input = ("01234",)
        result = Downloader._flatten(input)
        self.assertEqual(result, [{"job_id": "01234", "tasks":None}])

    def test_flatten_pad_job_id(self):
        input = ("1234",)
        result = Downloader._flatten(input)
        self.assertEqual(result, [{"job_id": "01234", "tasks":None}])

    def test_several_job_ids(self):
        input = ("1234","1235","1236")
        result = Downloader._flatten(input)
        self.assertEqual(result, [
            {"job_id": "01234", "tasks":None},
            {"job_id": "01235", "tasks":None},
            {"job_id": "01236", "tasks":None}
            ])

    def test_job_and_tasks(self):
        input = ("1234:1-7x2,10",)
        result = Downloader._flatten(input)
        self.assertEqual(result, [{"job_id": "01234", "tasks":["001","003","005","007","010"]}])

    def test_several_job_and_tasks(self):
        input = ("1234:1-7x2,10","1235:12-15")
        result = Downloader._flatten(input)
        self.assertEqual(result, [
            {"job_id": "01234", "tasks":["001","003","005","007","010"]},
            {"job_id": "01235", "tasks":["012","013","014","015"]}
            ])

    def test_mix_job_and_job_with_tasks(self):
        input = ("1234","1235:12-15")
        result = Downloader._flatten(input)
        self.assertEqual(result, [
            {"job_id": "01234", "tasks":None},
            {"job_id": "01235", "tasks":["012","013","014","015"]}
            ])

    def test_invalid_range_downloads_whole_job(self):
        # Someone might have a bunch of stuff queued up and made a mistake and left for the night.
        # We should download the whole job in this case so they don't have to restart the dl in the
        # morning.
        input = ("1234:badrange",)
        result = Downloader._flatten(input)
        self.assertEqual(result, [
            {"job_id": "01234", "tasks":None}
            ])
