import tkinter as tk
from tkinter import messagebox, colorchooser
import json
import os


class NotebookApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Notebook")
        self.window.geometry("500x550")
        self.window.resizable(True, True)

        # Файл для хранения заметок
        self.notes_file = "notesfornotebook.json"

        self.current_styles = {
            "bg_color": "#f0f0f0",
            "listbox_bg": "#ffffff",
            "listbox_fg": "#000000",
            "entry_bg": "#ffffff",
            "entry_fg": "#000000",
            "button_bg": "#f0f0f0",
            "font_family": "Arial",
            "font_size": 19
        }

        self.create_widgets()
        self.apply_styles()
        self.window.bind('<Return>', lambda event: self.calc())

        # Загружаем заметки при запуске
        self.load_notes()

    def quest(self):
        """Создает окно справки для кнопки ="""
        helper = tk.Toplevel(self.window)
        helper.title("Helper")
        helper.geometry("500x400")
        helper.resizable(True, True)
        label = tk.Label(helper,
                         text="Справка о кнопке = :\n\nИспользуйте математические\n символы для \nвыполнения соответствующих действий.\n\nПомните, что нельзя делить на ноль,\n писать буквы в заметку,\n в которой выполняете действие\n или нажимать эту кнопку без выбора заметки.",
                         font=("Arial", 16), justify="left")
        label.pack(pady=20)
        close_btn = tk.Button(helper, text="Закрыть", font=("Arial", 14), command=helper.destroy)
        close_btn.pack(pady=10)

    def quest2(self):
        """Создает окно справки о стилизации"""
        helper = tk.Toplevel(self.window)
        helper.title("Helper")
        helper.geometry("600x300")
        helper.resizable(False, False)
        text = """Справка о стилизации:

    1. Выберите элемент для настройки в выпадающем списке
    2. Нажмите "Выбрать цвет" для изменения цвета
    3. Выберите шрифт и его размер
    4. Используйте:
       - "Применить" - сохранить изменения
       - "Сбросить всё" - вернуть стандартные настройки
       - "Отмена" - отменить изменения"""

        label = tk.Label(helper, text=text, font=("Arial", 14), justify="left")
        label.pack(pady=20, padx=10)

        close_btn = tk.Button(helper, text="Закрыть", font=("Arial", 12), command=helper.destroy)
        close_btn.pack(pady=10)

    def save_notes(self):
        """Сохраняет все заметки в файл"""
        notes = self.listbox.get(0, tk.END)
        with open(self.notes_file, 'w', encoding='utf-8') as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)

    def load_notes(self):
        """Загружает заметки из файла при запуске"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    notes = json.load(f)
                    for note in notes:
                        self.listbox.insert(tk.END, note)
        except Exception as e:
            messagebox.showwarning("Ошибка", f"Не удалось загрузить заметки: {str(e)}")

    def add(self):
        tasks = self.enter.get()
        if tasks:
            self.listbox.insert(tk.END, tasks)
            self.enter.delete(0, tk.END)
            self.save_notes()  # Сохраняем после добавления
        else:
            messagebox.showwarning("Ошибка", "Поле пустое!")

    def delete(self):
        try:
            select = self.listbox.curselection()
            self.listbox.delete(select)
            self.save_notes()  # Сохраняем после удаления
        except:
            messagebox.showwarning("Ошибка", "Не выбрана заметка")

    def calc(self):
        try:
            select = self.listbox.curselection()
            if not select:
                calcul = self.enter.get()
                if not calcul:
                    messagebox.showwarning("Ошибка", "Не выбрана заметка и поле ввода пустое!")
                    return
                try:
                    result = eval(calcul)
                    note = f"{calcul} = {result}"
                    self.listbox.insert(tk.END, note)
                    self.enter.delete(0, tk.END)
                    self.save_notes()  # Сохраняем после вычисления
                except Exception as e:
                    messagebox.showwarning("Ошибка", f"Ошибка вычисления: {str(e)}")
                return

            index = select[0]
            calcul = self.listbox.get(index)
            try:
                result = eval(calcul)
                self.listbox.delete(index)
                self.listbox.insert(index, f"{calcul} = {result}")
                self.save_notes()  # Сохраняем после изменения
            except SyntaxError:
                messagebox.showwarning("Ошибка", "Некорректное математическое выражение!")
            except NameError:
                messagebox.showwarning("Ошибка", "Использованы недопустимые символы (например, буквы)!")
            except ZeroDivisionError:
                messagebox.showwarning("Ошибка", "Деление на ноль невозможно!")
            except Exception as e:
                messagebox.showwarning("Ошибка", f"Неизвестная ошибка: {str(e)}")
        except Exception as e:
            messagebox.showwarning("Ошибка", f"Ошибка обработки: {str(e)}")

    def create_widgets(self):
        # Listbox
        self.listbox = tk.Listbox(self.window, width=35, height=10)
        self.listbox.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        # Entry
        self.enter = tk.Entry(self.window, width=35, borderwidth=3, relief="solid", justify="left")
        self.enter.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Buttons
        self.add_but = tk.Button(self.window, text="Добавить заметку", command=self.add)
        self.add_but.grid(row=2, column=0, pady=5, sticky="ew")

        self.del_but = tk.Button(self.window, text="Удалить заметку", command=self.delete)
        self.del_but.grid(row=3, column=0, pady=5, sticky="ew")

        # Button frame
        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row=4, column=0, pady=10, sticky="ew")

        self.calculator_but = tk.Button(
            self.button_frame,
            text="=",
            command=self.calc,
            font=("Arial", 16, "bold"),
            width=3
        )
        self.calculator_but.pack(side="left", expand=True, padx=5)

        self.quest_but = tk.Button(self.button_frame, text="<== ?", command=self.quest)
        self.quest_but.pack(side="left", expand=True, padx=5)

        self.quest2_but = tk.Button(self.button_frame, text="? ==>", command=self.quest2)
        self.quest2_but.pack(side="left", expand=True, padx=5)

        self.style_but = tk.Button(self.button_frame, text="Стилизация", command=self.style_button)
        self.style_but.pack(side="left", expand=True, padx=5)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

    def apply_styles(self):
        """Применяет текущие стили ко всем виджетам"""
        self.window.config(bg=self.current_styles["bg_color"])

        self.listbox.config(
            bg=self.current_styles["listbox_bg"],
            fg=self.current_styles["listbox_fg"],
            font=(self.current_styles["font_family"], self.current_styles["font_size"])
        )

        self.enter.config(
            bg=self.current_styles["entry_bg"],
            fg=self.current_styles["entry_fg"],
            font=(self.current_styles["font_family"], self.current_styles["font_size"])
        )

        for btn in [self.add_but, self.del_but, self.calculator_but, self.quest_but, self.quest2_but, self.style_but]:
            btn.config(
                bg=self.current_styles["button_bg"],
                fg="black",
                font=(self.current_styles["font_family"], self.current_styles["font_size"]),
                activebackground=self.darken_color(self.current_styles["button_bg"]),
                highlightbackground=self.current_styles["button_bg"]
            )

    def darken_color(self, color, factor=0.8):
        """Затемняет цвет для activebackground"""
        if len(color) == 7 and color[0] == '#':
            rgb = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
            darkened = tuple(max(0, int(c * factor)) for c in rgb)
            return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        return color

    def style_button(self):
        st_color = tk.Toplevel(self.window)
        st_color.title("Стилизация")
        st_color.geometry("500x350")
        st_color.resizable(False, False)

        temp_styles = self.current_styles.copy()

        def apply_temp_styles():
            self.window.config(bg=temp_styles["bg_color"])
            self.listbox.config(bg=temp_styles["listbox_bg"], fg=temp_styles["listbox_fg"])
            self.enter.config(bg=temp_styles["entry_bg"], fg=temp_styles["entry_fg"])
            for btn in [self.add_but, self.del_but, self.calculator_but, self.quest_but, self.style_but]:
                btn.config(
                    bg=temp_styles["button_bg"],
                    activebackground=self.darken_color(temp_styles["button_bg"])
                )

        # Элементы интерфейса стилизации
        tk.Label(st_color, text="Элемент для настройки:").pack(pady=5)
        element_var = tk.StringVar(value="Фон приложения")
        elements = ["Фон приложения", "Фон списка", "Текст списка",
                    "Фон поля ввода", "Текст поля ввода", "Кнопки"]
        tk.OptionMenu(st_color, element_var, *elements).pack()

        # Выбор цвета
        def choose_color():
            color = colorchooser.askcolor()[1]
            if color:
                element = element_var.get()
                if element == "Фон приложения":
                    temp_styles["bg_color"] = color
                elif element == "Фон списка":
                    temp_styles["listbox_bg"] = color
                elif element == "Текст списка":
                    temp_styles["listbox_fg"] = color
                elif element == "Фон поля ввода":
                    temp_styles["entry_bg"] = color
                elif element == "Текст поля ввода":
                    temp_styles["entry_fg"] = color
                elif element == "Кнопки":
                    temp_styles["button_bg"] = color
                apply_temp_styles()

        tk.Button(st_color, text="Выбрать цвет", command=choose_color).pack(pady=5)

        # Настройки шрифта
        tk.Label(st_color, text="Шрифт:").pack()
        font_var = tk.StringVar(value=self.current_styles["font_family"])
        tk.OptionMenu(st_color, font_var, "Arial", "Times New Roman", "Courier", "Verdana").pack()

        tk.Label(st_color, text="Размер шрифта:").pack()
        size_var = tk.IntVar(value=self.current_styles["font_size"])
        tk.Scale(st_color, from_=8, to=32, variable=size_var, orient="horizontal").pack()

        # Кнопки управления
        def apply_changes():
            """Сохраняет изменения и закрывает окно"""
            self.current_styles = temp_styles.copy()
            self.current_styles["font_family"] = font_var.get()
            self.current_styles["font_size"] = size_var.get()
            self.apply_styles()
            st_color.destroy()

        def cancel_changes():
            """Отменяет изменения и закрывает окно"""
            self.apply_styles()  # Восстанавливаем исходные стили
            st_color.destroy()

        # В разделе с кнопками управления (в конце функции style_button)
        btn_frame = tk.Frame(st_color)
        btn_frame.pack(pady=10)

        def reset_all():
            """Полный сброс к заводским настройкам"""
            temp_styles.update({
                "bg_color": "#f0f0f0",
                "listbox_bg": "#ffffff",
                "listbox_fg": "#000000",
                "entry_bg": "#ffffff",
                "entry_fg": "#000000",
                "button_bg": "#f0f0f0",
                "font_family": "Arial",
                "font_size": 19
            })
            font_var.set("Arial")
            size_var.set(19)
            apply_temp_styles()

        tk.Button(btn_frame, text="Применить", command=apply_changes).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Сбросить всё", command=reset_all).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Отмена", command=cancel_changes).pack(side="left", padx=5)


if __name__ == "__main__":
    app = NotebookApp()
    try:
        app.window.mainloop()
    except KeyboardInterrupt:
        app.window.destroy()