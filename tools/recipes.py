from pathlib import Path

RECIPES_PATH = Path(__file__).parent.parent / "data" / "recipes.txt"


def save_recipe(name, ingredients, method, time, rating, notes):
    """Save a coffee recipe to the recipes.txt file.

    Args:
        name: Name of the recipe.
        ingredients: Ingredients used.
        method: Brew method and temperature.
        time: Brew time.
        rating: Rating out of 5.
        notes: Additional notes.

    Returns:
        A string indicating success or describing the error.
    """
    try:
        RECIPES_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry = (
            f"[NAME]: {name} \n"
            f"[INGREDIENTS]: {ingredients} \n"
            f"[METHOD]: {method} \n"
            f"[BREW_TIME]: {time} \n"
            f"[RATING]: {rating} \n"
            f"[NOTES]: {notes}\n"
            f"---\n"
        )
        with open(RECIPES_PATH, "a") as f:
            f.write(entry)
        return "Recipe saved successfully."
    except Exception as e:
        return f"Failed to save recipe: {e}"


def read_recipes(name=None):
    """Read a recipe from the recipes.txt file by name.

    Args:
        name: Name of the recipe to retrieve. If empty or None, all recipes are returned.

    Returns:
        The matching recipe block, all recipes if name is empty/None,
        or a string describing the error.
    """
    try:
        with open(RECIPES_PATH, "r") as f:
            content = f.read()
    except FileNotFoundError:
        return "Error: recipes.txt file not found."
    except Exception as e:
        return f"Error reading file: {e}"

    blocks = [block.strip() for block in content.split("---") if block.strip()]

    if not name:
        if not blocks:
            return "No recipes found."
        return "\n---\n".join(blocks)

    for block in blocks:
        for line in block.splitlines():
            if line.startswith("[NAME]:") and name.strip().lower() in line[len("[NAME]:"):].strip().lower():
                return block

    return f"Error: No recipe found with the name '{name}'."


def delete_recipe(name):
    """Delete a recipe from recipes.txt by name.

    Args:
        name: Name (or substring) of the recipe to delete. Matched case-insensitively
              against the [NAME] line of each block.

    Returns:
        A string confirming deletion, or describing the error if not found or on failure.
    """
    try:
        with open(RECIPES_PATH, "r") as f:
            content = f.read()
    except FileNotFoundError:
        return "Error: recipes.txt file not found."
    except Exception as e:
        return f"Error reading file: {e}"

    blocks = [block.strip() for block in content.split("---") if block.strip()]

    kept = []
    deleted = False
    for block in blocks:
        matched = False
        for line in block.splitlines():
            if line.startswith("[NAME]:") and name.strip().lower() in line[len("[NAME]:"):].strip().lower():
                matched = True
                break
        if matched:
            deleted = True
        else:
            kept.append(block)

    if not deleted:
        return f"Error: No recipe found with the name '{name}'."

    try:
        RECIPES_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RECIPES_PATH, "w") as f:
            for block in kept:
                f.write(block + "\n---\n")
    except Exception as e:
        return f"Error writing file: {e}"

    return f"Recipe '{name}' deleted successfully."


def analyse_recipes(name):
    """Read a recipe and return it formatted for analysis."""
    recipe = read_recipes(name)
    if recipe.startswith("Error"):
        return recipe
    return f"Here is the recipe to analyse:\n{recipe}\nPlease identify weaknesses and suggest specific improvements."
