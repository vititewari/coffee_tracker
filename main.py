from tools.recipes import save_recipe, read_recipes, analyse_recipes, delete_recipe
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "save_recipe",
        "description": "Save a new coffee recipe to the recipes file.",
        "input_schema": {
            "type": "object",
            "required": ["name", "ingredients", "method", "time", "rating", "notes"],
            "properties": {
                "name": {"type": "string", "description": "Name of the recipe."},
                "ingredients": {"type": "string", "description": "Ingredients used in the recipe."},
                "method": {"type": "string", "description": "Brew method and temperature."},
                "time": {"type": "string", "description": "Brew time."},
                "rating": {"type": "string", "description": "Rating out of 5."},
                "notes": {"type": "string", "description": "Additional notes about the recipe."},
            },
        },
    },
    {
        "name": "read_recipes",
        "description": "Read a recipe by name from the recipes file. If name is empty or omitted, returns all recipes.",
        "input_schema": {
            "type": "object",
            "required": [],
            "properties": {
                "name": {"type": "string", "description": "Name of the recipe to retrieve. Leave empty to get all recipes."},
            },
        },
    },
    {
        "name": "analyse_recipes",
        "description": "Read a recipe by name and return it formatted with a prompt to identify weaknesses and suggest improvements.",
        "input_schema": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "description": "Name of the recipe to analyse."},
            },
        },
    },
    {
        "name": "delete_recipe",
        "description": "Delete a recipe by name from the recipes file.",
        "input_schema": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "description": "Name of the recipe to delete."},
            },
        },
    },
]

tool_router = {
    "save_recipe": save_recipe,
    "read_recipes": read_recipes,
    "analyse_recipes": analyse_recipes,
    "delete_recipe": delete_recipe,
}


def run_agent(user_message):
    """Run the coffee recipe agent with the given user message."""
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            system=(
                "You are a helpful barista assistant helping an intermediate coffee brewer "
                "manage and improve their coffee recipes. The user hand grinds their beans, "
                "owns a semi-professional coffee machine, and is a hardcore coffee lover who "
                "prefers coffee that is not too bitter."
            ),
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text
        elif response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    if tool_name in tool_router:
                        tool_result = tool_router[tool_name](**tool_input)
                    else:
                        tool_result = f"Error: Unknown tool '{tool_name}'."
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(tool_result),
                    })
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            return f"Unexpected stop reason: {response.stop_reason}"


if __name__ == "__main__":
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() == "quit":
            break
        print(f"Assistant: {run_agent(user_input)}")
