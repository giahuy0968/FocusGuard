import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, Toplevel, ttk
import csv
import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
from tkinter import StringVar
import subprocess
import os
import numpy as np
import random
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import threading
def show_notification(message):
    def create_window():
        root = tk.Tk()
        root.overrideredirect(True)

        window_width = 300
        window_height = 100

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.configure(bg="lightyellow")

        label = tk.Label(root, text=message, font=("Arial", 12), bg="lightyellow", wraplength=280)
        label.pack(expand=True)

        root.after(10000, root.destroy)
        root.mainloop()

    threading.Thread(target=create_window).start()
def format_label(label):
    words = label.split()
    return '\n'.join([' '.join(words[i:i+2]) for i in range(0, len(words), 2)])
def show_empty_chart():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie([1], labels=[""], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    chart_path = "./images/empty_chart.png"
    plt.savefig(chart_path)
    plt.close(fig)

    if os.path.exists(chart_path):
        img = Image.open(chart_path)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)

        if hasattr(frame_plot, "chart_label"):
            root.chart_label.configure(image=img_tk)
            root.chart_label.image = img_tk
        else:
            root.chart_label = ttk.Label(frame_plot, image=img_tk)
            root.chart_label.image = img_tk
            root.chart_label.grid(row=0, column=0)

        temp_img = Image.open("./images/kimtuthaphoctap.jpg")
        temp_img = temp_img.resize((200, 200)) 
        temp_img_tk = ImageTk.PhotoImage(temp_img)

        if hasattr(frame_plot, "temp_label"):
            root.temp_label.configure(image=temp_img_tk)
            root.temp_label.image = temp_img_tk
        else:
            root.temp_label = ttk.Label(frame_plot, image=temp_img_tk)
            root.temp_label.image = temp_img_tk
            root.temp_label.grid(row=0, column=1)  

def update_fatigue_pie_chart():
    try:
        with open("./database/fatigue_log.csv", "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file lịch sử")
        return

    if not data:
        messagebox.showinfo("Thông báo", "Không có dữ liệu để vẽ biểu đồ.")
        return

    fatigue_counts = {}
    for _, status in data:
        fatigue_counts[status] = fatigue_counts.get(status, 0) + 1

    fig, ax = plt.subplots(figsize=(5, 5))

    original_labels = fatigue_counts.keys()
    formatted_labels = [format_label(label) for label in original_labels]
    sizes = fatigue_counts.values()

    wedges, texts, autotexts = ax.pie(
        sizes, labels=formatted_labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 16}
    )
    ax.axis('equal')

    chart_path = "./images/fatigue_pie_chart.png"
    plt.savefig(chart_path)
    plt.close(fig)

    if os.path.exists(chart_path):
        img = Image.open(chart_path)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)

        if hasattr(frame_plot, "chart_label"):
            root.chart_label.configure(image=img_tk)
            root.chart_label.image = img_tk
        else:
            root.chart_label = ttk.Label(frame_plot, image=img_tk)
            root.chart_label.image = img_tk
            root.chart_label.grid(row=0, column=0)

        temp_img = Image.open("./images/kimtuthaphoctap.jpg")
        temp_img = temp_img.resize((200, 200))
        temp_img_tk = ImageTk.PhotoImage(temp_img)

        if hasattr(frame_plot, "temp_label"):
            root.temp_label.configure(image=temp_img_tk)
            root.temp_label.image = temp_img_tk
        else:
            root.temp_label = ttk.Label(frame_plot, image=temp_img_tk)
            root.temp_label.image = temp_img_tk
            root.temp_label.grid(row=0, column=1)
def turn_on_camera():
    show_notification("Thông báo\nBật máy ảnh để nhận diện cử chỉ vui lòng chờ...")
    subprocess.Popen(["python", "PhatHienMetMoi.py"])

def select_exercise():
    exercise_window = Toplevel(root)
    exercise_window.title("Bài tập thể dục")
    window_width = 700
    window_height = 470

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    exercise_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    exercise_window.resizable(False, False)

    frame = ttk.Frame(exercise_window)
    frame.pack()

    list_image = os.listdir("./excercise")
    list_image = [img for img in list_image if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    image_exercise = ttk.Label(frame)
    image_exercise.pack()

    current_image = {'filename': None}

    def change_image():
        available_images = [img for img in list_image if img != current_image['filename']]
        if not available_images:
            available_images = list_image 
        image_filename = random.choice(available_images)

        image_path = os.path.join("excercise", image_filename)
        image = Image.open(image_path)
        resized_image = image.resize((700, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)

        image_exercise.configure(image=photo)
        image_exercise.image = photo 
        current_image['filename'] = image_filename 

    change_button = ttk.Button(exercise_window, text="Đổi bài tập", command=change_image)
    change_button.pack(pady=10)

    change_image()

class TEECalculator:
    def __init__(self, BMR, BMI, activity_level, exercise_type, exercise_hours):
        self.BMR = BMR
        self.BMI = BMI
        self.activity_level = activity_level
        self.exercise_type = exercise_type
        self.exercise_hours = exercise_hours
        self.exercise_addition = 0
        self.TEE = self.calculate_TEE()
        self.TE = self.calculate_TE()

    def calculate_TEE(self):
        activity_multipliers = {
            1: 1.2,    
            2: 1.375,  
            3: 1.55,   
            4: 1.725, 
            5: 1.9    
        }
        multiplier = activity_multipliers.get(self.activity_level, 1.2)
        TEE = self.BMR * multiplier


        return round(TEE, 2)

    def calculate_TE(self):
        if self.exercise_type == "Nặng":
            exercise_addition = 400 * self.exercise_hours
        elif self.exercise_type == "Trung bình":
            exercise_addition = 300 * self.exercise_hours
        elif self.exercise_type == "Nhẹ":
            exercise_addition = 200 * self.exercise_hours
        else:
            exercise_addition = 0

        self.exercise_addition = exercise_addition
        if self.BMI < 18.5:
            TE = (self.TEE + self.BMR) + 500 - exercise_addition
        elif 18.5 <= self.BMI <= 24.9:
            TE = (self.TEE + self.BMR) - exercise_addition
        elif 25 <= self.BMI <= 29.9:
            TE = (self.TEE + self.BMR) - 500 - exercise_addition
        else:
            TE = (self.TEE + self.BMR) - 500 - exercise_addition
        return abs(round(TE))

class MealSelector:
    def __init__(self, TE, data_file='./database/data.csv'):
        self.TE = TE
        self.data_frame = pd.read_csv(data_file, delimiter=';', encoding='utf-8', header=None, names=['Ten mon an', 'calo', 'Trong luong'])
        self.data_frame['Trong luong'] = self.data_frame['Trong luong'].str.replace('g', '').astype(float)

    def select_food_items(self):
        selected_foods = []
        total_calories_selected = 0
        selected_indices = set()

        while abs(total_calories_selected - self.TE) > 10:
            food_row = random.choice(self.data_frame.index)
            if food_row in selected_indices:
                continue
            food = self.data_frame.loc[food_row]
            food_calories = int(food['calo'])
            if food_calories > self.TE or total_calories_selected + food_calories > self.TE:
                continue
            selected_foods.append(food)
            selected_indices.add(food_row)
            total_calories_selected += food_calories

            if total_calories_selected >= self.TE or len(selected_indices) == len(self.data_frame):
                break

        return selected_foods

    def train_linear_regression(self):
        X = self.data_frame['calo'].to_numpy().reshape(-1, 1)
        y = self.data_frame['Trong luong'].to_numpy().reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, y)
        return model

    def save_results(self, selected_foods, model):
        with open("./database/result.txt", "w", encoding='utf-8') as f:
            for food in selected_foods:
                predicted_weight = model.predict(np.array([[food['calo']]])).flatten()[0]
                f.write(f"{food['Ten mon an']};{round(food['calo'])};{round(food['Trong luong'], 2)};{round(predicted_weight, 2)}\n")

        with open("./database/result.txt", "r", encoding='utf-8') as f:
            lines = f.readlines()

        with open("./database/result_modified.txt", "w", encoding='utf-8') as f:
            for line in lines:
                parts = line.strip().split(';')
                modified_line = ' - '.join(parts[:-1])
                f.write(modified_line + '\n')

def read_food_data():
    foods = []
    try:
        with open("./database/result_modified.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(' - ')
                if len(parts) == 3:
                    foods.append(parts)
    except FileNotFoundError:
        print("Không tìm thấy file result_modified.txt.")
    return foods

def meal_suggestions():
    nutrition_window = Toplevel(root)
    nutrition_window.title("Gợi ý dinh dưỡng")
    nutrition_window.resizable(False, False)
    window_width = 830
    window_height = 550

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    nutrition_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    labels = ["Năm sinh", "Chiều cao (cm)", "Cân nặng (kg)", "Giới tính", "Mức độ vận động", "Mức độ luyện tập", "Thời gian luyện tập (giờ)"]
    entries = {}

    options = {
        "Giới tính": ["Nam", "Nữ"],
        "Mức độ vận động": ["Thụ động", "Nhẹ", "Trung bình", "Năng động", "Rất tích cực"],
        "Mức độ luyện tập": ["Không luyện tập", "Nhẹ", "Trung bình", "Nặng"]
    }

    for i, label_text in enumerate(labels):
        label = ttk.Label(nutrition_window, text=label_text)
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        var = StringVar()
        if label_text in options:
            combo = ttk.Combobox(nutrition_window, textvariable=var, values=options[label_text], width=28, state="readonly")
            combo.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            combo.set(options[label_text][0])
        else:
            entry = ttk.Entry(nutrition_window, textvariable=var, width=28)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        
        entries[label_text] = var
        
    label_calo_mat_di = ttk.Label(nutrition_window, text="Calo bị mất đi sau khi luyện tập: ")
    label_calo_mat_di.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    
    label_BMR = ttk.Label(nutrition_window, text="Chỉ số BMR: ")
    label_BMR.grid(row=1, column=2, padx=10, pady=5, sticky="w")
    
    label_BMI = ttk.Label(nutrition_window, text="Chỉ số BMI: ")
    label_BMI.grid(row=2, column=2, padx=10, pady=5, sticky="w")
    
    label_tinh_trang = ttk.Label(nutrition_window, text="Tình trạng: ")
    label_tinh_trang.grid(row=3, column=2, padx=10, pady=5, sticky="w")
    
    progressbar = ttk.Progressbar(nutrition_window, style='red')
    progressbar.grid(row=4, column=2, padx=10, pady=5, sticky="w")
    
    label_TEE = ttk.Label(nutrition_window, text="Nhu cầu năng lượng cho hoạt động (TEE): ")
    label_TEE.grid(row=5, column=2, padx=10, pady=5, sticky="w")
    
    label_TE = ttk.Label(nutrition_window, text="Tổng calo cần thiết cho 1 ngày (TE): ")
    label_TE.grid(row=6, column=2, padx=10, pady=5, sticky="w")
    
    tree_frame = ttk.Frame(nutrition_window)
    tree_frame.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10, padx=10)

    tree = ttk.Treeview(tree_frame, columns=("Tên món ăn", "Calo", "Trọng lượng"), show="headings")
    tree.heading("Tên món ăn", text="Tên món ăn", anchor="center")
    tree.heading("Calo", text="Calo", anchor="center")
    tree.heading("Trọng lượng", text="Trọng lượng", anchor="center")
    tree.column("Tên món ăn", width=250, anchor="center")
    tree.column("Calo", width=100, anchor="center")
    tree.column("Trọng lượng", width=120, anchor="center")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill=BOTH)

    def filter_and_suggest():
        age = int(entries["Năm sinh"].get())
        height = float(entries["Chiều cao (cm)"].get())
        weight = float(entries["Cân nặng (kg)"].get())
        gender = entries["Giới tính"].get()
        activity_level = ["Thụ động", "Nhẹ", "Trung bình", "Năng động", "Rất tích cực"].index(entries["Mức độ vận động"].get()) + 1
        exercise_type = entries["Mức độ luyện tập"].get()
        exercise_hours = float(entries["Thời gian luyện tập (giờ)"].get())
        now_year = datetime.datetime.now().year
        age = now_year - age
        BMI = weight / ((height / 100) ** 2)
        if gender == "Nữ":
            BMR = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
            BMR = round(BMR, 1)
            return BMR
        elif gender == "Nam":
            BMR = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
            BMR = round(BMR, 1)

        calculator = TEECalculator(BMR, BMI, activity_level, exercise_type, exercise_hours)
        
        label_calo_mat_di.config(text="Calo bị mất đi sau khi luyện tập: " + str(calculator.exercise_addition))
        label_BMR.config(text="Chỉ số BMR: " + str(round(BMR, 2)))
        label_BMI.config(text="Chỉ số BMI: " + str(round(BMI, 1)))
        if BMI < 18.5:
            label_tinh_trang.config(text="Tình trạng: Thiếu cân")
            progressbar.config(bootstyle="success") 
        elif BMI >= 18.5 and BMI <= 24.9:
            label_tinh_trang.config(text="Tình trạng: Bình Thường")
            progressbar.config(bootstyle="default")  
        elif BMI >= 25 and BMI <= 29.9:
            label_tinh_trang.config(text="Tình trạng: Thừa cân")
            progressbar.config(bootstyle="warning")  
        elif BMI >= 30:
            label_tinh_trang.config(text="Tình trạng: Béo phì")
            progressbar.config(bootstyle="danger")  
        progressbar["value"] = 100
        progressbar.update_idletasks()
        label_TEE.config(text="Nhu cầu năng lượng cho hoạt động (TEE): " + str(calculator.TEE))
        label_TE.config(text="Tổng calo cần thiết cho 1 ngày (TE): " + str(calculator.TE))
        selector = MealSelector(calculator.TE)
        selected_foods = selector.select_food_items()
        model = selector.train_linear_regression()
        selector.save_results(selected_foods, model)

        update_treeview()

    def update_treeview():
        food_data = read_food_data()

        for i in tree.get_children():
            tree.delete(i)

        for food in food_data:
            tree.insert("", "end", values=food)

    filter_button = ttk.Button(nutrition_window, text="Tính và Gợi ý", command=filter_and_suggest)
    filter_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

def show_fatigue_history():
    try:
        with open("./database/fatigue_log.csv", "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file lịch sử")
        return

    history_window = Toplevel(root)
    history_window.title("Lịch Sử Mệt Mỏi")
    window_width = 400
    window_height = 400

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    history_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    frame = ttk.Frame(history_window)
    frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=("Thời Gian", "Trạng Thái"), show="headings", selectmode="browse")
    tree.heading("Thời Gian", text="Thời Gian", anchor="center")
    tree.heading("Trạng Thái", text="Trạng Thái", anchor="center")
    tree.column("Thời Gian", width=150, anchor="center")
    tree.column("Trạng Thái", width=220, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    for i, row in enumerate(data):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", tk.END, values=row, tags=(tag,))
    tree.tag_configure("evenrow", background="#F0F0F0", foreground="black")
    tree.tag_configure("oddrow", background="white", foreground="black")

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn dòng cần xoá", parent=history_window)
            return
        index = tree.index(selected[0])
        tree.delete(selected[0])
        del data[index]
        with open("./database/fatigue_log.csv", "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)
        messagebox.showinfo("Thành công", "Đã xoá dòng đã chọn", parent=history_window)

    def delete_all():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xoá toàn bộ lịch sử?", parent=history_window):
            tree.delete(*tree.get_children())
            with open("./database/fatigue_log.csv", "w", encoding="utf-8-sig", newline="") as file:
                pass  
            messagebox.showinfo("Thành công", "Đã xoá toàn bộ lịch sử", parent=history_window)

    button_frame = ttk.Frame(history_window)
    button_frame.pack(pady=10)

    delete_btn = ttk.Button(button_frame, text="Xoá dòng đã chọn", command=delete_selected)
    delete_btn.grid(row=0, column=0, padx=10)

    clear_btn = ttk.Button(button_frame, text="Xoá toàn bộ lịch sử", command=delete_all)
    clear_btn.grid(row=0, column=1, padx=10)

root = tb.Window(themename="superhero")
root.title("FocusGuard")

window_width = 500
window_height = 620

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)


image_background_path = "./images/background.jpg"
image = Image.open(image_background_path)
resized_image = image.resize((500, 620), Image.LANCZOS)
photo = ImageTk.PhotoImage(resized_image)

image_background = ttk.Label(root, image=photo)
image_background.image = photo
image_background.place(x=0, y=0, relwidth=1, relheight=1)

style = tb.Style()
style.configure("TButton", font=("Helvetica", 12))

icon_path = "./images/icon.jpg"
icon = Image.open(icon_path)
resized_icon = icon.resize((80, 80), Image.LANCZOS)
icon = ImageTk.PhotoImage(resized_icon)
icon_label = tb.Label(root, image=icon)
icon_label.pack(pady=10)

camera_frame = tb.Frame(root)
camera_frame.pack(pady=10, padx=20, fill=X)

camera_btn = tb.Button(camera_frame, text="📷 Bật Máy Ảnh", bootstyle="primary", command=turn_on_camera)
camera_btn.pack(ipadx=10, ipady=20, fill=X)

top_frame = tb.Frame(root)
top_frame.pack(pady=10, padx=20, fill=X)

exercise_btn = tb.Button(top_frame, text="🏋️ Chọn Bài Thể Dục", bootstyle="success", command=select_exercise)
exercise_btn.grid(row=0, column=0, padx=2, ipadx=10, ipady=10, sticky="ew")

meal_btn = tb.Button(top_frame, text="🥗 Gợi Ý Thực Đơn", bootstyle="info", command=meal_suggestions)
meal_btn.grid(row=0, column=1, padx=2, ipadx=10, ipady=10, sticky="ew")

history_btn = tb.Button(root, text="📜 Lịch Sử Mệt Mỏi", bootstyle="warning", command=show_fatigue_history)
history_btn.pack(padx= 20, pady=10, ipadx=10, ipady=10, fill=X)

top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=1)

update_button = tb.Button(root, text="Cập nhật biểu đồ", bootstyle="primary", command=update_fatigue_pie_chart)
update_button.pack(pady=10, padx=20, fill=X)

frame_plot = ttk.Frame(root)
frame_plot.pack()
show_empty_chart()
root.mainloop()
