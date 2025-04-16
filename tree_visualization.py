import networkx as nx
import matplotlib.pyplot as plt
import os

# Настройка шрифтов
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 8

def visualize_tree(data, tree_image):
    print(f"Visualizing tree with data: {data}")  # Отладочное сообщение
    G = nx.DiGraph()

    # Добавляем узлы и рёбра
    for member in data:
        G.add_node(member["fio"], label=f"{member['fio']}\n{member['birthdate']}")
        if member["parent"]:
            G.add_edge(member["parent"], member["fio"])

    # Определяем уровни узлов
    try:
        layers = list(nx.topological_generations(G))
    except nx.NetworkXError:
        # Если граф содержит циклы, используем BFS
        layers = list(nx.bfs_layers(G, source=None))

    # Создаем позиции узлов
    pos = {}
    for i, layer in enumerate(layers):
        for j, node in enumerate(layer):
            pos[node] = (j, -i)  # Горизонтальное размещение узлов, вертикальное разделение по уровням

    # Создаем изображение графа
    plt.figure(figsize=(17, 9))  # Размер графика

    # Отрисовываем график
    nx.draw(
        G,
        pos,
        with_labels=True,
        labels=nx.get_node_attributes(G, 'label'),
        node_size=2000,
        node_color="lightblue",
        font_size=8,
        arrows=True,
        edge_color="gray"
    )

    plt.title("Семейное древо")

    # Сохраняем график в файл
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)  # Создаем папку, если её нет
    temp_file_path = os.path.join(temp_dir, "tree.png")

    # Сохраняем изображение
    plt.savefig(temp_file_path)
    print(f"Saved tree image to: {temp_file_path}")  # Отладочное сообщение
    tree_image.source = temp_file_path  # Присваиваем путь к изображению
    plt.close()