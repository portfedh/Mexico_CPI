# /// script
# requires-python = ">=3.13"
# dependencies = ["requests", "pandas", "numpy", "truststore"]
# ///
# Run using:
# $ uv run test_inpc.py -v

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
        test_token = INPC.Inpc.token
        self.assertEqual(sourtce_token, test_token)

    # Test that series is for monthly inflation
    def test_serie_consulta(self):
        serie = "910392"
        test_serie = INPC.Inpc.inpc
        self.assertEqual(serie, test_serie)

    # Test that we are asking for all values, not latest value from API.
    def test_tipo_consulta(self):
        consulta = "false"  # Latest Value would be True, all values would be False
        test_consulta = INPC.Inpc.consulta
        self.assertEqual(consulta, test_consulta)

    # Test the http status code. get_inpc_data() sets the global INPC.status;
    # __new__ skips __init__ so no input() prompts run.
    def test_status(self):
        status = 200
        INPC.Inpc.__new__(INPC.Inpc).get_inpc_data()
        test_status = INPC.status
        self.assertEqual(test_status, status)


if __name__ == "__main__":
    unittest.main()
