import json
import os

def get_path(filename):
    """Возвращает путь к файлу в папке data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return os.path.join(data_dir, filename)

def load_family_data():
    """Загружает данные из файла family_data.json."""
    path = get_path("family_data.json")
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content.strip():  # Если файл пустой
                return []
            return json.loads(content)
    except FileNotFoundError:
        # Если файл не найден, создаем его с пустым списком
        default_data = []
        save_family_data(default_data)
        return default_data

def save_family_data(data):
    """Сохраняет данные в файл family_data.json."""
    path = get_path("family_data.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)