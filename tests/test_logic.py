import unittest
from pricing_logic.material_db import get_material_cost
from pricing_logic.labor_calc import estimate_labor
from pricing_logic.vat_rules import get_vat_rate
from pricing_engine import generate_quote

class TestPricingLogic(unittest.TestCase):

    def test_material_cost(self):
        self.assertEqual(get_material_cost("lay ceramic tiles"), 25)
        self.assertEqual(get_material_cost("install toilet"), 120)
        self.assertEqual(get_material_cost("unknown task"), 10)

    def test_labor_estimation(self):
        cost, duration = estimate_labor("paint walls", "Paris")
        self.assertEqual(duration, "2h")
        self.assertAlmostEqual(cost, 96.0)  # 2h * 40 * 1.2

    def test_vat_rates(self):
        self.assertEqual(get_vat_rate("plumbing task"), 0.10)
        self.assertEqual(get_vat_rate("paint wall"), 0.20)

    def test_quote_generation(self):
        transcript = "Replace toilet and install vanity in Marseille"
        quote = generate_quote(transcript, city="Marseille")
        self.assertEqual(quote["zone"], "bathroom")
        self.assertTrue(len(quote["tasks"]) >= 2)
        for task in quote["tasks"]:
            self.assertIn("total_price", task)
            self.assertIn("confidence_score", task)

if __name__ == "__main__":
    unittest.main()
