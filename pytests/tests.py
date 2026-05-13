import pytest
import tools.recipes as recipes_module
from tools.recipes import save_recipe, read_recipes, analyse_recipes, delete_recipe


@pytest.fixture(autouse=True)
def tmp_recipes(tmp_path, monkeypatch):
    """Redirect RECIPES_PATH to a temp file for every test so nothing touches the real data."""
    temp_file = tmp_path / "recipes.txt"
    monkeypatch.setattr(recipes_module, "RECIPES_PATH", temp_file)
    return temp_file


# ---------------------------------------------------------------------------
# save_recipe
# ---------------------------------------------------------------------------

def test_save_recipe_returns_success(tmp_recipes):
    result = save_recipe("V60", "20g coffee", "Pour over", "3 min", "4", "Nice")
    assert result == "Recipe saved successfully."


def test_save_recipe_creates_file(tmp_recipes):
    save_recipe("V60", "20g coffee", "Pour over", "3 min", "4", "Nice")
    assert tmp_recipes.exists()


def test_save_recipe_writes_all_fields(tmp_recipes):
    save_recipe("V60", "20g coffee", "Pour over", "3 min", "4", "Nice")
    content = tmp_recipes.read_text()
    assert "[NAME]: V60" in content
    assert "[INGREDIENTS]: 20g coffee" in content
    assert "[METHOD]: Pour over" in content
    assert "[BREW_TIME]: 3 min" in content
    assert "[RATING]: 4" in content
    assert "[NOTES]: Nice" in content
    assert "---" in content


def test_save_recipe_appends_multiple(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    save_recipe("Espresso", "18g", "Espresso", "30s", "5", "")
    content = tmp_recipes.read_text()
    assert "V60" in content
    assert "Espresso" in content


# ---------------------------------------------------------------------------
# read_recipes
# ---------------------------------------------------------------------------

def test_read_recipes_returns_all_when_no_name(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    save_recipe("Espresso", "18g", "Espresso", "30s", "5", "")
    result = read_recipes()
    assert "V60" in result
    assert "Espresso" in result


def test_read_recipes_returns_all_when_none(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    result = read_recipes(None)
    assert "V60" in result


def test_read_recipes_by_exact_name(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    save_recipe("Espresso", "18g", "Espresso", "30s", "5", "")
    result = read_recipes("V60")
    assert "V60" in result
    assert "Espresso" not in result


def test_read_recipes_case_insensitive(tmp_recipes):
    save_recipe("Morning V60", "20g", "Pour", "3 min", "4", "")
    result = read_recipes("morning v60")
    assert "Morning V60" in result


def test_read_recipes_substring_match(tmp_recipes):
    save_recipe("Morning V60 Pour Over", "20g", "Pour", "3 min", "4", "")
    result = read_recipes("pour")
    assert "Morning V60 Pour Over" in result


def test_read_recipes_not_found_returns_error(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    result = read_recipes("Chemex")
    assert "Error" in result
    assert "Chemex" in result


def test_read_recipes_empty_file_returns_no_recipes(tmp_recipes):
    tmp_recipes.write_text("")
    result = read_recipes()
    assert "No recipes found." in result


def test_read_recipes_file_not_found_returns_error(tmp_recipes):
    result = read_recipes()
    assert "Error" in result
    assert "not found" in result.lower()


# ---------------------------------------------------------------------------
# analyse_recipes
# ---------------------------------------------------------------------------

def test_analyse_recipes_returns_recipe_content(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    result = analyse_recipes("V60")
    assert "V60" in result


def test_analyse_recipes_includes_analysis_prompt(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    result = analyse_recipes("V60")
    assert "improve" in result.lower() or "weakness" in result.lower()


def test_analyse_recipes_not_found_returns_error(tmp_recipes):
    result = analyse_recipes("Nonexistent")
    assert "Error" in result


def test_analyse_recipes_case_insensitive(tmp_recipes):
    save_recipe("Morning V60", "20g", "Pour", "3 min", "4", "")
    result = analyse_recipes("v60")
    assert "Morning V60" in result


# ---------------------------------------------------------------------------
# delete_recipe
# ---------------------------------------------------------------------------

def test_delete_recipe_returns_success(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    result = delete_recipe("V60")
    assert "deleted successfully" in result


def test_delete_recipe_removes_from_file(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    save_recipe("Espresso", "18g", "Espresso", "30s", "5", "")
    delete_recipe("V60")
    content = tmp_recipes.read_text()
    assert "V60" not in content
    assert "Espresso" in content


def test_delete_recipe_preserves_other_recipes(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    save_recipe("Espresso", "18g", "Espresso", "30s", "5", "")
    save_recipe("Chemex", "30g", "Chemex", "4 min", "3", "")
    delete_recipe("Espresso")
    result = read_recipes()
    assert "V60" in result
    assert "Chemex" in result
    assert "Espresso" not in result


def test_delete_recipe_case_insensitive(tmp_recipes):
    save_recipe("Morning V60", "20g", "Pour", "3 min", "4", "")
    result = delete_recipe("morning v60")
    assert "deleted successfully" in result


def test_delete_recipe_substring_match(tmp_recipes):
    save_recipe("Morning V60 Pour Over", "20g", "Pour", "3 min", "4", "")
    result = delete_recipe("v60")
    assert "deleted successfully" in result
    assert "V60" not in tmp_recipes.read_text()


def test_delete_recipe_not_found_returns_error(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    result = delete_recipe("Chemex")
    assert "Error" in result
    assert "Chemex" in result


def test_delete_recipe_file_not_found_returns_error(tmp_recipes):
    result = delete_recipe("V60")
    assert "Error" in result
    assert "not found" in result.lower()


def test_delete_only_recipe_leaves_empty_file(tmp_recipes):
    save_recipe("V60", "20g", "Pour", "3 min", "4", "")
    delete_recipe("V60")
    result = read_recipes()
    assert "No recipes found." in result
