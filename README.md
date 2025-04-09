# visualizing-graph-traversals

# Приветствую читатель. Это мой пет проект на тему обходов графов. 
## Я реализовал интерактивную программу для визуализации обходов графов (DFS, BFS, алгоритм Дейкстры) с возможностью добавления вершин и ребер, демонстрацией промежуточных этапов и результатов.

## Начнем. Что такое граф?
### •	Графы – фундаментальная структура данных, используемая в различных задачах информатики. Понимание алгоритмов обхода графов является важным элементом обучения, особенно в контексте подготовки школьников к олимпиадам и будущему обучению.


# Основная часть. Архитектура проекта.
## Обзор реализованных компонентов:  

## - Класс GraphVisualizer:  
  Основной класс, отвечающий за создание и управление графом, реализацию алгоритмов (DFS, BFS, Дейкстра) и взаимодействие с пользователем

![изображение](https://github.com/user-attachments/assets/48619990-61ff-4e53-b328-2eaf6a7fdcea)

## - Ключевые функции:

- add_vertex – добавление вершин с буквенной маркировкой (A, B, C, …).  
- add_edge – создание ребра между вершинами с размещением веса.  
- dfs и bfs – реализации обходов графа с визуальным выделением ребер, по которым идём.  
- run_dijkstra – алгоритм Дейкстры для поиска кратчайшего пути с пошаговой визуализацией.  
- check_cycles – проверка графа на наличие циклов.

![изображение](https://github.com/user-attachments/assets/1db7305d-e699-4f8e-8262-8e46a0e1b786)

```python
def add_edge(self, v1, v2):
    """Добавляет ребро между вершинами v1 и v2 с запросом веса."""
    weight = simpledialog.askinteger("Вес ребра", f"Введите вес для ребра {self.n_to_letter(v1)}->{self.n_to_letter(v2)}:", parent=self.master)
    if weight is None:
        return
    x1, y1 = self.vertices[v1]['x'], self.vertices[v1]['y']
    x2, y2 = self.vertices[v2]['x'], self.vertices[v2]['y']
    dx = x2 - x1
    dy = y2 - y1
    dis = (dx**2 + dy**2) ** 0.5
    if dis == 0:
        dis = 1

    start_x = x1 + (dx / dis) * self.vertex_radius
    start_y = y1 + (dy / dis) * self.vertex_radius
    end_x = x2 - (dx / dis) * self.vertex_radius
    end_y = y2 - (dy / dis) * self.vertex_radius

    line = self.canvas.create_line(start_x, start_y, end_x, end_y, fill="black", width=2)

    mid_x, mid_y = (start_x + end_x) / 2, (start_y + end_y) / 2
    if abs(dx) >= abs(dy):
        padx, pady = 0, -15
    else:
        padx, pady = 15, 0
    weight_text = self.canvas.create_text(mid_x + padx, mid_y + pady, text=str(weight), fill="black", font=6)
    
    self.edges[(v1, v2)] = {'weight': weight, 'line': line, 'text': weight_text}
    self.edges[(v2, v1)] = {'weight': weight, 'line': line, 'text': weight_text}
    self.adj_list[v1].append(v2)
    self.adj_list[v2].append(v1)
```

> *Математически вычисляются точки, от которых будет проходить прямая, соединяющая две вершины, с учетом того, что они имеют форму круга.*

# Описание работы программы

![изображение](https://github.com/user-attachments/assets/0cab4ba5-53c6-4213-9bce-15c22c48efde)

## Обход DFS
### Логика взаимодействия с программой:
##### - Пользователь через графический интерфейс добавляет вершины и соединяет их ребрами.
##### - При запуске алгоритма соответствующие вершины и ребра меняют цвет, что позволяет наблюдать последовательность обхода. Динамически происходит обновление стека вершин.
##### - Для каждого шага обхода подсвечиваются ребра, по которым происходит переход, что делает процесс наглядным.

![изображение](https://github.com/user-attachments/assets/0ffd2a35-f151-4e57-88c1-d5d557d78e62)


# Алгоритм Дейкстры. Динамическая подсветка.
### - Пользователь выбирает начальную и конечную вершины (в примере поиск кратчайшего пути из A в F) 
#### *Выполняется обход графа:*

![изображение](https://github.com/user-attachments/assets/14792c1e-21b3-4d30-a357-3a8968c147df)

- Зеленым выделяется вершина уже обработанная алгоритмом.
- Оранжевым выделяется ребро по которому добавляется следующая вершина.
- Фиолетовым выделяется текущая просматриваемая вершина. 

## Результат работы программы.

![изображение](https://github.com/user-attachments/assets/a6577359-227e-4b1b-a773-a903ce596511)

#### По окончанию работы алгоритма красным выделяется кратчайший маршрут из одной вершины в другую и справа на панели выводиться сам путь и его длина.

# Заключение

### Мой проект демонстрирует, как можно с помощью Python и Tkinter наглядно визуализировать сложные алгоритмы обхода графов. 
### Программа помогает школьникам лучше понять принципы работы алгоритмов DFS, BFS и Дейкстры.

## **- Плюсы проекта:**
- *Доступный интерфейс и визуализация каждого шага алгоритма.*
- *Интерактивность и возможность самостоятельного эксперимента с графами.*

- ***Не требуется установленный Python — всё заработает «из коробки» для любого пользователя через .exe файл, без необходимости установки дополнительного ПО.***

## **- Перспективы развития:**  
- Доработка интерфейса для более гибкого редактирования графа.
- Добавление дополнительных алгоритмов и функций (например, построение остова графа).

## Используемые технологии:
-	Язык программирования: Python
-	Библиотека для GUI: Tkinter
-	Среда разработки: Visual Studio Code



