# FocusGuard – Phiên bản nâng cấp giao diện bằng CustomTkinter
# Giữ nguyên logic gốc, chỉ thay đổi GUI (Runner.py)

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os
import sys
import csv
import random
import datetime
import subprocess
import tkinter as tk
from tkinter import messagebox, Toplevel
from tkinter import ttk
# Import thư viện mới
import customtkinter as ctk
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # render offscreen để tránh đụng GUI

# ---------------------------- cài đặt ----------------------------
# Đặt chế độ giao diện (System, Light, Dark)
ctk.set_appearance_mode("System")
# Đặt theme màu (blue, dark-blue, green)
ctk.set_default_color_theme("blue")

# ---------------------------- tiện ích (giữ nguyên) ----------------------------


def ensure_dir(path: str):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


# Tạo các thư mục cần thiết
ensure_dir("./images")
ensure_dir("./database")
ensure_dir("./excercise")


def show_notification(message: str):
    """Popup thông báo (Dùng Toplevel chuẩn của Tkinter)."""
    # Dùng Toplevel của tk thay vì ctk để có cửa sổ popup đơn giản
    win = Toplevel(root)
    win.overrideredirect(True)
    window_width, window_height = 300, 100
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    win.geometry(f"{window_width}x{window_height}+{x}+{y}")
    win.configure(bg="lightyellow")
    label = tk.Label(
        win, text=message, font=("Arial", 12), bg="lightyellow", wraplength=280
    )
    label.pack(expand=True, fill="both")
    win.after(5000, win.destroy)  # Tự đóng sau 5s (thay vì 10s cũ)


def format_label(label: str) -> str:
    words = label.split()
    return "\n".join([" ".join(words[i:i + 2]) for i in range(0, len(words), 2)])


def _set_dual_images_to_frame(frame, left_img_path, right_img_path, size=(250, 250)):
    """Hiển thị 2 ảnh (trái/phải) lên frame (đã sửa cho CustomTkinter)."""

    # CustomTkinter dùng CTkImage để quản lý ảnh tốt hơn

    # --- Ảnh trái (Biểu đồ) ---
    if os.path.exists(left_img_path):
        img_left = ctk.CTkImage(Image.open(left_img_path), size=size)
        if hasattr(frame, "chart_label"):
            frame.chart_label.configure(image=img_left, text="")
        else:
            frame.chart_label = ctk.CTkLabel(frame, image=img_left, text="")
        frame.chart_label.image = img_left  # Giữ reference
        frame .chart_label.grid(row=0,  column=0,  padx=(10, 0),  pady=10)
    else:
        # Xử lý nếu không có ảnh
        if hasattr(frame, "chart_label"):
            frame.chart_label.configure(
                image=None, text="(Không có ảnh biểu đồ)")
        else:
            frame.chart_label = ctk.CTkLabel(
                frame, text="(Không có ảnh biểu đồ)", width=size[0], height=size[1])
        frame .chart_label.grid(row=0,  column=0,  padx=(10, 0),  pady=10)

    # --- Ảnh phải (Ảnh phụ) ---
    if os.path.exists(right_img_path):
        img_right = ctk.CTkImage(Image.open(right_img_path), size=size)
        if hasattr(frame, "temp_label"):
            frame.temp_label.configure(image=img_right, text="")
        else:
            frame.temp_label = ctk.CTkLabel(frame, image=img_right, text="")
        frame.temp_label.image = img_right  # Giữ reference
        frame .temp_label.grid(row=0,  column=1,  padx=(10, 10),  pady=10)
    else:
        # Xử lý nếu không có ảnh
        if hasattr(frame, "temp_label"):
            frame.temp_label.configure(image=None, text="(Không có ảnh phụ)")
        else:
            frame.temp_label = ctk.CTkLabel(
                frame, text="(Không có ảnh phụ)", width=size[0], height=size[1])
        frame .temp_label.grid(row=0,  column=1,  padx=(10, 10),  pady=10)

# ---------------------------- biểu đồ (giữ nguyên logic) ----------------------------


def show_empty_chart():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie([1], labels=[""], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    chart_path = "./images/empty_chart.png"
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)
    _set_dual_images_to_frame(
        frame_plot, chart_path, "./images/kimtuthaphoctap.jpg", size=(250, 250)
    )


def update_fatigue_pie_chart():
    try:
        with open("./database/fatigue_log.csv", "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            data = list(reader)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file lịch sử")
        return
    if not data:
        messagebox.showinfo("Thông báo", "Không có dữ liệu để vẽ biểu đồ.")
        return

    fatigue_counts = {}
    for row in data:
        if len(row) >= 2:
            status = row[1]
            fatigue_counts[status] = fatigue_counts.get(status, 0) + 1

    fig, ax = plt.subplots(figsize=(5, 5))
    original_labels = list(fatigue_counts.keys())
    formatted_labels = [format_label(lb) for lb in original_labels]
    sizes = list(fatigue_counts.values())

    # Thêm màu nền cho biểu đồ matplotlib để hợp với Ctk
    fig.patch.set_facecolor('#f2f2f2')  # Màu sáng
    if ctk.get_appearance_mode() == "Dark":
        fig.patch.set_facecolor('#2b2b2b')  # Màu tối
        ax.tick_params(colors='white')
        plt.rcParams['text.color'] = 'white'

    ax.pie(sizes, labels=formatted_labels, autopct="%1.1f%%", startangle=90,
           textprops={"fontsize": 12})
    ax.axis("equal")
    chart_path = "./images/fatigue_pie_chart.png"
    plt.savefig(chart_path, bbox_inches="tight",
                transparent=True)  # Nền trong suốt
    plt.close(fig)
    _set_dual_images_to_frame(
        frame_plot, chart_path, "./images/kimtuthaphoctap.jpg", size=(250, 250)
    )
    # Reset màu text matplotlib về mặc định
    plt.rcParams['text.color'] = 'black'

# ---------------------------- chức năng camera (giữ nguyên) ----------------------------


def turn_on_camera():
    show_notification(
        "Thông báo\nBật máy ảnh để nhận diện cử chỉ, vui lòng chờ...")
    # Chạy đúng Python interpreter của venv
    subprocess.Popen([sys.executable, "PhatHienMetMoi.py"])

# ---------------------------- chọn bài tập (Nâng cấp GUI) ----------------------------


def select_exercise():
    # Dùng CTkToplevel thay cho Toplevel
    exercise_window = ctk.CTkToplevel(root)
    exercise_window.title("Bài tập thể dục")
    window_width, window_height = 700, 470
    # (Cách căn giữa cửa sổ của CTk)
    exercise_window.geometry(f"{window_width}x{window_height}")
    exercise_window.grab_set()  # Khóa tương tác với cửa sổ chính
    exercise_window.resizable(False, False)

    frame = ctk.CTkFrame(exercise_window, fg_color="transparent")
    frame.pack(fill="both", expand=True)

    list_image = [img for img in os.listdir("./excercise")
                  if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

    # Dùng CTkLabel để hiển thị ảnh
    image_exercise = ctk.CTkLabel(frame, text="")
    image_exercise.pack(padx=10, pady=10)

    current_image = {"filename": None}

    def change_image():
        if not list_image:
            image_exercise.configure(text="(Thư mục ./excercise trống)")
            return

        available = [img for img in list_image if img !=
                     current_image["filename"]] or list_image
        image_filename = random.choice(available)
        image_path = os.path.join("excercise", image_filename)

        try:
            # Dùng CTkImage
            ctk_img = ctk.CTkImage(Image.open(image_path), size=(700, 400))
            image_exercise.configure(image=ctk_img)
            current_image["filename"] = image_filename
        except Exception as e:
            image_exercise.configure(image=None, text=f"Lỗi mở ảnh: {e}")

    # Dùng CTkButton
    ctk.CTkButton(exercise_window, text="Đổi bài tập",
                  command=change_image).pack(pady=10)

    change_image()

# ---------------------------- TEE / gợi ý món (Giữ nguyên logic) ----------------------------
# Các class TEECalculator và MealSelector giữ nguyên 100%


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
            1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9
        }
        multiplier = activity_multipliers.get(self.activity_level, 1.2)
        return round(self.BMR * multiplier, 2)

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
    def __init__(self, TE, data_file="./database/data.csv"):
        self.TE = TE
        self.data_frame = pd.read_csv(
            data_file, delimiter=";", encoding="utf-8",
            header=None, names=["Ten mon an", "calo", "Trong luong"]
        )
        self.data_frame["Trong luong"] = (
            self.data_frame["Trong luong"].astype(str).str.replace(
                "g", "", regex=False).astype(float)
        )

    def select_food_items(self):
        selected_foods = []
        total = 0
        used = set()
        tries = 0
        while abs(total - self.TE) > 10 and tries < 5000:
            tries += 1
            idx = random.choice(self.data_frame.index)
            if idx in used:
                continue
            row = self.data_frame.loc[idx]
            cal = int(row["calo"]) if str(row["calo"]).isdigit() else 0
            if cal <= 0 or cal > self.TE or total + cal > self.TE:
                continue
            selected_foods.append(row)
            used.add(idx)
            total += cal
        return selected_foods

    def train_linear_regression(self):
        X = self.data_frame["calo"].to_numpy().reshape(-1, 1)
        y = self.data_frame["Trong luong"].to_numpy().reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, y)
        return model

    def save_results(self, selected_foods, model):
        with open("./database/result.txt", "w", encoding="utf-8") as f:
            for food in selected_foods:
                predicted_weight = model.predict(
                    np.array([[food["calo"]]])).flatten()[0]
                f.write(
                    f"{food['Ten mon an']};{round(food['calo'])};{round(food['Trong luong'], 2)};{round(predicted_weight, 2)}\n")
        with open("./database/result.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("./database/result_modified.txt", "w", encoding="utf-8") as f:
            for line in lines:
                parts = line.strip().split(";")
                f.write(" - ".join(parts[:-1]) + "\n")


def read_food_data():
    foods = []
    try:
        with open("./database/result_modified.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(" - ")
                if len(parts) == 3:
                    foods.append(parts)
    except FileNotFoundError:
        print("Không tìm thấy file result_modified.txt.")
    return foods

# ---------------------------- gợi ý món (Nâng cấp GUI) ----------------------------


def meal_suggestions():
    nutrition_window = ctk.CTkToplevel(root)
    nutrition_window.title("Gợi ý dinh dưỡng")
    nutrition_window.geometry("830x550")
    nutrition_window.resizable(False, False)
    nutrition_window.grab_set()

    # Chia cửa sổ thành 2 frame: Trái (nhập liệu) và Phải (kết quả)
    frame_left = ctk.CTkFrame(nutrition_window)
    frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

    frame_right = ctk.CTkFrame(nutrition_window)
    frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

    # --- Frame Trái (Nhập liệu) ---
    labels = ["Năm sinh", "Chiều cao (cm)", "Cân nặng (kg)", "Giới tính",
              "Mức độ vận động", "Mức độ luyện tập", "Thời gian luyện tập (giờ)"]
    entries = {}
    options = {
        "Giới tính": ["Nam", "Nữ"],
        "Mức độ vận động": ["Thụ động", "Nhẹ", "Trung bình", "Năng động", "Rất tích cực"],
        "Mức độ luyện tập": ["Không luyện tập", "Nhẹ", "Trung bình", "Nặng"]
    }

    for i, text in enumerate(labels):
        label = ctk.CTkLabel(frame_left, text=text)
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        var = ctk.StringVar()
        if text in options:
            cb = ctk.CTkComboBox(frame_left, variable=var,
                                 values=options[text], width=200, state="readonly")
            cb.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            cb.set(options[text][0])
        else:
            ent = ctk.CTkEntry(frame_left, textvariable=var, width=200)
            ent.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entries[text] = var

    # --- Frame Phải (Kết quả và Treeview) ---
    label_calo_mat_di = ctk.CTkLabel(
        frame_right, text="Calo bị mất đi sau khi luyện tập: ")
    label_BMR = ctk.CTkLabel(frame_right, text="Chỉ số BMR: ")
    label_BMI = ctk.CTkLabel(frame_right, text="Chỉ số BMI: ")
    label_tinh_trang = ctk.CTkLabel(frame_right, text="Tình trạng: ")
    progressbar = ctk.CTkProgressBar(frame_right)
    progressbar.set(0)  # Khởi tạo giá trị
    label_TEE = ctk.CTkLabel(
        frame_right, text="Nhu cầu năng lượng cho hoạt động (TEE): ")
    label_TE = ctk.CTkLabel(
        frame_right, text="Tổng calo cần thiết cho 1 ngày (TE): ")

    label_calo_mat_di.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    label_BMR.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    label_BMI.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    label_tinh_trang.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    progressbar.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
    label_TEE.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    label_TE.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    # Treeview (dùng ttk vì CTk không có Treeview, nhưng style nó cho hợp)
    from tkinter import ttk
    style = ttk.Style()
    style.theme_use("default")
    # Style cho Treeview
    style.configure("Treeview",
                    background="#DCDCDC",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#DCDCDC")
    style.map('Treeview', background=[('selected', '#347083')])

    tree_frame = ctk.CTkFrame(frame_right)
    tree_frame.grid(row=7, column=0, pady=10, padx=10, sticky="nsew")
    frame_right.grid_rowconfigure(7, weight=1)
    frame_right.grid_columnconfigure(0, weight=1)

    tree = ttk.Treeview(tree_frame, columns=("Tên món ăn", "Calo", "Trọng lượng"),
                        show="headings", selectmode="browse")
    tree.heading("Tên món ăn", text="Tên món ăn", anchor="center")
    tree.heading("Calo", text="Calo", anchor="center")
    tree.heading("Trọng lượng", text="Trọng lượng", anchor="center")
    tree.column("Tên món ăn", width=200, anchor="w")
    tree.column("Calo", width=80, anchor="center")
    tree.column("Trọng lượng", width=100, anchor="center")

    scrollbar = ctk.CTkScrollbar(tree_frame, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def update_treeview():
        for i in tree.get_children():
            tree.delete(i)
        for food in read_food_data():
            tree.insert("", "end", values=food)

    def filter_and_suggest():
        try:
            birth_year = int(entries["Năm sinh"].get())
            height = float(entries["Chiều cao (cm)"].get())
            weight = float(entries["Cân nặng (kg)"].get())
            gender = entries["Giới tính"].get()
            activity_level = ["Thụ động", "Nhẹ", "Trung bình", "Năng động", "Rất tích cực"].index(
                entries["Mức độ vận động"].get()
            ) + 1
            exercise_type = entries["Mức độ luyện tập"].get()
            exercise_hours = float(entries["Thời gian luyện tập (giờ)"].get())
        except Exception:
            messagebox.showwarning(
                "Chú ý", "Vui lòng nhập đúng định dạng dữ liệu.")
            return

        now_year = datetime.datetime.now().year
        age = now_year - birth_year
        BMI = weight / ((height / 100) ** 2)

        if gender == "Nữ":
            BMR = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
        else:
            BMR = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
        BMR = round(BMR, 1)

        calculator = TEECalculator(
            BMR, BMI, activity_level, exercise_type, exercise_hours)

        label_calo_mat_di.configure(
            text=f"Calo bị mất đi sau khi luyện tập: {calculator.exercise_addition}")
        label_BMR.configure(text=f"Chỉ số BMR: {BMR}")
        label_BMI.configure(text=f"Chỉ số BMI: {round(BMI, 1)}")

        # Cập nhật progress bar và màu
        progress_val = (BMI - 15) / (30 - 15)  # Giả sử thang từ 15-30
        progress_val = max(0, min(1, progress_val))  # Kẹp giá trị

        if BMI < 18.5:
            label_tinh_trang.configure(
                text="Tình trạng: Thiếu cân", text_color="blue")
            progressbar.configure(progress_color="blue")
        elif 18.5 <= BMI <= 24.9:
            label_tinh_trang.configure(
                text="Tình trạng: Bình thường", text_color="green")
            progressbar.configure(progress_color="green")
        elif 25 <= BMI <= 29.9:
            label_tinh_trang.configure(
                text="Tình trạng: Thừa cân", text_color="orange")
            progressbar.configure(progress_color="orange")
        else:
            label_tinh_trang.configure(
                text="Tình trạng: Béo phì", text_color="red")
            progressbar.configure(progress_color="red")

        progressbar.set(progress_val)

        label_TEE.configure(
            text=f"Nhu cầu năng lượng cho hoạt động (TEE): {calculator.TEE}")
        label_TE.configure(
            text=f"Tổng calo cần thiết cho 1 ngày (TE): {calculator.TE}")

        try:
            selector = MealSelector(calculator.TE)
            selected_foods = selector.select_food_items()
            model = selector.train_linear_regression()
            selector.save_results(selected_foods, model)
            update_treeview()
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy ./database/data.csv")

    # Nút bấm (đặt ở frame trái, bên dưới)
    ctk.CTkButton(frame_left, text="Tính và Gợi ý",
                  command=filter_and_suggest)\
        .grid(row=len(labels), column=0, columnspan=2, pady=20, padx=10, sticky="ew")

# ---------------------------- lịch sử mệt mỏi (Nâng cấp GUI) ----------------------------


def show_fatigue_history():
    try:
        with open("./database/fatigue_log.csv", "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file lịch sử")
        return

    history_window = ctk.CTkToplevel(root)
    history_window.title("Lịch Sử Mệt Mỏi")
    history_window.geometry("400x450")
    history_window.resizable(False, False)
    history_window.grab_set()

    frame = ctk.CTkFrame(history_window, fg_color="transparent")
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    # (Dùng lại style Treeview từ hàm meal_suggestions)
    tree = ttk.Treeview(frame, columns=("Thời Gian", "Trạng Thái"),
                        show="headings", selectmode="browse")
    tree.heading("Thời Gian", text="Thời Gian", anchor="center")
    tree.heading("Trạng Thái", text="Trạng Thái", anchor="center")
    tree.column("Thời Gian", width=150, anchor="center")
    tree.column("Trạng Thái", width=200, anchor="w")

    scrollbar = ctk.CTkScrollbar(frame, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for i, row in enumerate(data):
        # Bỏ tag màu vì style ttk đã xử lý
        tree.insert("", tk.END, values=row)

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning(
                "Chú ý", "Vui lòng chọn dòng cần xoá", parent=history_window)
            return
        index = tree.index(selected[0])
        tree.delete(selected[0])
        del data[index]
        with open("./database/fatigue_log.csv", "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)
        messagebox.showinfo(
            "Thành công", "Đã xoá dòng đã chọn", parent=history_window)

    def delete_all():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xoá toàn bộ lịch sử?", parent=history_window):
            tree.delete(*tree.get_children())
            with open("./database/fatigue_log.csv", "w", encoding="utf-8-sig", newline="") as file:
                pass
            messagebox.showinfo(
                "Thành công", "Đã xoá toàn bộ lịch sử", parent=history_window)

    button_frame = ctk.CTkFrame(history_window, fg_color="transparent")
    button_frame.pack(pady=10)

    ctk.CTkButton(button_frame, text="Xoá dòng đã chọn",
                  command=delete_selected).grid(row=0, column=0, padx=10)
    ctk.CTkButton(button_frame, text="Xoá toàn bộ lịch sử", command=delete_all,
                  fg_color="red", hover_color="#C00000").grid(row=0, column=1, padx=10)

# ---------------------------- giao diện chính (Nâng cấp GUI) ----------------------------


# Tạo cửa sổ chính
root = ctk.CTk()
root.title("FocusGuard")
root.geometry("750x500")  # Kích thước mới cho layout sidebar
root.resizable(False, False)

# --- (Mục 1) Tạo Sidebar bên trái ---
sidebar_frame = ctk.CTkFrame(root, width=180, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

# --- THÊM ẢNH NỀN VÀO SIDEBAR ---
# Đảm bảo file "background.jpg" nằm trong thư mục "images" nhé
bg_path = "./images/background.jpg"
if os.path.exists(bg_path):
    bg_img_data = Image.open(bg_path)
    # Cắt ảnh cho vừa (180x500)
    bg_img = ctk.CTkImage(bg_img_data, size=(180, 500))
    bg_label = ctk.CTkLabel(sidebar_frame, image=bg_img, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    print("Không tìm thấy file ./images/background.jpg")

# --- ĐẶT WIDGET BẰNG .PLACE() ---

# Logo/Icon
icon_path = "./images/icon.jpg"
if os.path.exists(icon_path):
    icon_img = ctk.CTkImage(Image.open(icon_path), size=(80, 80))
    # Thêm fg_color="transparent" để label không che mất nền
    icon_label = ctk.CTkLabel(
        sidebar_frame, image=icon_img, text="", fg_color="transparent")
    # y = 20 (pady) + 40 (nửa height)
    icon_label.place(relx=0.5, y=60, anchor="center")
else:
    logo_label = ctk.CTkLabel(sidebar_frame, text="FocusGuard", font=ctk.CTkFont(
        size=20, weight="bold"), fg_color="transparent")
    logo_label.place(relx=0.5, y=60, anchor="center")

# Các nút trên Sidebar (Giả sử các nút cao 40px)
# relwidth=0.8 tương đương với padx=20 trên frame rộng 180
btn_camera = ctk.CTkButton(sidebar_frame, text=" 📷  Bật Máy Ảnh",
                           command=turn_on_camera, fg_color="#D32F2F", hover_color="#B71C1C")
# y = 100 (icon_end) + 10 (pady) + 20 (nửa height)
btn_camera.place(relx=0.5, y=130, anchor="center", relwidth=0.8)

btn_exercise = ctk.CTkButton(sidebar_frame, text=" 🏋️  Bài Thể Dục",
                             command=select_exercise, fg_color="#F57C00", hover_color="#E65100")
# y = 150 (btn_end) + 10 (pady) + 20 (nửa height)
btn_exercise.place(relx=0.5, y=180, anchor="center", relwidth=0.8)

btn_meal = ctk.CTkButton(
    sidebar_frame, text=" 🥗  Gợi Ý Thực Đơn", command=meal_suggestions)
btn_meal.place(relx=0.5, y=230, anchor="center",
               relwidth=0.8)  # y = 200 + 10 + 20

btn_history = ctk.CTkButton(sidebar_frame, text=" 📜  Lịch Sử Mệt Mỏi",
                            command=show_fatigue_history, fg_color="#388E3C", hover_color="#1B5E20")
btn_history.place(relx=0.5, y=280, anchor="center",
                  relwidth=0.8)  # y = 250 + 10 + 20

# Nút Cài đặt (Giả sử label 20px, menu 30px)
theme_menu = ctk.CTkComboBox(sidebar_frame,  values=["Light", "Dark", "System"],
                             command=ctk.set_appearance_mode,
                             fg_color="#565B5E",  button_color="#565B5E",  button_hover_color="#4A4E51",
                             state="readonly",  justify="center")
theme_menu.set("Color Theme")  # Đặt chữ hiển thị ban đầu
theme_menu.place(relx=0.5,  y=330,  anchor="center",
                 relwidth=0.8)  # Đặt nó ở giữa

# --- (Mục 2) Tạo Khung chính bên phải ---
main_frame = ctk.CTkFrame(root, fg_color="transparent")
main_frame.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=20, pady=20)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(3, weight=1)

# Nút Cập nhật biểu đồ (dùng .pack() và thêm ipady)
btn_update_chart = ctk.CTkButton(main_frame, text="Cập nhật biểu đồ",
                                 command=update_fatigue_pie_chart, fg_color="#673AB7", hover_color="#512DA8")
btn_update_chart.pack(fill="x", padx=10, pady=(
    10, 5), ipady=10)  # Thêm ipady=10 để nút cao lên

# Frame chứa 2 ảnh (dùng .pack())
frame_plot = ctk.CTkFrame(main_frame)
frame_plot.pack(fill="y",  expand=True,  padx=0,  pady=(0, 5))

# Hiển thị biểu đồ rỗng ban đầu
show_empty_chart()

# (Không cần ảnh nền vì CustomTkinter tự quản lý nền)

root.mainloop()
