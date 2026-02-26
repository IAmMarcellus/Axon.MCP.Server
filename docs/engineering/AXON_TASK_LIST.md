# Axon Task List (Running Board)

**Path:** `/home/marcellus/.openclaw/workspace/repos/Axon.MCP.Server/docs/engineering/AXON_TASK_LIST.md`  
**Scope:** Ongoing implementation, hardening, and validation tasks for Axon.MCP.Server.  
**Last Updated (UTC):** 2026-02-26T23:12:00Z

## How to Use (for humans + coding agents)

1. **Single source of truth:** Use this file for active/planned/blocked Axon tasks.
2. **State transitions:** Move tasks between state sections only (don’t duplicate).
3. **Ordering rules:**
   - `INCOMPLETE`, `IN_PROGRESS`, and `BLOCKED` must stay sorted by **priority** (`P0` highest → `P3` lowest).
   - If same priority, sort by task ID.
4. **Done timestamps:** When moving a task to `DONE`, add `completed_at=<ISO-8601 UTC>`.
5. **Priority discipline:**
   - `P0` = urgent/release or correctness risk
   - `P1` = important near-term hardening
   - `P2` = medium-value improvements
   - `P3` = low urgency / cleanup
6. **Task format (required fields):**
   - `id`, `priority`, `owner`, `summary`, `next_step`
   - Optional: `blocked_reason`, `depends_on`, `links`

## Task Entry Template

- [ ] `AX-XXX` | `P#` | owner=`<agent-or-human>` | summary=`<what>` | next_step=`<immediate next action>`
  - depends_on=`<optional>`
  - links=`<optional>`

---

## IN_PROGRESS (sorted by priority)

- [ ] `AX-023` | `P0` | owner=`main+cron` | summary=`Verify Python symbol support works end-to-end (parser -> extraction -> query/tool flows)` | next_step=`Run focused MCP/sync symbol-flow checks and patch any remaining Python symbol gaps.`
  - links=`src/parsers/python_parser.py, tests/unit/test_python_parser.py`

- [ ] `AX-024` | `P1` | owner=`cron` | summary=`Continue rolling stabilization/hardening across backend + React with regression coverage expansion.` | next_step=`Take next high-impact issue from audit/coverage output, fix it, and add regression tests.`

## INCOMPLETE (sorted by priority)

- [ ] `AX-025` | `P0` | owner=`main` | summary=`Curate, commit, and push the current stabilization working tree safely in logical commits.` | next_step=`Split changes by concern (parser/security/ui/tests), commit, push, and update PR/summary.`

- [ ] `AX-026` | `P1` | owner=`main+cron` | summary=`Increase coverage for low-coverage API routes and worker pipeline steps touched by stabilization.` | next_step=`Add targeted route + worker tests for highest-risk paths and re-run full pytest.`

- [ ] `AX-027` | `P1` | owner=`main+cron` | summary=`Add integration-level regression coverage specifically for Python symbol workflows (search/navigation/use-cases).` | next_step=`Add tests that assert Python symbols are discoverable and queryable after ingestion.`

- [ ] `AX-028` | `P2` | owner=`cron` | summary=`Reduce remaining project-controlled UTC/deprecation warning sources.` | next_step=`Sweep project modules for residual datetime.utcnow() usage and migrate safely.`

- [ ] `AX-029` | `P3` | owner=`main+cron` | summary=`Run dedicated React lint-hardening sweep across pre-existing UI lint debt.` | next_step=`Fix high-signal lint issues first (hooks deps, a11y, explicit-any, unused vars) and keep build/tests green.`

## BLOCKED (sorted by priority)

- [ ] `AX-030` | `P1` | owner=`main+cron` | summary=`Eliminate Celery internal datetime.utcnow() deprecation warnings in runtime output.` | next_step=`Track pinned Celery version and upgrade path.`
  - blocked_reason=`Warnings originate from dependency internals, not only project-owned code; full removal requires upstream/library upgrade.`

- [ ] `AX-031` | `P2` | owner=`main+cron` | summary=`Remove Starlette/python_multipart deprecation warning path fully.` | next_step=`Upgrade dependency chain and validate import path changes end-to-end.`
  - blocked_reason=`Warning originates from external dependency import path behavior.`

- [ ] `AX-032` | `P2` | owner=`main` | summary=`Automate 1Password `.env` sync for unattended agent sessions.` | next_step=`Adopt service-account/token-based auth path for non-interactive gateway execution.`
  - blocked_reason=`Current OP session auth is shell-scoped and not reliably available to service/cron process context.`

## DONE (sorted by completion date, newest first)

- [x] `AX-022` | `P0` | owner=`main` | summary=`Implement Python symbol parser + factory routing for `.py` files.` | completed_at=`2026-02-26T23:04:18Z`
  - links=`commit b6af290, src/parsers/python_parser.py, tests/unit/test_python_parser.py`

- [x] `AX-021` | `P1` | owner=`cron` | summary=`Harden Python dependency parsing and React metrics handling (+Inf/-Inf/NaN) with regression tests.` | completed_at=`2026-02-26T22:23:00Z`
  - links=`src/parsers/python_dependency_parser.py, ui/src/components/metrics_panel/MetricsPanel.tsx`

- [x] `AX-020` | `P1` | owner=`cron` | summary=`Complete baseline stabilization/hardening sweep (security defaults, async/process robustness, lifecycle migration) and verify backend/frontend test/build health.` | completed_at=`2026-02-26T22:07:00Z`
  - links=`docs/engineering/BUG_AUDIT_2026-02-26.md`
