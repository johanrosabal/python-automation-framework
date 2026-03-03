# mock/db/product_db.py
import json
from pathlib import Path
from typing import Dict, List
from models.product import Product

# Ruta al archivo JSON
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "products.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_products() -> List[Dict]:
    """Carga productos. Devuelve lista vacía si el archivo está vacío/inválido."""
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


def _save_products(products: List[Dict]):
    """Guarda la lista de productos."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)


# Funciones CRUD

def get_all_products() -> List[Product]:
    products_data = _load_products()
    return [Product(**prod) for prod in products_data]


def get_product_by_id(product_id: int) -> Product | None:
    products = _load_products()
    for prod in products:
        if prod["id"] == product_id:
            return Product(**prod)
    return None


def create_product(product_data: dict) -> Product:  # ✅ Corregido: product_data: dict
    products = _load_products()
    new_id = max([p["id"] for p in products], default=0) + 1
    new_product = {"id": new_id, **product_data}
    products.append(new_product)
    _save_products(products)
    return Product(**new_product)


def update_product(product_id: int, product_data: dict) -> Product | None:  # ✅ Corregido: product_data: dict
    products = _load_products()
    for i, prod in enumerate(products):
        if prod["id"] == product_id:
            products[i] = {"id": product_id, **product_data}
            _save_products(products)
            return Product(**products[i])
    return None


def delete_product(product_id: int) -> bool:
    products = _load_products()
    initial_count = len(products)
    products = [p for p in products if p["id"] != product_id]
    if len(products) < initial_count:
        _save_products(products)
        return True
    return False
