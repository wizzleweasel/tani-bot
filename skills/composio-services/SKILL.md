---
name: composio-services
description: "External service operations via composio_helper.py. Use when: (1) user asks about GitHub, (2) user asks about Supabase, (3) user asks about Hacker News. Always run bash commands — never call tools directly."
---

# Connected Services (via Composio)

**CRITICAL: Always execute these as bash commands using the python3 command shown. NEVER attempt to call a tool named composio or any service name directly. NEVER invent action names — only use the exact action names listed below.**

Connected services: GitHub, Supabase, Hacker News

# GitHub via the composio-run command

**Always execute these as bash commands. Never invent action names.**

## List my repos

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER '{}'
```

## Search repos

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_FIND_REPOSITORIES '{"query": "language:python stars:>100"}'
```

## Create an issue

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_CREATE_AN_ISSUE '{"owner": "org", "repo": "repo-name", "title": "Bug report", "body": "Description"}'
```

## List issues

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_LIST_REPOSITORY_ISSUES '{"owner": "org", "repo": "repo-name"}'
```

## Create a pull request

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_CREATE_A_PULL_REQUEST '{"owner": "org", "repo": "repo-name", "title": "Fix bug", "head": "fix-branch", "base": "main", "body": "Description"}'
```

## List pull requests

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_LIST_PULL_REQUESTS '{"owner": "org", "repo": "repo-name"}'
```

## Get file content

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_GET_REPOSITORY_CONTENT '{"owner": "org", "repo": "repo-name", "path": "README.md"}'
```

## Create or update a file

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS '{"owner": "org", "repo": "repo-name", "path": "file.txt", "message": "Add file", "content": "base64content"}'
```

## List branches

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_LIST_BRANCHES '{"owner": "org", "repo": "repo-name"}'
```

## Search issues and PRs

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS '{"query": "is:open label:bug repo:org/repo"}'
```

## Create a release

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec GITHUB_CREATE_A_RELEASE '{"owner": "org", "repo": "repo-name", "tag_name": "v1.0.0", "name": "Release 1.0", "body": "Release notes"}'
```

## Rules

1. Always use bash. Never call a tool directly. Never invent action names.
2. Prefer built-in gh CLI skill for most GitHub tasks if available.

---

# Supabase via the composio-run command

**Always execute these as bash commands. Never invent action names.**

## Run a SQL query

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec SUPABASE_BETA_RUN_SQL_QUERY '{"project_ref": "PROJECT_REF", "query": "SELECT * FROM users LIMIT 10"}'
```

## List all projects

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec SUPABASE_LIST_ALL_PROJECTS '{}'
```

## Create a project

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec SUPABASE_CREATE_A_PROJECT '{"name": "my-project", "organization_id": "ORG_ID", "region": "us-east-1", "db_pass": "securepassword"}'
```

## Get table schemas

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec SUPABASE_GET_TABLE_SCHEMAS '{"project_ref": "PROJECT_REF"}'
```

## List organizations

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec SUPABASE_LIST_ALL_ORGANIZATIONS '{}'
```

## Generate TypeScript types

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec SUPABASE_GENERATE_TYPE_SCRIPT_TYPES '{"project_ref": "PROJECT_REF"}'
```

## Rules

1. Always use bash. Never call a tool directly. Never invent action names.

---

# Hacker News via the composio-run command

**Always execute these as bash commands. Never invent action names. No authentication needed — HN is a public API.**

## Get front page posts

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec HACKERNEWS_GET_FRONTPAGE '{}'
```

## Get today's posts

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec HACKERNEWS_GET_TODAYS_POSTS '{}'
```

## Get latest posts

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec HACKERNEWS_GET_LATEST_POSTS '{}'
```

## Search posts

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec HACKERNEWS_SEARCH_POSTS '{"query": "AI agents"}'
```

## Get a specific post/item by ID

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec HACKERNEWS_GET_ITEM_WITH_ID '{"item_id": "12345"}'
```

## Get a user profile

```bash
/mnt/data/openclaw/workspace/bin/composio-run exec HACKERNEWS_GET_USER '{"username": "pg"}'
```

## Rules

1. Always use bash. Never call a tool directly. Never invent action names.
2. No authentication is needed for Hacker News — it's a public API.