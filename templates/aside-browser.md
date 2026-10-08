## Browser work in Aside

Open and operate every browser page in Aside, including navigation, clicking, input, and result verification. The Hermes model plans the actions and directly controls Aside through the configured MCP `repl` tool or `aside repl` JavaScript. Do not use Aside's own AI agent: `aside exec`, bare `aside` with natural-language prompts, or an agent-delegating MCP tool. Do not switch to `exec` when `repl` fails; diagnose and restore the direct-control connection instead. An `exec` model/provider quota error is not evidence that `repl` browser control has exhausted an LLM quota.

For each project, use the Aside profile specified by that project's rules and keep its account and data boundaries. If the project does not identify a profile, establish the correct profile before account-bound work. When direct control is unavailable, report the blocker and resume through `repl` after it is resolved; do not silently switch browsers or invoke Aside's AI agent.
