from kivy.app import App
from kivy.config import Config
from data_handler import load_family_data, save_family_data
from tree_visualization import (
    visualize_tree,
    validate_family_data,
    get_generations,
    separate_by_gender,
    find_common_ancestor
)
from ui import FamilyTreeUI

# Увеличиваем размер окна
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
            update_tree_callback=self.update_tree_visualization,
            find_ancestor_callback=self.find_common_ancestor_ui
        )

        # Сохраняем ссылку на изображение дерева из UI
        self.tree_image = self.ui.tree_image

        # Проверяем корректность данных
        if not validate_family_data(self.data):
            print("Данные содержат ошибки. Пожалуйста, исправьте их.")

        # Определяем поколения
        generations = get_generations(self.data)
        print("Поколения:")
        for gen, members in generations.items():
            print(f"{gen}: {members}")

        # Разделяем по полу
        gender_split = separate_by_gender(self.data)
        print("Мужская линия:", gender_split["Мужская линия"])
        print("Женская линия:", gender_split["Женская линия"])

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

    def find_common_ancestor_ui(self, person1, person2):
        """Находит общего предка через UI."""
        ancestor = find_common_ancestor(self.data, person1, person2)
        if ancestor:
            print(f"Общий предок для {person1} и {person2}: {ancestor}")
        else:
            print(f"У {person1} и {person2} нет общих предков.")

if __name__ == "__main__":
    FamilyTreeApp().run()