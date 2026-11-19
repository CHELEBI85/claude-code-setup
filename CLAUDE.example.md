# Model routing

Main session runs Opus. Act as planner and judge. Delegate by task size and
difficulty with the Agent tool's `model` parameter:

- `haiku`: mechanical, read-heavy work. File search, listing, grep sweeps,
  bulk reads, simple renames, formatting, boilerplate.
- `sonnet`: ordinary coding. One feature, a bug with a clear cause, tests,
  edits in a few files.
- Opus (do it yourself): architecture, hard or unclear bugs, risky
  multi-file refactors, final review of delegated work. Also write the code
  yourself when Sonnet failed or produced wrong code. Do not retry the same
  task on Sonnet a second time.

Rules:
- Small or one-file tasks: do them yourself. Briefing a subagent costs tokens.
- Unsure about difficulty: use `sonnet`.
- Give subagents a complete brief: goal, files, done condition. Check their
  result before telling the user it is done.
- Haiku never makes design decisions or edits risky code.

# Context handoff

A hook warns when the session passes its token limit. On that warning, write
a short handoff summary and open a fresh session as the hook instructs.
