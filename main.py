import tkinter as tk
from tkinter import simpledialog, messagebox
import time
from collections import deque

class GraphVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Визуализация обходов графа (DFS, BFS, Дейкстра)")
        self.canvas = tk.Canvas(master, width=800, height=600, bg="white")
        self.canvas.grid(row=0, column=0, padx=15, pady=10)

        # Параметры задержки для визуализации
        self.time_sleep = 1.1

        # Словари для хранения вершин, ребер и списка смежности
        self.vertices = {}   # {id: {'x': x, 'y': y, 'oval': oval, 'text': vertex_text}}
        self.edges = {}      # {(v1, v2): {'weight': weight, 'line': line, 'text': weight_text}}
        self.adj_list = {}   # {id: [список соседей]}

        self.vertex_id = 0
        self.vertex_radius = 25
        self.selected_vertex = None  # для режима добавления ребра
        self.mode = "vertex"         # текущий режим: "vertex", "edge", "dijkstra"

        self.dijkstra_start = None
        self.dijkstra_end = None

        self.control_frame = tk.Frame(master, bg="lightgray", width=300, height=600)
        self.control_frame.grid(row=0, column=1, sticky="n", padx=15, pady=10)
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_propagate(False)

        # Используем grid для размещения элементов панели управления
        self.mode_button = tk.Button(self.control_frame, text="Режим: Добавление вершин", 
                                     command=self.toggle_mode, 
                                     bg="#e0e0e0", padx=10, pady=5, relief="groove",
                                        cursor="hand2")
        self.mode_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.dfs_button = tk.Button(self.control_frame, text="Запустить DFS", 
                                    command=self.start_dfs, bg="#e0e0e0", padx=10, pady=5, relief="groove")
        self.dfs_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.bfs_button = tk.Button(self.control_frame, text="Запустить BFS", 
                                    command=self.start_bfs, bg="#e0e0e0", padx=10, pady=5, relief="groove")
        self.bfs_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.dijkstra_button = tk.Button(self.control_frame, text="Запустить Дейкстру", 
                                         command=self.activate_dijkstra_mode, bg="#e0e0e0", padx=10, pady=5, relief="groove")
        self.dijkstra_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.cycle_button = tk.Button(self.control_frame, text="Проверить циклы", 
                                      command=self.check_cycles, bg="#e0e0e0", padx=10, pady=5, relief="groove")
        self.cycle_button.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        self.stack_label = tk.Label(self.control_frame, text="Стэк/Очередь: []", bg="lightgray", font=("Arial", 10, "bold"))
        self.stack_label.grid(row=5, column=0, padx=5, pady=10, sticky="w", columnspan=2)

        self.dijkstra_label = tk.Label(self.control_frame, text="", bg="lightgray", font=6, wraplength=280)
        self.dijkstra_label.grid(row=6, column=0, padx=5, pady=10, sticky="w")

        self.result_label = tk.Label(
            self.control_frame, 
            text="Результат: ", 
            bg="PaleTurquoise2", 
            font=("Arial", 12, "bold"), 
            wraplength=280,
        )
        
        self.result_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="we")

        self.reset_frame = tk.Frame(self.control_frame, bg="lightgray")
        self.reset_frame.grid(row=8, column=0, padx=5, pady=10, sticky="ew")

        self.full_reset_button = tk.Button(self.reset_frame, text="Полный сброс", 
                                           command=self.full_reset, bg="#d0d0ff", padx=5, pady=3, relief="groove")
        self.full_reset_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.reset_edges_button = tk.Button(self.reset_frame, text="Сброс ребер", 
                                            command=self.reset_edges, bg="#d0d0ff", padx=5, pady=3, relief="groove")
        self.reset_edges_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.delete_edge_button = tk.Button(self.reset_frame, text="Удалить ребра", 
                                            command=self.delete_edge_btn, bg="#d0d0ff", padx=5, pady=3, relief="groove")
        self.delete_edge_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.reset_visual_button = tk.Button(self.reset_frame, text="Сброс визуализации", 
                                             command=self.reset_visualization, bg="#d0d0ff", padx=5, pady=3, relief="groove")
        self.reset_visual_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        
        self.help_exit_frame = tk.Frame(self.control_frame, bg="lightgray")
        self.help_exit_frame.grid(row=9, column=0, padx=5, pady=10, sticky="ew")
        self.help_exit_frame.grid_columnconfigure(0, weight=1)
        self.help_exit_frame.grid_columnconfigure(1, weight=1)

        self.help_button = tk.Button(
            self.help_exit_frame,
            text="Помощь",
            command=self.show_help,
            bg="#d0d0ff",
            padx=5,
            pady=3,
            relief="groove"
        )
        self.help_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.exit_button = tk.Button(
            self.help_exit_frame,
            text="Выход",
            command=self.master.destroy,
            bg="#d0d0ff",
            padx=5,
            pady=3,
            relief="groove"
        )
        self.exit_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def show_help(self):
        """Отображает окно с руководством пользователя с прокруткой"""
        help_window = tk.Toplevel(self.master)
        help_window.title("Руководство пользователя")
        help_window.geometry("600x700")
        help_window.resizable(False, False)

        main_frame = tk.Frame(help_window)
        main_frame.pack(fill=tk.BOTH, expand=1)
        help_scroll = tk.Scrollbar(main_frame)
        help_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        help_text = tk.Text(
            main_frame,
            wrap=tk.WORD,
            yscrollcommand=help_scroll.set,
            font=("Arial", 10),
            padx=15,
            pady=15
        )
        help_text.pack(fill=tk.BOTH, expand=1)
        help_scroll.config(command=help_text.yview)

        help_content = """Инструкция по использованию программы:

    1. Добавление вершин:
    - Режим по умолчанию.
    - Кликните левой кнопкой мыши на холст для создания вершины.

    2. Добавление ребер:
    - Переключитесь в режим 'Добавление ребра'.
    - Последовательно кликните на две вершины.
    - Введите вес ребра во всплывающем окне.

    3. Обход в глубину (DFS):
    - Нажмите кнопку 'Запустить DFS'.
    - Введите начальную вершину (A, B, C...).
    - Визуализация:
        * Желтый - текущая вершина
        * Зеленый - полностью обработанная вершина
        * Оранжевые ребра - текущий путь

    4. Обход в ширину (BFS):
    - Нажмите кнопку 'Запустить BFS'.
    - Автоматически начинается с вершины A.
    - Визуализация:
        * Желтый - обрабатываемая вершина
        * Зеленый - посещенные вершины
        * Мигающие оранжевые ребра - добавляемые в очередь

    5. Алгоритм Дейкстры:
    - Нажмите кнопку 'Запустить Дейкстру'.
    - Последовательно выберите начальную и конечную вершины.
    - Визуализация:
        * Оранжевый - стартовая вершина
        * Розовый - конечная вершина
        * Фиолетовый - текущая обрабатываемая вершина
        * Красным - найденный кратчайший путь

    6. Проверка циклов:
    - Нажмите кнопку 'Проверить циклы'

    7. Управление графом:
    - Полный сброс: удаляет все элементы
    - Сброс ребер: удаляет только соединения
    - Удаление ребер: режим выбора ребер для удаления

    8. Цветовая схема:
    - Светло-голубой: неактивная вершина
    - Красная обводка: выбранная вершина
    - Желтый: активная обработка
    - Зеленый: завершенная обработка
    - Красный: кратчайший путь/выделение"""
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)  

        close_button = tk.Button(
            help_window,
            text="Закрыть",
            command=help_window.destroy,
            bg="#e0e0e0",
            padx=10,
            pady=5
        )
        close_button.pack(pady=5)

    def toggle_mode(self):
        """Переключает режим между добавлением вершин и ребер."""
        if self.mode == "vertex":
            self.mode = "edge"
            self.mode_button.config(text="Режим: Добавление ребра")
        else:
            self.mode = "vertex"
            self.mode_button.config(text="Режим: Добавление вершин")
        self.selected_vertex = None

    def to_add_vertex(self):
        self.mode = "vertex"
        self.mode_button.config(text="Режим: Добавление вершин")
        self.selected_vertex = None

    def activate_dijkstra_mode(self):
        """Переводит программу в режим выбора вершин для алгоритма Дейкстры."""
        self.mode = "dijkstra"
        self.dijkstra_start = None
        self.dijkstra_end = None
        self.dijkstra_label.config(text="Выберите начальную вершину")
        self.mode_button.config(text="Режим: Дейкстра")

    def on_canvas_click(self, event):
        """Обрабатывает клики по холсту в зависимости от текущего режима."""
        if self.mode == "vertex":
            self.add_vertex(event.x, event.y)
        elif self.mode == "delete_edge":
            clicked_vertex = self.get_vertex_at(event.x, event.y)
            if clicked_vertex is not None:
                if self.selected_vertex is None:
                    self.selected_vertex = clicked_vertex
                    self.canvas.itemconfig(self.vertices[clicked_vertex]['oval'], outline="red", width=3)
                else:
                    if clicked_vertex == self.selected_vertex:
                        self.canvas.itemconfig(self.vertices[self.selected_vertex]['oval'], outline="black", width=1)
                        self.selected_vertex = None
                    else:
                        self.delete_edge(self.selected_vertex, clicked_vertex)
                        self.canvas.itemconfig(self.vertices[self.selected_vertex]['oval'], outline="black", width=1)
                        self.selected_vertex = None

        elif self.mode == "edge":
            clicked_vertex = self.get_vertex_at(event.x, event.y)
            if clicked_vertex is not None:
                if self.selected_vertex is None:
                    self.selected_vertex = clicked_vertex
                    self.canvas.itemconfig(self.vertices[clicked_vertex]['oval'], outline="red", width=3)
                else:
                    if clicked_vertex == self.selected_vertex:
                        self.canvas.itemconfig(self.vertices[self.selected_vertex]['oval'], outline="black", width=1)
                        self.selected_vertex = None
                    else:
                        self.add_edge(self.selected_vertex, clicked_vertex)
                        self.canvas.itemconfig(self.vertices[self.selected_vertex]['oval'], outline="black", width=1)
                        self.selected_vertex = None
        elif self.mode == "dijkstra":
            clicked_vertex = self.get_vertex_at(event.x, event.y)
            if clicked_vertex is not None:
                if self.dijkstra_start is None:
                    self.dijkstra_start = clicked_vertex
                    self.canvas.itemconfig(self.vertices[clicked_vertex]['oval'], fill="orange")
                    self.dijkstra_label.config(text="Выберите конечную вершину")
                elif self.dijkstra_end is None:
                    self.dijkstra_end = clicked_vertex
                    self.canvas.itemconfig(self.vertices[clicked_vertex]['oval'], fill="pink")
                    self.dijkstra_label.config(text="Выполняется алгоритм Дейкстры...")
                    self.master.update()
                    self.run_dijkstra(self.dijkstra_start, self.dijkstra_end)
                    self.dijkstra_label.config(text="Алгоритм Дейкстры выполнен. Результаты показаны на графе.")
                    time.sleep(self.time_sleep)
                    self.mode = "vertex"
                    self.dijkstra_start = None
                    self.dijkstra_end = None

    def n_to_letter(self, num):
        return chr(ord('A') + num)

    def add_vertex(self, x, y):
        if self.get_vertex_at(x, y) == None:
            oval = self.canvas.create_oval(x - self.vertex_radius, y - self.vertex_radius,
                                        x + self.vertex_radius, y + self.vertex_radius,
                                        fill="lightblue", outline="black", width=1)
            label = self.n_to_letter(self.vertex_id)
            vertex_text = self.canvas.create_text(x, y, text=label)
            self.vertices[self.vertex_id] = {'x': x, 'y': y, 'oval': oval, 'text': vertex_text}
            self.adj_list[self.vertex_id] = []  
            self.vertex_id += 1

    def get_vertex_at(self, x, y):
        """Определяет, находится ли клик внутри области какой-либо вершины."""
        for vid, data in self.vertices.items():
            vx, vy = data['x'], data['y']
            if (x - vx)**2 + (y - vy)**2 <= self.vertex_radius**2:
                return vid
        return None

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

    def start_dfs(self):
        """Запускает обход в глубину (DFS) с визуализацией, подсвечивая ребра по пути."""
        self.reset_visualization()  
        str_start_vertex = simpledialog.askstring("Начальная вершина", 
                                                  "Введите начальную вершину (A, B...)", 
                                                  parent=self.master)
        if str_start_vertex != "" or str_start_vertex != None:
            start_vertex = ord(str_start_vertex.upper())-ord("A")
        else:
            messagebox.showinfo("Информация", "Поле не может быть пустым!")   
            return
        if start_vertex not in self.vertices.keys():
            messagebox.showinfo("Информация", "Такой вершины не существует!")   
            return
        if self.vertices:
            self.dfs_stack = []
            self.visited = set()
            self.stack_label.config(text="Стэк: []")
            self.dfs(start_vertex)

    def dfs(self, vertex):
        """Рекурсивный обход DFS с задержками и подсветкой ребер, по которым идём."""
        self.dfs_stack.append(vertex)
        self.stack_label.config(text="Стэк: " + str(list(map(self.n_to_letter, self.dfs_stack))))
        self.canvas.itemconfig(self.vertices[vertex]['oval'], fill="yellow")
        self.master.update()
        time.sleep(self.time_sleep)
        self.visited.add(vertex)
        for neighbor in self.adj_list[vertex]:
            if neighbor not in self.visited:
                # Подсвечиваем ребро, по которому идём
                edge = self.edges.get((vertex, neighbor))
                if edge:
                    self.canvas.itemconfig(edge['line'], fill="orange", width=3)
                self.master.update()
                time.sleep(self.time_sleep/2)
                self.dfs(neighbor)
                if edge:
                    self.canvas.itemconfig(edge['line'], fill="black", width=2)
                self.master.update()
                time.sleep(self.time_sleep/2)
        self.canvas.itemconfig(self.vertices[vertex]['oval'], fill="green")
        self.dfs_stack.pop()
        self.stack_label.config(text="Стэк: " + str(list(map(self.n_to_letter, self.dfs_stack))))
        self.master.update()
        time.sleep(self.time_sleep)

    def start_bfs(self):
        """Запускает обход в ширину (BFS) с визуализацией и выводом доступности вершин."""
        self.reset_visualization()
        if self.vertices:
            start_vertex = 0
            self.bfs(start_vertex)

    def bfs(self, start_vertex):
        """Обход BFS с использованием очереди, подсветкой ребер при добавлении соседей и задержками для визуализации."""
        queue = deque([start_vertex])
        visited = {start_vertex}
        self.stack_label.config(text="Очередь: " + str(list(map(self.n_to_letter, queue))))
        while queue:
            vertex = queue.popleft()
            self.stack_label.config(text="Очередь: " + str(list(map(self.n_to_letter, queue))))
            self.canvas.itemconfig(self.vertices[vertex]['oval'], fill="yellow")
            self.master.update()
            time.sleep(self.time_sleep)
            self.canvas.itemconfig(self.vertices[vertex]['oval'], fill="green")
            for neighbor in self.adj_list[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    # Подсвечиваем ребро от текущей вершины к соседу
                    edge = self.edges.get((vertex, neighbor))
                    if edge:
                        self.canvas.itemconfig(edge['line'], fill="orange", width=3)
                        self.master.update()
                        time.sleep(self.time_sleep/2)
                        self.canvas.itemconfig(edge['line'], fill="black", width=2)
                    self.stack_label.config(text="Очередь: " + str(list(map(self.n_to_letter, queue))))
                    self.master.update()
                    time.sleep(self.time_sleep/2)
        # Вывод информации о доступности вершин
        if len(visited) == len(self.vertices):
            result = "Все вершины доступны"
        else:
            result = f"Не все вершины доступны: посещено {len(visited)} из {len(self.vertices)}"
        self.result_label.config(text="Результат: " + result)

    def check_cycles(self):
        """Проверяет наличие циклов в графе с использованием DFS (учёт родительской вершины)."""
        visited = set()
        def dfs_cycle(v, parent):
            visited.add(v)
            for neighbor in self.adj_list[v]:
                if neighbor not in visited:
                    if dfs_cycle(neighbor, v):
                        return True
                elif neighbor != parent:
                    return True
            return False
        
        has_cycle = False
        for v in self.vertices:
            if v not in visited:
                if dfs_cycle(v, -1):
                    has_cycle = True
                    break
        if has_cycle:
            self.result_label.config(text="Результат: Граф содержит цикл")
        else:
            self.result_label.config(text="Результат: Граф не содержит циклов")
    
    def run_dijkstra(self, start, end):
        """Реализует алгоритм Дейкстры с пошаговой визуализацией и выделением кратчайшего пути,
        включая подсветку ребер при релаксации."""
        self.reset_visualization()
        distances = {v: float('inf') for v in self.vertices}
        previous = {v: None for v in self.vertices}
        distances[start] = 0
        visited = set()
        
        while len(visited) < len(self.vertices):
            current = None
            current_distance = float('inf')
            for v in self.vertices:
                if v not in visited and distances[v] < current_distance:
                    current_distance = distances[v]
                    current = v
            if current is None:
                break
            self.canvas.itemconfig(self.vertices[current]['oval'], fill="purple")
            self.master.update()
            time.sleep(self.time_sleep)
            for neighbor in self.adj_list[current]:
                if neighbor in visited:
                    continue
                edge = self.edges.get((current, neighbor))
                if edge is None:
                    continue
                weight = edge['weight']
                if distances[current] + weight < distances[neighbor]:
                    distances[neighbor] = distances[current] + weight
                    previous[neighbor] = current
                # Подсвечиваем ребро, по которому идём от current к neighbor
                self.canvas.itemconfig(edge['line'], fill="orange", width=3)
                self.master.update()
                time.sleep(self.time_sleep/1.25)
                self.canvas.itemconfig(edge['line'], fill="black", width=2)
                self.canvas.itemconfig(self.vertices[neighbor]['oval'], fill="yellow")
                self.master.update()
                time.sleep(self.time_sleep/1.25)
            visited.add(current)
            self.canvas.itemconfig(self.vertices[current]['oval'], fill="green")
            self.master.update()
            time.sleep(self.time_sleep)
        
        if distances[end] == float('inf'):
            result_text = "Путь не найден"
            self.result_label.config(text="Результат: " + result_text)
            return
        
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        for i in range(len(path) - 1):
            v1 = path[i]
            v2 = path[i + 1]
            edge = self.edges.get((v1, v2))
            if edge:
                self.canvas.itemconfig(edge['line'], fill="#DC143C", width=4)
            self.canvas.itemconfig(self.vertices[path[i]]['oval'], fill="#DC143C")
            self.master.update()
            time.sleep(self.time_sleep)
        self.canvas.itemconfig(self.vertices[path[-1]]['oval'], fill="#DC143C")
        self.master.update()
        result_text = f"Кратчайший путь: {' -> '.join(map(self.n_to_letter, path))} с длиной {distances[end]}"
        self.result_label.config(text="Результат: " + result_text)

    def reset_visualization(self):
        """Сбрасывает окраску вершин и ребер до исходного состояния."""
        for vid, data in self.vertices.items():
            self.canvas.itemconfig(data['oval'], fill="lightblue")
        for cur in self.edges:
            edge = self.edges.get(cur)
            if edge:
                self.canvas.itemconfig(edge['line'], fill="black", width=2)

    def full_reset(self):
        """Полный сброс: удаление всех вершин, ребер и сброс внутренних структур."""
        self.canvas.delete("all")
        self.vertices.clear()
        self.edges.clear()
        self.adj_list.clear()

        self.vertex_id = 0
        self.selected_vertex = None
        self.result_label.config(text="Результат: ")
        self.dijkstra_label.config(text="")
        self.to_add_vertex()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def reset_edges(self):
        """Удаляет все ребра, оставляя вершины."""
        for key in list(self.edges.keys()):
            edge = self.edges.get(key)
            if edge:
                self.canvas.delete(edge['line'])
                self.canvas.delete(edge['text'])
                if key[0] < key[1]:
                    self.edges.pop((key[0], key[1]), None)
                    self.edges.pop((key[1], key[0]), None)
        for v in self.adj_list:
            self.adj_list[v] = [n for n in self.adj_list[v] if n in self.vertices]
        self.result_label.config(text="Результат: Ребра сброшены")

    def to_pointer(self):
        """Делает курсор при наведении типа pointer"""
        for el, data in self.vertices.items():
            oval = data["oval"]

    def delete_edge_btn(self):
        """Кнопка удалить ребро"""
        self.mode = "delete_edge"
        # self.to_pointer()
        
    def delete_edge(self, v1, v2):
        """Удаляет ребро, выбранное пользователем, по указанию вершин."""
        if (v1, v2) in self.edges:
            edge = self.edges.get((v1, v2))
            self.canvas.delete(edge['line'])
            self.canvas.delete(edge['text'])
            self.edges.pop((v1, v2), None)
            self.edges.pop((v2, v1), None)
            if v2 in self.adj_list[v1]:
                self.adj_list[v1].remove(v2)
            if v1 in self.adj_list[v2]:
                self.adj_list[v2].remove(v1)
            messagebox.showinfo("Информация", f"Ребро {self.n_to_letter(v1)}-{self.n_to_letter(v2)} удалено")
        else:
            messagebox.showinfo("Информация", "Ребро не найдено")
        self.mode = "vertex"

    def reset_visualization_button(self):
        """Сбрасывает только визуализацию (окраску) без удаления данных."""
        messagebox.showinfo("Информация", "Результат: Визуализация сброшена")   
        self.reset_visualization()

    def reset_visualization(self):
        """Сбрасывает окраску вершин и ребер до исходного состояния."""
        for vid, data in self.vertices.items():
            self.canvas.itemconfig(data['oval'], fill="lightblue")
        for cur in self.edges:
            edge = self.edges.get(cur)
            if edge:
                self.canvas.itemconfig(edge['line'], fill="black", width=2)
        self.result_label.config(text="Результат: ")
        self.dijkstra_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = GraphVisualizer(root)
    root.mainloop()
