from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from draw_omikuji import (  # noqa: E402
    build_payload,
    choose_fortune,
    load_fortunes,
    parse_guidance,
    should_offer_redraw,
    to_text,
)


class DrawOmikujiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fortunes = load_fortunes()

    def test_loads_all_fortunes(self) -> None:
        self.assertEqual(100, len(self.fortunes))

    def test_choose_specific_sign(self) -> None:
        record = choose_fortune(self.fortunes, sign_no=1)
        self.assertEqual(1, record["签号"])
        self.assertEqual("大吉", record["吉凶"])

    def test_parse_guidance(self) -> None:
        items = parse_guidance("愿望：会实现吧。\n交往：要谨慎。")
        self.assertEqual("愿望", items[0]["label"])
        self.assertEqual("会实现吧。", items[0]["value"])
        self.assertEqual("交往", items[1]["label"])

    def test_lower_fortune_offers_redraw(self) -> None:
        record = choose_fortune(self.fortunes, sign_no=3)
        self.assertTrue(should_offer_redraw(record))
        payload = build_payload(record)
        self.assertTrue(payload["redraw"]["offered"])

    def test_upper_fortune_does_not_offer_redraw(self) -> None:
        record = choose_fortune(self.fortunes, sign_no=1)
        self.assertFalse(should_offer_redraw(record))
        payload = build_payload(record)
        self.assertFalse(payload["redraw"]["offered"])
        self.assertIn("opening", payload["ceremony"])
        self.assertIn("reveal", payload["ceremony"])
        self.assertIn("closing", payload["ceremony"])
        self.assertGreaterEqual(len(payload["guidance"]), 5)

    def test_redraw_builds_previous_and_new_fortunes(self) -> None:
        previous_record = choose_fortune(self.fortunes, sign_no=3)
        new_record = choose_fortune(self.fortunes, seed=12, exclude_sign_no=3)
        payload = build_payload(new_record, previous_record=previous_record)
        self.assertEqual("redraw", payload["mode"])
        self.assertEqual(3, payload["previous_fortune"]["签号"])
        self.assertNotEqual(
            payload["previous_fortune"]["签号"],
            payload["fortune"]["签号"],
        )
        self.assertIn("旧纸", payload["fate_shift"]["destroyed_sign_meaning"])

    def test_text_output_uses_ceremony_lines(self) -> None:
        record = choose_fortune(self.fortunes, sign_no=1)
        payload = build_payload(record)
        text = to_text(payload)
        self.assertIn(payload["ceremony"]["opening"], text)
        self.assertIn(payload["ceremony"]["reveal"], text)
        self.assertIn(payload["ceremony"]["closing"], text)
        self.assertIn("疾病：会治愈吧。", text)
        self.assertIn("盼望的人：会出现吧。", text)


if __name__ == "__main__":
    unittest.main()
