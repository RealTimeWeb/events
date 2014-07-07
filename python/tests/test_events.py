import unittest

import sys

sys.path.append("../src")

try:
    import events
except ImportError:
    from python.src import events


class TestEvents(unittest.TestCase):
    def test_method_online(self):
        events.connect()
        events._start_editing()

        keys = ['actor1 name',
                'actor1 latitude',
                'actor1 longitude',
                'actor2 name',
                'actor2 latitude',
                'actor2 longitude',
                'average tone',
                'event code',
                'SQLDATE']

        item = events.get_events_information("Actor1Geo_FullName==\"New York, "
                                             "United States\"")
        self.assertTrue(isinstance(item, list))

        # Assert all of the keys are in item
        intersection = set(keys).intersection(item[0])
        self.assertEqual(9, len(intersection))

        events._save_cache("../src/events_cache.json")

    def test_method_offline(self):
        events.disconnect("../src/events_cache.json")

        keys = ['actor1 name',
                'actor1 latitude',
                'actor1 longitude',
                'actor2 name',
                'actor2 latitude',
                'actor2 longitude',
                'average tone',
                'event code',
                'SQLDATE']

        item = events.get_events_information("Actor1Geo_FullName==\"New York, "
                                             "United States\"")
        self.assertTrue(isinstance(item, list))

        # Assert all of the keys are in item
        intersection = set(keys).intersection(item[0])
        self.assertEqual(9, len(intersection))

    def test_throw_exception(self):
        events.connect()

        with self.assertRaises(events.EventsException) as context:
            events.get_events_information("Hello")

        self.assertEqual('Make sure you entered a valid query',
                         context.exception.args[0])

        with self.assertRaises(events.EventsException) as context:
            events.get_events_information(1)
        self.assertEqual('Please enter a valid query',
                         context.exception.args[0])

        with self.assertRaises(events.EventsException) as context:
            events.get_events_information("Actor1Geo_FullName==Herndon")

        self.assertEqual('There were no results', context.exception.args[0])
