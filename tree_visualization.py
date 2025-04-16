import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# Настройка шрифтов
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def validate_family_data(data):
    """
    Проверяет корректность данных семейного древа.
    - Каждый человек может иметь не более двух родителей.
    - Граф не должен содержать циклов.
    """
    G = nx.DiGraph()
    parents = {}

    for member in data:
        fio = member.get("fio", "Неизвестный")
        parent = member.get("parent", None)
        if parent:
            G.add_edge(parent, fio)
            parents[fio] = parents.get(fio, 0) + 1

    # Проверяем количество родителей
    for person, count in parents.items():
        if count > 2:
            print(f"Ошибка: у {person} больше двух родителей.")
            return False

    # Проверяем граф на наличие циклов
    if not nx.is_directed_acyclic_graph(G):
        print("Ошибка: граф содержит циклы.")
        return False

    print("Данные корректны.")
    return True


def get_generations(data):
    """
    Определяет поколения в семейном древе.
    """
    G = nx.DiGraph()

    # Добавляем узлы и рёбра
    for member in data:
        fio = member.get("fio", "Неизвестный")
        parent = member.get("parent", None)
        if parent:
            G.add_edge(parent, fio)

    # Определяем уровни поколений
    try:
        layers = list(nx.topological_generations(G))
        generations = {}
        for i, layer in enumerate(layers):
            generations[f"Поколение {i + 1}"] = layer
        return generations
    except nx.NetworkXError:
        print("Граф содержит циклы. Невозможно определить поколения.")
        return {}


def separate_by_gender(data):
    """
    Разделяет узлы по полу (мужской/женский).
    """
    G = nx.DiGraph()

    # Добавляем узлы с атрибутами
    for member in data:
        fio = member.get("fio", "Неизвестный")
        gender = member.get("gender", "unknown")  # По умолчанию "unknown", если пол не указан
        parent = member.get("parent", None)
        G.add_node(fio, gender=gender)
        if parent:
            G.add_edge(parent, fio)

    # Разделяем узлы по полу
    male_nodes = [node for node, attr in G.nodes(data=True) if attr.get('gender') == 'male']
    female_nodes = [node for node, attr in G.nodes(data=True) if attr.get('gender') == 'female']

    return {
        "Мужская линия": male_nodes,
        "Женская линия": female_nodes
    }

def find_common_ancestor(data, person1, person2):
    """
    Находит наименьшего общего предка для двух людей.
    """
    G = nx.DiGraph()

    # Добавляем узлы и рёбра
    for member in data:
        fio = member.get("fio", "Неизвестный")
        parent = member.get("parent", None)
        if parent:
            G.add_edge(parent, fio)

    # Находим всех предков для обоих людей
    ancestors1 = nx.ancestors(G, person1)
    ancestors2 = nx.ancestors(G, person2)

    # Находим пересечение множеств предков
    common_ancestors = ancestors1.intersection(ancestors2)
    if common_ancestors:
        return common_ancestors
    else:
        return None


def visualize_tree(data, tree_image):
    print(f"Visualizing tree with data: {data}")  # Отладочное сообщение
    G = nx.DiGraph()

    # Добавляем всех родителей как узлы, даже если они не указаны в данных
    for member in data:
        parent = member.get("parent", None)
        if parent:
            G.add_node(parent, label=parent)  # Создаем узел для родителя

    # Добавляем узлы и рёбра
    for member in data:
        fio = member.get("fio", "Неизвестный")
        birthdate = member.get("birthdate", "")
        parent = member.get("parent", None)

        # Создаем метку для узла
        label = f"{fio}\n{birthdate}" if birthdate else fio  # ФИО + дата рождения или только ФИО

        # Добавляем узел с меткой
        G.add_node(fio, label=label)  # Явно добавляем атрибут 'label'
        if parent:
            G.add_edge(parent, fio)

    # Проверяем граф на наличие циклов
    if not nx.is_directed_acyclic_graph(G):
        print("Граф содержит циклы. Используем BFS для определения уровней.")
        layers = list(nx.bfs_layers(G, source=None))
    else:
        try:
            layers = list(nx.topological_generations(G))
        except nx.NetworkXError:
            # Если граф содержит циклы, используем BFS
            layers = list(nx.bfs_layers(G, source=None))

    # Создаем позиции узлов с отступами
    pos = {}
    vertical_spacing = 1.5  # Вертикальный отступ между уровнями
    horizontal_spacing = 1.5  # Горизонтальный отступ между узлами одного уровня

    for i, layer in enumerate(layers):
        for j, node in enumerate(layer):
            # Располагаем узлы с отступами
            x = j * horizontal_spacing  # Горизонтальное размещение с отступом
            y = -i * vertical_spacing  # Вертикальное размещение с отступом
            pos[node] = (x, y)

    # Создаем фигуру и ось
    fig, ax = plt.subplots(figsize=(17, 9))

    # Рисуем узлы как прямоугольники
    for node, (x, y) in pos.items():
        # Проверяем наличие атрибута 'label'
        label = G.nodes[node].get('label', 'Нет данных')  # Если 'label' отсутствует, используем значение по умолчанию

        # Вычисляем размер прямоугольника на основе длины текста
        bbox = ax.text(x, y, label, ha='center', va='center').get_window_extent(renderer=ax.figure.canvas.get_renderer())
        rect_width = bbox.width / 72 + 0.2  # Добавляем небольшой отступ
        rect_height = bbox.height / 72 + 0.2  # Добавляем небольшой отступ

        # Рисуем прямоугольник
        rect = Rectangle((x - rect_width / 2, y - rect_height / 2), rect_width, rect_height,
                         facecolor='lightblue', edgecolor='black')
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center')

    # Рисуем рёбра
    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='gray'))

    # Настройки осей
    ax.set_xlim(-1, len(pos) + 1)
    ax.set_ylim(-len(layers), 1)
    ax.axis('off')  # Скрываем оси

    # Добавляем заголовок
    ax.text(0.5, 1.05, "Генеалогическое древо семьи", transform=ax.transAxes,
            fontsize=14, ha='center', va='bottom')

    # Сохраняем график в файл
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)  # Создаем папку, если её нет
    temp_file_path = os.path.join(temp_dir, "tree.png")

    # Сохраняем изображение
    plt.savefig(temp_file_path)
    print(f"Saved tree image to: {temp_file_path}")  # Отладочное сообщение
    tree_image.source = temp_file_path  # Присваиваем путь к изображению
    plt.close()