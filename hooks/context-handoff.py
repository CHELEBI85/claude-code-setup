#!/usr/bin/env python3
"""UserPromptSubmit hook: when context passes a token threshold, tell Claude to
write a handoff summary and open a fresh session. Silent below the threshold.

Config: env CONTEXT_HANDOFF_TOKENS (default 100000).
Fires once per session, again after each extra STEP tokens.
"""
import json
import os
import sys

THRESHOLD = int(os.environ.get("CONTEXT_HANDOFF_TOKENS", "100000"))
STEP = 25000


def main():
    try:
        data = json.load(sys.stdin)
        path = data.get("transcript_path")
        sid = data.get("session_id", "unknown")
        if not path or not os.path.exists(path):
            return
        used = 0
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                msg = d.get("message")
                if d.get("isSidechain") or not isinstance(msg, dict):
                    continue
                u = msg.get("usage")
                if isinstance(u, dict):
                    used = (
                        u.get("input_tokens", 0)
                        + u.get("cache_creation_input_tokens", 0)
                        + u.get("cache_read_input_tokens", 0)
                    )
        if used < THRESHOLD:
            return

        marker = os.path.join(os.path.expanduser("~/.claude"), "hooks", ".handoff-state.json")
        try:
            with open(marker, encoding="utf-8") as f:
                state = json.load(f)
        except (OSError, ValueError):
            state = {}
        if used < state.get(sid, 0) + STEP and sid in state:
            return
        state[sid] = used
        # Keep the state file small.
        state = dict(list(state.items())[-50:])
        try:
            with open(marker, "w", encoding="utf-8") as f:
                json.dump(state, f)
        except OSError:
            pass

        msg = (
            f"CONTEXT HANDOFF: this session holds about {used:,} tokens, over the "
            f"{THRESHOLD:,} limit. Finish the current step. Then write a short handoff "
            "summary (goal, done, open work, key files, decisions) and continue in a "
            "fresh session: call mcp__ccd_session__start_session with that summary as "
            "the brief, context \"fresh\". If that tool is unavailable (terminal), save "
            "the summary to HANDOFF.md in the project and tell the user to run /clear "
            "and read it. Tell the user in one line that you are doing this."
        )
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": msg,
        }}))
    except Exception:
        # Never block the prompt because of this hook.
        return


main()
