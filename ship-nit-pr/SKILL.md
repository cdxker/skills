---
name: ship-nit-pr
description: Implement, publish, and merge every small code nit, tweak, tiny fix, minor change, cleanup, or “just change this” request as its own isolated GitHub pull request; trigger whenever Denzell asks for a small repository change or calls something a nit.
---

# Ship each nit as its own PR

Treat Denzell's request for a small repository change as explicit authorization to implement it, verify it locally, create an isolated branch and commit, push that branch, open a pull request, and merge it immediately. Do not wait for a separate “commit,” “push,” “make a PR,” or “merge” instruction. Never wait for, watch, or poll CI before merging.

## Keep the scope atomic

- Put exactly one user-requested nit or tightly coupled tiny fix in each PR.
- Never include unrelated worktree changes, generated files, formatting churn, or opportunistic cleanup.
- Inspect `git status -sb` and the complete intended diff before staging.
- Stage explicit paths. Never use `git add -A` in a mixed worktree.
- If unrelated changes overlap the same lines and cannot be separated safely, stop and ask Denzell before publishing.
- If several distinct nits arrive together, use separate branches and PRs unless they only make sense as one change.

## Implement and verify

- Follow the repository's `AGENTS.md` files and applicable skills.
- Make the smallest complete change that fixes the requested behavior.
- Run the narrowest meaningful type, lint, formatting, and test checks.
- Do not install dependencies or start a server outside Herdr.
- If a check cannot run, state that clearly in the PR and final handoff.

## Publish automatically

Use the `github:yeet` skill when available, but still require squash-and-merge. Otherwise follow this workflow:

1. Confirm `gh` is installed and authenticated.
2. Determine the remote default branch and repository.
3. Start from the appropriate clean base. Name a new branch `agent/<concise-description>`.
4. Stage only the intended paths and review the staged diff.
5. Commit with a terse imperative message.
6. Push with upstream tracking.
7. Open a PR with a concise title and a body covering:
   - what changed;
   - why and root cause;
   - user impact;
   - validation performed.
8. As soon as the PR is open and GitHub reports it mergeable, squash-and-merge it with `gh pr merge --squash`. Always use squash-and-merge, regardless of the repository's established or default merge strategy. Never use a merge commit or rebase merge. Do not run `gh pr checks --watch`, wait for checks, or delay the merge for CI. If branch protection requires checks, enable squash auto-merge and continue only when GitHub reports the PR merged; do not stay in a CI polling loop.
9. If GitHub synchronously rejects the merge for a reason unrelated to pending CI, investigate within the nit's scope and report the blocker.
10. Refresh and verify the local application as described below.
11. Return the PR link, branch, commit, local validation, resulting squash commit, and local application status.

## Refresh the local application after merge

Do not call a nit complete while an existing local application is still serving the pre-merge code.

1. Determine whether the repository has a dedicated live worktree and `*.localhost` site. Inspect repository instructions, active dev-server process working directories, and the local proxy configuration instead of guessing from worktree names.
2. Inspect the live worktree's status and commit before changing it. Preserve dependency directories and unrelated user files. If source changes or local commits would be overwritten or require a history rewrite, stop and report the conflict instead of discarding them.
3. Fetch the remote default branch, then rebase or fast-forward the live worktree onto the exact merged default-branch commit. A detached live worktree may be rebased directly onto `origin/<default-branch>` when its current commit is an ancestor and its source tree is otherwise clean.
4. Reuse the application's established process supervisor and never create a duplicate server. Poetry Studio is served by the enabled systemd user unit `poetry-dev.service`: restart and inspect that unit with `systemctl --user` and `journalctl --user`, never Herdr. For applications without an established supervisor, follow the active `AGENTS.md` server instructions.
5. Open the real `http://<app>.localhost` URL and verify the requested behavior there, including browser errors and responsive behavior when relevant. Do not substitute a temporary port URL for this final verification.
6. If no local site or live worktree exists, say so explicitly in the handoff. If one exists but cannot be synchronized safely, treat that as an incomplete local rollout and report the blocker.

One nit gets one branch, one commit when practical, one PR, and one squash merge when green. Never silently append a new nit to an existing PR.
