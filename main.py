from kivy.app import App
from data_handler import load_family_data
from data_handler import save_family_data
from tree_visualization import visualize_tree
from ui import FamilyTreeUI
import os

class FamilyTreeApp(App):
    def build(self):
        self.title = "Семейное древо"

        # Загружаем данные
        self.data = load_family_data()

        # Создаем UI
        return FamilyTreeUI(
            add_member_callback=self.add_member,
            update_tree_callback=self.update_tree_visualization
        )

    def add_member(self, fio, birthdate, parent_fio):
        """Добавляет нового члена семьи."""
        self.data.append({
            "fio": fio,
            "birthdate": birthdate,
            "parent": parent_fio
        })
        save_family_data(self.data)

    def update_tree_visualization(self):
        """Обновляет визуализацию дерева."""
        visualize_tree(self.data, self.root.tree_label)

def get_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")  # Папка для данных
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)  # Создаем папку, если её нет
    return os.path.join(data_dir, filename)

if __name__ == "__main__":
    FamilyTreeApp().run()