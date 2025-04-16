import networkx as nx
import matplotlib.pyplot as plt
from kivy.graphics.texture import Texture
from PIL import Image
import io
import numpy as np

# Настройка шрифтов
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def visualize_tree(data, label_widget):
    """Визуализирует дерево и отображает его в Kivy виджете."""
    G = nx.DiGraph()

    for member in data:
        G.add_node(member["fio"], label=f"{member['fio']}\n{member['birthdate']}")
        if member["parent"]:
            G.add_edge(member["parent"], member["fio"])

    # Создаем изображение графа
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)  # Расположение узлов
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'),
            node_size=3000, node_color="lightblue", font_size=8)
    plt.title("Семейное древо")

    # Преобразуем график в изображение
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = Image.open(buf)

    # Преобразуем PIL-изображение в текстуру Kivy
    image_data = np.array(image.convert('RGBA')).tobytes()
    texture = Texture.create(size=(image.width, image.height), colorfmt='rgba')
    texture.blit_buffer(image_data, colorfmt='rgba', bufferfmt='ubyte')

    # Отображаем текстуру в виджете
    label_widget.texture = texture
    plt.close()