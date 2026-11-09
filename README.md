# hermes_personal

Personal Hermes Agent on Railway. Based on [arjunkomath/hermes-agent-railway-template](https://github.com/arjunkomath/hermes-agent-railway-template), image pinned to the official `nousresearch/hermes-agent` release.

## Model routing (`hermes-overlay.yaml`)

| Role | Model |
|---|---|
| Main loop: tool calls, routine reasoning | `claude-haiku-5-5` |
| Delegated subagents: heavy reasoning, writing | `claude-sonnet-5-5` |
| Cross-provider failover | `fallback_providers` (commented out until a second provider key exists) |

On every boot `merge-config.py` merges the overlay into `/data/.hermes/config.yaml`. Git wins for the keys in the overlay. It never blocks startup, and writes `config.yaml.bak` before changing anything.

## Secrets

Never commit keys. Set `ANTHROPIC_API_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` and channel tokens in Railway variables or the Hermes dashboard.
