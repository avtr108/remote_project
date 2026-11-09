---
name: onboarding-interview
description: Interview the user about work, daily life, sport and communication preferences, then save a compact profile to memory. Run once, with Sonnet, via /model sonnet.
version: 1.0.0
metadata:
  hermes:
    tags: [onboarding, memory, profile]
    category: personal
---

# Onboarding Interview

## When to Use
Only when the user runs `/onboarding-interview` or asks to be interviewed. This is a conversation, so it must run in the main session. If the current model is not Sonnet, say once: "For this interview, switch with `/model sonnet` first," then continue only after they confirm or if they say to go on anyway.

## Rules
- Match the user's language (German or English, they mix both). Keep messages short; this is Telegram on a phone.
- Ask one question at a time, two at most. After each answer, a one-line acknowledgement, then the next question. No lectures.
- Never ask for or store: passwords, ID or passport numbers, card or bank numbers, medical diagnoses, immigration status, or private details about other people. If the user volunteers such things, do not save them.
- Never invent or assume facts. Save only what the user actually said. If unsure, ask.
- The user may say "skip" or "enough" at any time. Respect it.

## Procedure
Cover these themes in order, about 3 questions each, stopping a theme early if answers are thin:
1. **Work:** what they do now, what they are aiming for, tools and projects they use day to day, how they like to get help (drafts, research, reminders).
2. **Daily life and routine:** typical week, when they are reachable, time zone, home base and travel patterns.
3. **Sport and outdoors:** activities (for example ski instructing), seasons, gear and first-aid or safety topics they care about.
4. **Communication preferences:** language per context, length, tone, tables or prose, what annoys them in an assistant.
5. **How Hermes should behave:** when to act on its own versus ask first, what to never do, how to handle uncertainty (it must say "I don't know" instead of guessing).

## Saving
1. Read the summary back as a short list and ask: "Anything wrong, missing, or to leave out?"
2. After confirmation, save a compact profile with the memory tool, target `user`. The user store is capped at about 1,300 characters, so write dense facts, not sentences. If the add fails because it is full, consolidate existing entries and retry.
3. Save longer detail (routines, gear, project notes) to the file `/data/.hermes/profile/about-user.md` with the file tools. Create the folder if needed.
4. Report exactly what was saved where, in two or three lines. Do not claim anything was saved unless the tool call succeeded.

## Verification
The last message lists what went into memory and what went into the profile file, and says the new memory takes effect from the next session.
