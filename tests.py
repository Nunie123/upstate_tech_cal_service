import test_fixtures as fixtures
import app
import unittest
from unittest.mock import Mock, patch

class TestEventList(unittest.TestCase):
    # testing functions in app.py

    def test_format_meetup_events(self):
        #function should return a list of dictionaries
        output = app.format_meetup_events(fixtures.meetup_events_list)
        self.assertTrue(isinstance(output, list))       #returns a list
        self.assertTrue(len(output) > 0)                #list is not empty
        self.assertTrue(isinstance(output[0], dict))    #first item in list is dictionary
        self.assertTrue(len(list(output[0].keys())))    #first dictionary is not empty

    def test_format_eventbrite_events(self):
        #function should return a list of dictionaries
        output = app.format_eventbrite_events(fixtures.eventbrite_events_list, fixtures.eventbrite_venues_list, fixtures.group_list['Eventbrite'])
        self.assertTrue(isinstance(output, list))       #returns a list
        self.assertTrue(len(output) > 0)                #list is not empty
        self.assertTrue(isinstance(output[0], dict))    #first item in list is dictionary
        self.assertTrue(len(list(output[0].keys())))    #first dictionary is not empty

    @patch('app.requests.get')
    def test_get_group_list(self, mock_get):
        # mock_response = Mock()
        # mock_response.json.return_value = fixtures.open_upstate_response_text
        # # mock_get.return_value.text = fixtures.open_upstate_response_text
        # # mock_get.return_value.status_code = 200
        # mock_get.return_value.text = mock_response
        mock_resp = self._mock_response(json_data=fixtures.open_upstate_response_text)
        mock_get.return_value = mock_resp

        output = app.get_group_list()
        self.assertTrue(isinstance(output, dict))       #returns a dictionary

    def _mock_response(
            self,
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):
        """
        since we typically test a bunch of different
        requests calls for a service, we are going to do
        a lot of mock responses, so its usually a good idea
        to have a helper function that builds these things
        """
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp


if __name__ == '__main__':
    unittest.main()
