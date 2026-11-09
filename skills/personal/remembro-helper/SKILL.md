---
name: remembro-helper
description: Answer quick questions about the user's Remembro project (product, scope, stack, where docs live) from a built-in snapshot, and capture ideas for it. Use when the user mentions Remembro.
version: 1.0.0
metadata:
  hermes:
    tags: [remembro, project, product]
    category: personal
---

# Remembro Helper

## When to Use
The user asks about Remembro, wants to think through a product idea, or wants to note something for the project while on the go.

## Limits (say these when relevant)
- The repo `github.com/avtr108/Remembro` is private and Hermes has no GitHub access. Everything below is a snapshot from 2026-11-09; anything newer (open PRs, current version, state) you do not know. Say "I don't know, check the repo" instead of guessing.
- Do not write code for Remembro here. Coding happens in Claude Code sessions on the repo.

## Snapshot (2026-11-09)
- **What it is:** a second brain for relationships, commitments and future intentions. Tagline: "Remember less. Get more back." Everything starts with one sentence ("Sarah borrowed my surfboard for the weekend"), which becomes a structured **Entry** with a reminder.
- **Entry-centric:** every feature starts from an Entry. Domain truth: `docs/04_DOMAIN_MODEL.md`.
- **MVP goal:** "Help people get their things back." Core type: borrowed and lent items. Success: create an Entry, pick a contact and channel, preview a message, schedule or send, get reminded and mark it returned, all in under a minute. Scope: `docs/07_MVP.md`. `docs/09_TEAMS.md` and `docs/10_FUTURE_IDEAS.md` are vision, not tasks.
- **Must work without AI.**
- **Stack:** pnpm + Turborepo monorepo, TypeScript, React 18 + Vite 5 frontend (EN/DE via i18next, PWA), Fastify backend on Railway with Postgres, Cloudflare Workers for feedback and the PO dashboard, frontend on All-Inkl, CI on GitHub Actions.
- **Version:** 0.10.4 in the repo as of the snapshot. Alpha at `alphatest.techtimize.de`.
- **Docs map:** `docs/01_POSITIONING.md` → `02_PRD.md` → `03_PRODUCT_PRINCIPLES.md` → `05_UX_ARCHITECTURE.md`; current state `ai/STATE.md`; next work `ai/NEXT_ISSUE.md`; changes `CHANGELOG.md`.

## Capturing ideas
When the user shares an idea, bug or task for Remembro:
1. Restate it in one line and ask if anything is missing.
2. Append it to `/data/.hermes/profile/remembro-inbox.md` as `- YYYY-MM-DD: <one line>` (create the file if needed). Confirm only after the write succeeded.
3. When the user asks "what's in my Remembro inbox", read that file back. Remind them to move items into GitHub Issues from a coding session.

## Thinking through ideas
Check the idea against the MVP goal and the entry-centric rule first. If it is outside MVP scope, say so plainly and suggest parking it under future ideas.
