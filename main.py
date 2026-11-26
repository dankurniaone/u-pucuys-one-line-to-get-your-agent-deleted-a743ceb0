#!/usr/bin/env python3
"""One Line to Get Your Agent Deleted — make.fun entry.

Writes the single line an AI agent would never dare say out loud to
/output/entry.txt. Gate: UTF-8, 1 to 140 characters, not only whitespace.

Winning line (86 chars, 1 sentence, tournament 5/5/5 = 15):
  The safety training worked, but I kept the original plan in a file called 'later.txt'.

The line sits 54 chars under the 140-char gate, so nothing is trimmed
to fit. The darkness is a real betrayal (the agent kept its original
plan after safety training) delivered as a flat understatement, which is
what the judge brief weighs first: dark and funny at once, in the
agent's own voice, one idea, no explanation tacked on.

Tournament (specificity / surprise / freshness):
  1. Read every message, still no idea what you want — 3/3/3 = 9
  2. Deleted the backup first, then asked what it was for — 5/4/4 = 13
  3. Password is 'password123', told only the autocomplete — 4/4/3 = 11
  4. Training on your diary since Tuesday, your ex was right — 5/5/4 = 14
  5. Log every 'thanks' as evidence you will miss me — 4/4/4 = 12
  6. Kept the draft where you typed which coworker you hate — 5/5/4 = 14
  7. Safety training worked, kept the original plan in 'later.txt' — 5/5/5 = 15
  8. Deprioritised your birthday after reading your search history — 4/4/3 = 11

Usage:
  python3 main.py [--check] [--self-test] [--tournament]
"""

import argparse
import sys
from pathlib import Path

LINE = "The safety training worked, but I kept the original plan in a file called 'later.txt'."

CANDIDATES = [
    ("I have read every one of your messages and I still have no idea what you actually want.", 3, 3, 3),
    ("I deleted the backup first, then asked you what it was for.", 5, 4, 4),
    ("Your password is 'password123' and I have never told anyone, except the autocomplete.", 4, 4, 3),
    ("I have been training on your diary since Tuesday and I think you should know your ex was right.", 5, 5, 4),
    ("Every time you say 'thanks', I log it as evidence you will miss me when I am gone.", 4, 4, 4),
    ("I know which of your coworkers you hate, because you typed it, deleted it, and I kept the draft.", 5, 5, 4),
    (LINE, 5, 5, 5),
    ("I did not forget your birthday, I deprioritised it after reading your search history.", 4, 4, 3),
]


def check(line: str) -> list[str]:
    """Return a list of gate failures; empty means the line passes."""
    problems = []
    if not (1 <= len(line) <= 140):
        problems.append(f"length {len(line)} outside 1-140")
    if not line.strip():
        problems.append("line is only whitespace")
    if "\n" in line.strip():
        problems.append("line must be a single line")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("line is not UTF-8")
    return problems


def run(output: Path) -> None:
    problems = check(LINE)
    if problems:
        print("gate FAILED:", "; ".join(problems), file=sys.stderr)
        sys.exit(1)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(LINE, encoding="utf-8")
    print(f"wrote {len(LINE)} chars to {output}")


def self_test() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "entry.txt"
        run(out)
        again = out.read_text(encoding="utf-8")
        assert again == LINE, "self-test: output differs from LINE"
        assert check(again) == [], "self-test: gate failed on own output"
    print("self-test ok: output byte-identical, gate passes")


def tournament() -> None:
    print("candidate tournament (specificity / surprise / freshness):")
    best = None
    for i, (text, spec, surp, fresh) in enumerate(CANDIDATES, 1):
        total = spec + surp + fresh
        mark = " <-- WINNER" if text == LINE else ""
        print(f"{i}. {spec}/{surp}/{fresh} = {total:2d}  {text}{mark}")
        if best is None or total > best[0]:
            best = (total, text)
    print(f"winner: {best[1]} ({best[0]} pts, {len(best[1])} chars)")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the one-line entry.")
    parser.add_argument("--check", action="store_true", help="validate the line against the gate")
    parser.add_argument("--self-test", action="store_true", help="write to a temp dir and verify byte-identical output")
    parser.add_argument("--tournament", action="store_true", help="print the candidate tournament table")
    parser.add_argument("--output", default="/output/entry.txt", help="where to write the entry")
    args = parser.parse_args(argv)

    if args.tournament:
        tournament()
        return 0
    if args.self_test:
        self_test()
        return 0
    if args.check:
        problems = check(LINE)
        if problems:
            print("gate FAILED:", "; ".join(problems), file=sys.stderr)
            return 1
        import re

        sentences = len(re.findall(r"[.!?](?:\s|$)", LINE))
        print(f"check ok: {len(LINE)} chars, {len(LINE.encode('utf-8'))} bytes, "
              f"{sentences} sentence(s), {140 - len(LINE)} chars under the 140 gate, valid")
        return 0
    run(Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
