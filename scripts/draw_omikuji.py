#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "asakusa_omikuji.json"

FORTUNE_BUCKETS = {
    "大吉": "upper",
    "吉": "upper",
    "小吉": "middle",
    "半吉": "middle",
    "末吉": "middle",
    "末小吉": "middle",
    "凶": "lower",
}

DRAW_SUMMARIES = {
    "upper": "此签气象偏明，路数可开，但越在顺意处，越要守住分寸。",
    "middle": "此签不是骤然开门，而是缓缓见光，宜稳住心气，不可躁进。",
    "lower": "此签气象偏峭，不利强推，更像提醒你先止躁、避失、收束脚步。",
}

REDRAW_ELIGIBLE = {"凶", "半吉", "末吉", "末小吉"}

REDRAW_INVITATIONS = {
    "凶": "这一签若你不愿强留，可把它视作替你拦下一段逆气。若愿意，便行一回纳签重请，再请新签。",
    "default": "这一签若仍叫你心中发紧，也不必强留。可将旧签纳去，再请一签，换一重心气与路数。",
}

REDRAW_RITUAL_TEXT = (
    "销签不是抹去已经发生的事，而是把旧签所示的滞、急、逆，留在纸上，"
    "从此不再携它同行。"
)

REDRAW_SHIFT_TEXTS = {
    "upper": "新签偏明，表示此后这一路更宜守正而行。改写的不是过去，而是你从此刻起的步法与气象。",
    "middle": "新签转平，表示局面虽未大开，却已从逼仄转为可缓、可调、可扶正。改的是此后的行路之势。",
    "lower": "新签仍峭，也不必再逼着翻转。它提醒你今日之意在止，不在争；真正的转势，是肯把脚步收稳。",
}

OPENING_TEMPLATES = (
    "先把杂念放低一些，如晨烟拂过浅草寺的木檐，把一路行来的喧声都压得远了一层。签筒已静，木签未启，此刻不必急着向前，只需把心慢慢收拢。然后，我们来请这一签。",
    "不必多言，也不必先分辨吉凶。世间许多未定之事，此刻都可以先放在阶前，让香意替你压一压心上的浮动。你只管定住片刻，让木签先替你说话。",
    "世事先放在阶前，香意未散，签意未明，檐下的风也像比别处更轻一些。此刻不问来处，不问归处，只做一件事，轻轻启这一签。",
    "风从雷门外过，尘声渐歇，像有人把一整日的杂念都缓缓拂落。你不必急着把心事说破，只需把目光放低，把呼吸放稳。余下的，交给这一支签来开口。",
)

REVEAL_TEMPLATES = (
    "签筒既启，你得的是：第{sign_no}签 · {fortune_name}",
    "木签已出，眼前这一签是：第{sign_no}签 · {fortune_name}",
    "檐下启签，所得如下：第{sign_no}签 · {fortune_name}",
    "这一回落在你手中的，是：第{sign_no}签 · {fortune_name}",
)

DRAW_CLOSING_TEMPLATES = (
    "签意已明，路仍在你脚下。今日记得把心放稳一些。",
    "这一签照见的，不只是吉凶，也是在提醒你行路的姿势。",
    "若你信它，不妨信它替你拂去了一点浮躁，余下的路，再慢慢走。",
    "签纸至此可以轻轻收起，真正要走的路，仍要你自己一步一步踏稳。",
)

REDRAW_OPENING_TEMPLATES = (
    "旧签至此纳去，不再贴身。我们不问前尘，只问从这一刻起，路怎样改向。",
    "前一签已留在纸上，随香火一并安放。此刻重请，不为否认过去，只为另开一路。",
    "旧签已纳，旧气不再随身。如今再启一回，只看此后该如何行路。",
)

REDRAW_REVEAL_TEMPLATES = (
    "再启木签，新意已至：第{sign_no}签 · {fortune_name}",
    "销签之后，重新落下的是：第{sign_no}签 · {fortune_name}",
    "旧纸已留，新签已明：第{sign_no}签 · {fortune_name}",
)

REDRAW_CLOSING_TEMPLATES = (
    "旧签已留于旧纸，新意便从此刻起算。往后这一程，记得照着新签的气象去走。",
    "命不在一纸之间骤然改写，真正转过去的，是你从此刻起携带的心与步。",
    "销去的，是不必再背的旧滞；留下的，是此后可慢慢扶正的新路数。",
)


def load_fortunes() -> list[dict[str, str | int]]:
    with DATA_PATH.open(encoding="utf-8") as data_file:
        fortunes = json.load(data_file)
    if len(fortunes) != 100:
        raise ValueError(f"expected 100 fortunes, got {len(fortunes)}")
    return fortunes


def parse_guidance(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "：" in line:
            label, value = line.split("：", 1)
        else:
            label, value = "补充", line
        items.append({"label": label.strip(), "value": value.strip()})
    return items


def resolve_bucket(fortune_name: str) -> str:
    return FORTUNE_BUCKETS.get(fortune_name, "middle")


def pick_template(options: tuple[str, ...], *keys: object) -> str:
    marker = "".join(str(key) for key in keys)
    index = sum(ord(char) for char in marker) % len(options)
    return options[index]


def pack_fortune(record: dict[str, str | int]) -> dict[str, str | int]:
    return {
        "签号": record["签号"],
        "吉凶": record["吉凶"],
        "诗曰": record["诗曰"],
        "四句解说": record["四句解说"],
        "解曰": record["解曰"],
    }


def choose_fortune(
    fortunes: list[dict[str, str | int]],
    sign_no: int | None = None,
    seed: int | None = None,
    exclude_sign_no: int | None = None,
) -> dict[str, str | int]:
    pool = [
        record for record in fortunes if exclude_sign_no is None or record["签号"] != exclude_sign_no
    ]
    if not pool:
        raise ValueError("fortune pool is empty after exclusions")

    if sign_no is not None:
        if exclude_sign_no is not None and sign_no == exclude_sign_no:
            raise ValueError("new sign must differ from the destroyed sign")
        if not 1 <= sign_no <= len(fortunes):
            raise ValueError(f"sign number must be between 1 and {len(fortunes)}")
        return fortunes[sign_no - 1]

    if seed is None:
        return random.SystemRandom().choice(pool)
    rng = random.Random(seed)
    return rng.choice(pool)


def should_offer_redraw(record: dict[str, str | int]) -> bool:
    return str(record["吉凶"]) in REDRAW_ELIGIBLE


def build_redraw_offer(record: dict[str, str | int]) -> dict[str, object]:
    if not should_offer_redraw(record):
        return {"offered": False}

    fortune_name = str(record["吉凶"])
    invitation = REDRAW_INVITATIONS.get(fortune_name, REDRAW_INVITATIONS["default"])
    return {
        "offered": True,
        "invitation": invitation,
        "ritual": REDRAW_RITUAL_TEXT,
        "fate_shift_hint": "重请之后，变的不是已经发生的过去，而是你从此刻起所携带的心气与行路之势。",
    }


def build_fate_shift(
    previous_record: dict[str, str | int],
    new_record: dict[str, str | int],
) -> dict[str, str]:
    new_bucket = resolve_bucket(str(new_record["吉凶"]))
    return {
        "destroyed_sign_meaning": (
            f"前一签第{previous_record['签号']}签所示的滞气与提醒，至此留在旧纸上，不再贴身同行。"
        ),
        "new_path_meaning": REDRAW_SHIFT_TEXTS[new_bucket],
    }


def build_payload(
    record: dict[str, str | int],
    previous_record: dict[str, str | int] | None = None,
) -> dict[str, object]:
    guidance_items = parse_guidance(str(record["解曰"]))
    bucket = resolve_bucket(str(record["吉凶"]))
    payload: dict[str, object] = {
        "mode": "redraw" if previous_record is not None else "draw",
        "fortune_bucket": bucket,
        "summary": DRAW_SUMMARIES[bucket],
        "guidance": guidance_items,
        "fortune": pack_fortune(record),
    }

    if previous_record is None:
        payload["redraw"] = build_redraw_offer(record)
        payload["ceremony"] = {
            "opening": pick_template(OPENING_TEMPLATES, "draw", record["签号"], record["吉凶"]),
            "reveal": pick_template(
                REVEAL_TEMPLATES,
                "reveal",
                record["签号"],
                record["吉凶"],
            ).format(sign_no=record["签号"], fortune_name=record["吉凶"]),
            "closing": pick_template(
                DRAW_CLOSING_TEMPLATES,
                "closing",
                record["签号"],
                record["吉凶"],
            ),
        }
    else:
        payload["previous_fortune"] = pack_fortune(previous_record)
        payload["fate_shift"] = build_fate_shift(previous_record, record)
        payload["ceremony"] = {
            "opening": pick_template(
                REDRAW_OPENING_TEMPLATES,
                "redraw-opening",
                previous_record["签号"],
                record["签号"],
            ),
            "reveal": pick_template(
                REDRAW_REVEAL_TEMPLATES,
                "redraw-reveal",
                previous_record["签号"],
                record["签号"],
                record["吉凶"],
            ).format(sign_no=record["签号"], fortune_name=record["吉凶"]),
            "closing": pick_template(
                REDRAW_CLOSING_TEMPLATES,
                "redraw-closing",
                previous_record["签号"],
                record["签号"],
                record["吉凶"],
            ),
        }

    return payload


def to_text(payload: dict[str, object]) -> str:
    fortune = payload["fortune"]
    guidance = payload["guidance"]
    ceremony = payload["ceremony"]

    if payload["mode"] == "redraw":
        previous = payload["previous_fortune"]
        fate_shift = payload["fate_shift"]
        lines = [
            str(ceremony["opening"]),
            "",
            f"旧签已纳：第{previous['签号']}签 · {previous['吉凶']}",
            fate_shift["destroyed_sign_meaning"],
            "",
            str(ceremony["reveal"]),
            "",
            "诗曰：",
            str(fortune["诗曰"]),
            "",
            "签意：",
            str(payload["summary"]),
            str(fortune["四句解说"]),
        ]
        if guidance:
            lines.append("")
            lines.append("解曰：")
            for item in guidance:
                lines.append(f"- {item['label']}：{item['value']}")
        lines.extend(["", "转势：", fate_shift["new_path_meaning"], "", str(ceremony["closing"])])
        return "\n".join(lines)

    lines = [
        str(ceremony["opening"]),
        "",
        str(ceremony["reveal"]),
        "",
        "诗曰：",
        str(fortune["诗曰"]),
        "",
        "签意：",
        str(payload["summary"]),
        str(fortune["四句解说"]),
    ]

    if guidance:
        lines.append("")
        lines.append("解曰：")
        for item in guidance:
            lines.append(f"- {item['label']}：{item['value']}")

    redraw = payload.get("redraw", {})
    if isinstance(redraw, dict) and redraw.get("offered"):
        lines.extend(
            [
                "",
                "若你不欲留此签：",
                str(redraw["invitation"]),
                str(redraw["ritual"]),
                str(redraw["fate_shift_hint"]),
            ]
        )

    lines.extend(["", str(ceremony["closing"])])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw a real Asakusa Temple omikuji.")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--sign-no", type=int, help="Return a specific lot number.")
    mode_group.add_argument(
        "--redraw-from-sign",
        type=int,
        help="Destroy the previous sign and draw a new one.",
    )
    parser.add_argument("--seed", type=int, help="Deterministic seed for testing.")
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output format.",
    )
    args = parser.parse_args()

    fortunes = load_fortunes()

    if args.redraw_from_sign is not None:
        previous_record = choose_fortune(fortunes, sign_no=args.redraw_from_sign)
        new_record = choose_fortune(
            fortunes,
            seed=args.seed,
            exclude_sign_no=args.redraw_from_sign,
        )
        payload = build_payload(new_record, previous_record=previous_record)
    else:
        record = choose_fortune(fortunes, sign_no=args.sign_no, seed=args.seed)
        payload = build_payload(record)

    if args.format == "text":
        print(to_text(payload))
        return

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
