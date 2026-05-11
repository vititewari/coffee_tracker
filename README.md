# Coffee Tracker

  A terminal-based AI assistant for managing and improving your coffee recipes. Talk to it naturally — it decides when
  to save, retrieve, or analyse a recipe on your behalf.

  Powered by the Anthropic Claude API. Recipes are stored locally in a plain text file.

  ---

  ## Installation

  **1. Clone the repo and create a virtual environment**

  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1

  2. Install dependencies

  pip install anthropic

  3. Set your Anthropic API key

  $env:ANTHROPIC_API_KEY = "your-api-key-here"

  ---
  Running

  python main.py

  Type quit or press Ctrl+C to exit.

  ---
  What you can do

  All interaction is in plain English. The assistant understands three underlying actions:

  ┌──────────────────┬───────────────────────────────────────────────┐
  │      Action      │                  What to say                  │
  ├──────────────────┼───────────────────────────────────────────────┤
  │ Save a recipe    │ Describe a brew and ask it to save it         │
  ├──────────────────┼───────────────────────────────────────────────┤
  │ Read a recipe    │ Ask for a recipe by name (partial names work) │
  ├──────────────────┼───────────────────────────────────────────────┤
  │ Analyse a recipe │ Ask it to review or improve a recipe          │
  └──────────────────┴───────────────────────────────────────────────┘

  Recipes are saved to data/recipes.txt and persist between sessions.

  ---
  Example conversation

  Saving a recipe

  You: Save my morning V60 — 20g medium-fine ground, 300g water at 95C,
       bloom 45s with 60g then pour in stages over 3.5 minutes.
       Rating 4/5. Notes: slightly acidic, might try coarser next time.

  Assistant: Done! I've saved your Morning V60 Pour Over recipe. The bloom
  ratio looks solid at 1:3. Good call on noting the acidity — a coarser
  grind should bring that into balance.
  Reading a recipe

  You: Show me my V60 recipe.

  Assistant: Here it is:

  [NAME]: Morning V60 Pour Over
  [INGREDIENTS]: 20g medium-fine ground coffee, 300g water
  [METHOD]: 95C water, bloom for 45s with 60g, then pour in stages
  [BREW_TIME]: 3 minutes 30 seconds
  [RATING]: 4/5
  [NOTES]: Slightly acidic, try coarser grind next time
  Analysing a recipe

  You: Can you analyse my V60 and suggest improvements?

  Assistant: Looking at your Morning V60 Pour Over:

  Weaknesses:
  - Your 1:15 ratio (20g:300g) is on the stronger side — if acidity
    is a problem, try dropping to 18g for the same water weight.
  - "Pour in stages" is vague. Try a structured pour: 60g bloom,
    then three 80g pours every 45 seconds.
  - No grind size recorded — hard to reproduce or iterate without it.

  Suggested next brew:
  - Grind: one step coarser than your current setting
  - Dose: 18g in, 300g out
  - Pour: 60g bloom (45s), then 80g at 1:15, 1:45, and 2:15
  - Target finish: under 3:30