from kivy.app import App
from kivy.config import Config
from data_handler import load_family_data
from data_handler import save_family_data
from tree_visualization import visualize_tree
from ui import FamilyTreeUI

# Увеличиваем размер окна в 2 раза (например, до 800x600)
Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 600)

class FamilyTreeApp(App):
    def build(self):
        self.title = "Семейное древо"

        # Загружаем данные
        self.data = load_family_data()

        # Создаем UI
        self.ui = FamilyTreeUI(
            add_member_callback=self.add_member,
            update_tree_callback=self.update_tree_visualization
        )

        # Сохраняем ссылку на tree_image из UI
        self.tree_image = self.ui.tree_image

        # Обновляем визуализацию дерева сразу после запуска
        self.update_tree_visualization()

        return self.ui

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
        print(f"Updating tree visualization with data: {self.data}")  # Отладочное сообщение
        visualize_tree(self.data, self.tree_image)

if __name__ == "__main__":
    FamilyTreeApp().run()