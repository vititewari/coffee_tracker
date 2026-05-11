# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

An AI-powered coffee recipe manager. The user interacts via a terminal chat loop; the Claude agent decides when to call tools to save, read, or analyse recipes stored in a flat text file.

## How to run

```powershell
python main.py        # start the interactive chat loop
```

Type `quit` or press `Ctrl+C` to exit.

## Architecture

```
main.py              # entry point — Claude agent loop + tool definitions
tools/
  recipes.py         # three tool functions: save_recipe, read_recipes, analyse_recipes
data/
  recipes.txt        # flat-file recipe store, entries separated by ---
```

### Agent loop (`main.py`)

`run_agent(user_message)` drives a `while True` loop calling `client.messages.create()` with the Anthropic SDK. On `tool_use` stop, it dispatches via `tool_router` (a plain dict mapping tool name → function), appends the assistant turn and tool results to `messages`, then loops again. On `end_turn` it returns the text reply.

### Recipe storage (`tools/recipes.py`)

`RECIPES_PATH` is always resolved as an absolute path relative to the module file (`Path(__file__).parent.parent / "data" / "recipes.txt"`), so the functions work regardless of the working directory.

Each recipe is a block of tagged lines followed by `---`:

```
[NAME]: Morning V60 Pour Over
[INGREDIENTS]: ...
[METHOD]: ...
[BREW_TIME]: ...
[RATING]: ...
[NOTES]: ...
---
```

`read_recipes` splits on `---` and does a **case-insensitive substring** match on the `[NAME]` line, so partial queries like `"v60"` match `"Morning V60 Pour Over"`. Passing `None` or an empty string returns all recipes.

## Dependencies

- `anthropic` Python SDK (install with `pip install anthropic`)
- `ANTHROPIC_API_KEY` environment variable must be set
- Model used: `claude-haiku-4-5-20251001`

## Code rules

- All functions must have docstrings
- Always return error strings — never raise exceptions
- Tool schemas are defined manually as Python dicts (name, description, input_schema) in `main.py`; do not use decorators or auto-generation
- File path must always be `Path(__file__).parent.parent / "data" / "recipes.txt"` — never hardcode or use relative paths
- `data/` must be created automatically with `RECIPES_PATH.parent.mkdir(parents=True, exist_ok=True)` before any write
- After every new feature, run `pytest` and verify all tests pass before reporting done
- Windows PowerShell — do not use `<`/`>` for input redirection
