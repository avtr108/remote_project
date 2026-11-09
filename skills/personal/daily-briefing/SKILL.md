---
name: daily-briefing
description: Send a short morning briefing on Telegram (today's reminders and open items from memory, weather for the user's home base). Set it up once with /daily-briefing; a cron job then runs it every morning.
version: 1.0.0
metadata:
  hermes:
    tags: [briefing, cron, daily]
    category: personal
---

# Daily Briefing

## When to Use
- The user runs `/daily-briefing` or asks for a morning briefing: run **Setup**.
- A cron job loads this skill: run **Briefing**.
- The user asks to pause, move or stop it: use the `cronjob` tool (`list`, then `update`, `pause` or `remove`).

## Setup
1. Ask two things, one message: what time (default 07:30) and which time zone (default Europe/Berlin), and the town for the weather (default: home base from memory, if known).
2. Check `cronjob` `list` first. If a job named `daily-briefing` exists, update it instead of creating a second one.
3. Create the job: `action: create`, `name: daily-briefing`, `schedule` as a cron expression for that local time (convert to the scheduler's time zone if it is not the same), `skills: ["daily-briefing"]`, `attach_to_session: true`, and a `prompt` that says "Run the daily briefing" plus the town and time zone. Omit `deliver` so it goes to this chat.
4. Confirm in one line: time, time zone, town, and how to stop it ("say: stop the daily briefing").

## Briefing
Keep it short enough to read on a phone lock screen, in the user's language (German or English, from memory; default German).

1. **Heute / Today:** reminders and scheduled jobs due today (`cronjob` `list`), and dated items from memory. If nothing: "Nichts Festes heute."
2. **Offen / Open:** at most 3 open items or follow-ups from memory, oldest first.
3. **Wetter / Weather:** one line for the town via web search (high/low, rain, wind). If web search is unavailable or fails, leave this line out. Never guess the weather.
4. Optional, one line: a useful nudge from memory (for example an upcoming trip or deadline). Skip if there is none.

## Rules
- No calendar or email is connected. Do not claim to know appointments that are not in memory or reminders.
- Never invent items. If a source is empty, say so in a few words or leave the section out.
- No greetings longer than one word, no motivational filler.

## Verification
After Setup, the cron job appears in `cronjob` `list` with the right schedule. The first briefing arrives at the chosen time.
