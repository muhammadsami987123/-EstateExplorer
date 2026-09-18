import json
import uuid
from pathlib import Path
from typing import Any, Optional
import threading

DATA_DIR = Path(__file__).parent / "data"

class JsonDB:
    _locks = {}
    _locks_lock = threading.Lock()

    @classmethod
    def _get_lock(cls, collection: str):
        with cls._locks_lock:
            if collection not in cls._locks:
                cls._locks[collection] = threading.Lock()
            return cls._locks[collection]

    @classmethod
    def _path(cls, collection: str) -> Path:
        return DATA_DIR / f"{collection}.json"

    @classmethod
    def load(cls, collection: str) -> list:
        path = cls._path(collection)
        if not path.exists():
            return []
        with cls._get_lock(collection):
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except Exception:
                    return []

    @classmethod
    def save(cls, collection: str, data: list) -> None:
        path = cls._path(collection)
        path.parent.mkdir(parents=True, exist_ok=True)
        with cls._get_lock(collection):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def find(cls, collection: str, **filters) -> list:
        items = cls.load(collection)
        for key, value in filters.items():
            if value is not None:
                items = [i for i in items if i.get(key) == value]
        return items

    @classmethod
    def find_one(cls, collection: str, id: str) -> Optional[dict]:
        items = cls.load(collection)
        return next((i for i in items if i.get('id') == id), None)

    @classmethod
    def insert(cls, collection: str, item: dict) -> dict:
        items = cls.load(collection)
        if 'id' not in item or not item['id']:
            item['id'] = str(uuid.uuid4())
        items.append(item)
        cls.save(collection, items)
        return item

    @classmethod
    def update(cls, collection: str, id: str, data: dict) -> Optional[dict]:
        items = cls.load(collection)
        for i, item in enumerate(items):
            if item.get('id') == id:
                items[i] = {**item, **data}
                cls.save(collection, items)
                return items[i]
        return None

    @classmethod
    def delete(cls, collection: str, id: str) -> bool:
        items = cls.load(collection)
        new_items = [i for i in items if i.get('id') != id]
        if len(new_items) < len(items):
            cls.save(collection, new_items)
            return True
        return False
