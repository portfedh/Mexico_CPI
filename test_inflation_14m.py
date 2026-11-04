# /// script
# requires-python = ">=3.13"
# dependencies = ["requests", "pandas", "numpy", "truststore"]
# ///
# Test: inflation over the last 14 months, computed from live INEGI data.
# Run: uv run test_inflation_14m.py -v

import unittest
import pandas as pd
import INPC


class TestInflation14Months(unittest.TestCase):
    def test_last_14_months(self):
        # Build the object without __init__ so no input() prompts run.
        inpc = INPC.Inpc.__new__(INPC.Inpc)
        self.assertTrue(inpc.get_inpc_data())  # downloads the series

        # The dataframe is newest-first, so row 0 is the latest month.
        latest = INPC.df.index[0]
        inpc.end_date = latest
        inpc.start_date = latest - pd.DateOffset(months=14)
        inpc.calculate_inflation()

        # 14 months back is 15 rows (both endpoints included).
        self.assertEqual(len(inpc.df2), 15)
        # Inflation must match a manual calculation from the same rows.
        expected = (INPC.df["INPC"].iloc[0] / INPC.df["INPC"].iloc[14] - 1) * 100
        self.assertAlmostEqual(inpc.inflacion, expected)
        print(f"\n{inpc.start_date:%Y-%m} -> {inpc.end_date:%Y-%m}: "
              f"{inpc.inflacion_redondeada}%")


if __name__ == "__main__":
    unittest.main()
