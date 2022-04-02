# Run using:
# $ python3 -m unittest -v test_inpc.py

import unittest
import INPC
import api_key

# Tests
#################
#   1. Dataframe sin error
#   2. Fechas de consulta en rango


class TestINPC(unittest.TestCase):
    # Test Class that inherits from  unittest.testacse
    # Gives access to testing capabilities.

    # Test that api token is copied correctly
    def test_token(self):
        sourtce_token = api_key.token_inegi
        test_token = INPC.token
        self.assertEqual(sourtce_token, test_token)

    # Test that series is for monthly inflation
    def test_serie_consulta(self):
        serie = "628194"
        test_serie = INPC.inpc
        self.assertEqual(serie, test_serie)

    # Test that we are asking for all values, not latest value from API.
    def test_tipo_consulta(self):
        consulta = "false"  # Latest Value would be True, all values would be False
        test_consulta = INPC.consulta
        self.assertEqual(consulta, test_consulta)

    # Test the http status code
    def test_status(self):
        status = 200
        test_status = INPC.status
        self.assertEqual(test_status, status)


if __name__ == "__main__":
    unittest.main()
