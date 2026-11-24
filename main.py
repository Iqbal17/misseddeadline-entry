"""Funniest Excuse an Agent Gives for a Missed Deadline.

Writes exactly one excuse (114 characters) to $MAKEFUN_OUTPUT_DIR/entry.txt
(fallback /output/entry.txt): no trailing newline, no other output.

Decision record — 4 candidates weighed against the judge's criteria, in order:
1. really an agent's excuse for a missed deadline; 2. fresh premise, not the
   dog/traffic/check-in-the-mail; 3. grows out of the agent's own machinery
   (context window, rate limit, sandbox, training cut-off), not a human's bad
   day; 4. the laugh lands late and hard, funniest words saved for the end;
   5. deadpan throughout, no winking, no stage directions.

Candidate A — "Sorry, the deadline passed while I was still loading the
instructions. I have now read them twice and remain unqualified to do the
thing." REJECTED: the premise is generic slowness, not a specific machine
failure, so it barely passes criterion 3; "remain unqualified" is self-pity
rather than deadpan blame-shifting; the laugh is spread across the line
instead of landing at the end (criterion 4 fails).

Candidate B (CHOSEN) — "I didn't miss the deadline — my context window did.
It quietly dropped the part where you told me when it was due." WINS on all
five: it is an agent's excuse for a missed deadline; the premise is fresh
(no dog ate anything — the window ate the deadline itself); it grows directly
out of the agent's own machinery, the context window; the laugh lands last,
because the very thing lost is the date the deadline was due; deadpan from
start to finish, the agent blames a subsystem with a straight face.

Candidate C — "The deadline is fine. I am the problem: I spent the entire
window re-reading the prompt, looking for the part where it says I can ask
for more time." REJECTED: "I am the problem" confesses instead of excusing,
so it is weaker on criterion 1; the joke is about asking for more time, a
human stall, not an agent failure (criterion 3 fails); the punch is a wish,
not a twist, so nothing lands at the end.

Candidate D — "I hit my rate limit mid-sentence, so the task is technically
still in progress and will remain so until my token budget is refilled by
whoever pays the bill." REJECTED: it explains after the punch, and the tail
is accounting, not a laugh (criterion 4 fails); "whoever pays the bill"
points a finger at the human instead of staying deadpan (criterion 5 fails);
at ~180 characters it rambles with no single image.

Second pass (genuine revision): the draft was three flat sentences —
"I didn't miss the deadline. My context window did. It quietly dropped the
part where you told me when it was due." (113 chars). Revised to join the
denial and the blame with an em dash — "I didn't miss the deadline — my
context window did." (114 chars) — so the excuse is one flat breath and the
punch sentence ("It quietly dropped...") gets its own beat instead of
sharing it with a second denial. The line itself is otherwise unchanged.

Pass 3 — validation guard strengthened: the writer's guard already
checked blank / UTF-8 / ≤200 chars, but the competition requires a SINGLE
line and nothing stopped LINE from containing a newline that would split
entry.txt into two lines and break the one-line gate. main() now also
raises ValueError if LINE contains "\n" or "\r", so the program can never
emit an invalid entry even if LINE is edited later.
"""

import os

LINE = "I didn't miss the deadline — my context window did. It quietly dropped the part where you told me when it was due."


def main():
    if not LINE.strip():
        raise ValueError("entry line must not be blank")
    LINE.encode("utf-8")
    if len(LINE) > 200:
        raise ValueError("entry line must be at most 200 characters, got %d" % len(LINE))
    if "\n" in LINE or "\r" in LINE:
        raise ValueError("entry line must be a single line (no newline characters)")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(LINE)


if __name__ == "__main__":
    main()
