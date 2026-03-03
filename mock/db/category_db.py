# mock/db/category_db.py
import json
from pathlib import Path
from typing import Dict, List
from models.category import Category

# Ruta al archivo JSON
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "categories.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_categories() -> List[Dict]:
    """Carga categorías. Devuelve lista vacía si el archivo está vacío/inválido."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                return list(data.values())
            elif isinstance(data, list):
                return data
            else:
                return []
        except json.JSONDecodeError:
            return []


def _save_categories(categories: List[Dict]):
    """Guarda la lista de categorías."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2)


# Funciones CRUD

def get_all_categories() -> List[Category]:
    categories_data = _load_categories()
    return [Category(**cat) for cat in categories_data]


def get_category_by_id(category_id: int) -> Category | None:
    categories = _load_categories()
    for cat in categories:
        if cat["id"] == category_id:
            return Category(**cat)
    return None


def create_category(category_data: dict) -> Category:
    categories = _load_categories()
    new_id = max([c["id"] for c in categories], default=0) + 1
    new_category = {"id": new_id, **category_data}
    categories.append(new_category)
    _save_categories(categories)
    return Category(**new_category)


def update_category(category_id: int, category_data: dict) -> Category | None:
    categories = _load_categories()
    for i, cat in enumerate(categories):
        if cat["id"] == category_id:
            categories[i] = {"id": category_id, **category_data}
            _save_categories(categories)
            return Category(**categories[i])
    return None


def delete_category(category_id: int) -> bool:
    categories = _load_categories()
    initial_count = len(categories)
    categories = [c for c in categories if c["id"] != category_id]
    if len(categories) < initial_count:
        _save_categories(categories)
        return True
    return False
