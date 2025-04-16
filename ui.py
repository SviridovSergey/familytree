from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image

class FamilyTreeUI(BoxLayout):
    def __init__(self, add_member_callback, update_tree_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        # Поле для ввода данных
        self.input_layout = BoxLayout(orientation="vertical", size_hint=(1, 0.3))
        self.fio_input = TextInput(hint_text="Введите ФИО", multiline=False)
        self.birthdate_input = TextInput(hint_text="Дата рождения (ГГГГ-ММ-ДД)", multiline=False)
        self.parent_input = TextInput(hint_text="ФИО родителя (если есть)", multiline=False)
        self.add_button = Button(text="Добавить члена семьи", on_press=self.on_add_button)

        self.input_layout.add_widget(Label(text="Добавление нового члена семьи"))
        self.input_layout.add_widget(self.fio_input)
        self.input_layout.add_widget(self.birthdate_input)
        self.input_layout.add_widget(self.parent_input)
        self.input_layout.add_widget(self.add_button)

        # Виджет для отображения дерева
        self.tree_image = Image(source="", size_hint=(1, 0.7))

        self.add_widget(self.input_layout)
        self.add_widget(self.tree_image)

        # Колбэки
        self.add_member_callback = add_member_callback
        self.update_tree_callback = update_tree_callback

    def on_add_button(self, instance):
        """Обработчик нажатия на кнопку добавления члена семьи."""
        fio = self.fio_input.text.strip()
        birthdate = self.birthdate_input.text.strip()
        parent_fio = self.parent_input.text.strip()

        if not fio or not birthdate:
            self.tree_image.source = ""  # Очистить изображение
            return

        # Вызываем колбэк для добавления члена семьи
        self.add_member_callback(fio, birthdate, parent_fio)
        self.tree_image.source = ""  # Очистить изображение перед обновлением
        self.update_tree_callback()