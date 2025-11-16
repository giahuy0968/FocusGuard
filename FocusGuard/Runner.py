<<<<<<< HEAD
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
=======
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
import sys
import numpy as np
import random
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import threading
import webbrowser
import json
from urllib import request, parse
import tempfile

# Import module tìm kiếm trạm dừng chân
try:
    from rest_stops_api import rest_stops_finder
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False
    print("Module rest_stops_api không khả dụng")
def show_notification(message):
    def create_window():
        try:
            root = tk.Tk()
            root.overrideredirect(True)
            root.attributes('-topmost', True)

            window_width = 350
            window_height = 120

            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)

            root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Modern gradient-like background
            root.configure(bg="#3498db")
            
            # Border frame
            border_frame = tk.Frame(root, bg="#2980b9", padx=2, pady=2)
            border_frame.pack(fill=tk.BOTH, expand=True)
            
            inner_frame = tk.Frame(border_frame, bg="#ecf0f1")
            inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            
            # Icon
            icon_label = tk.Label(inner_frame, text="🔔", font=("Segoe UI Emoji", 32), 
                                 bg="#ecf0f1", fg="#3498db")
            icon_label.pack(pady=(10, 5))

            # Message
            label = tk.Label(inner_frame, text=message, font=("Segoe UI", 11), 
                            bg="#ecf0f1", fg="#2c3e50", wraplength=320, justify="center")
            label.pack(expand=True, pady=(0, 10))

            # Fade out effect
            def fade_out(alpha=1.0):
                try:
                    if alpha > 0 and root.winfo_exists():
                        root.attributes('-alpha', alpha)
                        root.after(50, fade_out, alpha - 0.05)
                    else:
                        if root.winfo_exists():
                            root.quit()
                            root.destroy()
                except:
                    pass

            root.after(3000, fade_out)
            root.mainloop()
        except Exception as e:
            print(f"Notification error: {e}")

    threading.Thread(target=create_window, daemon=True).start()

def show_rest_stops_map():
    """Hiển thị bản đồ các trạm dừng chân, quán cà phê, nhà hàng gần nhất"""
    try:
        map_window = Toplevel(root)
        map_window.title("🗺️ Bản Đồ Trạm Dừng Chân")
        window_width = 900
        window_height = 700

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        map_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Header
        header_frame = ttk.Frame(map_window)
        header_frame.pack(fill=X, pady=(15, 10), padx=20)
        
        title_label = ttk.Label(header_frame, text="🗺️ BẢN ĐỒ TRẠM DỪNG CHÂN", 
                               font=("Segoe UI", 18, "bold"), foreground="#c0392b")
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Tìm kiếm điểm nghỉ ngơi gần vị trí của bạn", 
                                  font=("Segoe UI", 10), foreground="#7f8c8d")
        subtitle_label.pack()

        # Location input section
        input_frame = ttk.Labelframe(map_window, text="📍 Nhập Vị Trí Của Bạn", padding=15)
        input_frame.pack(fill=X, padx=20, pady=(10, 10))

        location_label = ttk.Label(input_frame, text="Địa chỉ hoặc Tọa độ:", font=("Segoe UI", 10))
        location_label.grid(row=0, column=0, padx=10, pady=8, sticky="w")

        location_var = StringVar(value="Hà Nội, Việt Nam")
        location_entry = ttk.Entry(input_frame, textvariable=location_var, width=40, font=("Segoe UI", 10))
        location_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

        search_radius_label = ttk.Label(input_frame, text="Bán kính tìm kiếm (km):", font=("Segoe UI", 10))
        search_radius_label.grid(row=1, column=0, padx=10, pady=8, sticky="w")

        radius_var = StringVar(value="5")
        radius_combo = ttk.Combobox(input_frame, textvariable=radius_var, 
                                    values=["1", "2", "5", "10", "20"], width=37, state="readonly")
        radius_combo.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        facility_label = ttk.Label(input_frame, text="Loại cơ sở:", font=("Segoe UI", 10))
        facility_label.grid(row=2, column=0, padx=10, pady=8, sticky="w")

        facility_var = StringVar(value="Tất cả")
        facility_combo = ttk.Combobox(input_frame, textvariable=facility_var,
                                      values=["Tất cả", "Trạm xăng", "Quán cà phê", "Nhà hàng", "Khách sạn"],
                                      width=37, state="readonly")
        facility_combo.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        input_frame.columnconfigure(1, weight=1)

        # Results section
        results_frame = ttk.Labelframe(map_window, text="📋 Danh Sách Điểm Dừng Chân", padding=10)
        results_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

        # Treeview for results
        tree = ttk.Treeview(results_frame, columns=("Tên", "Loại", "Địa chỉ", "Khoảng cách"), 
                           show="headings", height=15)
        tree.heading("Tên", text="🏪 Tên Địa Điểm", anchor="w")
        tree.heading("Loại", text="📌 Loại", anchor="center")
        tree.heading("Địa chỉ", text="📍 Địa Chỉ", anchor="w")
        tree.heading("Khoảng cách", text="📏 Khoảng Cách", anchor="center")
        
        tree.column("Tên", width=200, anchor="w")
        tree.column("Loại", width=100, anchor="center")
        tree.column("Địa chỉ", width=300, anchor="w")
        tree.column("Khoảng cách", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill=BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

        status_label = ttk.Label(results_frame, text="Nhấn 'Tìm Kiếm' để xem các điểm dừng chân gần bạn", 
                                font=("Segoe UI", 10), foreground="#7f8c8d")
        status_label.pack(pady=5)

        def search_places():
            """Tìm kiếm các địa điểm gần vị trí"""
            location = location_var.get().strip()
            radius = radius_var.get()
            facility = facility_var.get()
            
            if not location:
                messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập địa chỉ!", parent=map_window)
                return

            # Clear previous results
            for item in tree.get_children():
                tree.delete(item)
            
            status_label.config(text="🔍 Đang tìm kiếm...", foreground="#3498db")
            map_window.update()

            try:
                filtered_places = []
                
                if API_AVAILABLE:
                    # Try to use real API
                    status_label.config(text="🌐 Đang kết nối với OpenStreetMap...", foreground="#3498db")
                    map_window.update()
                    
                    # Geocode address
                    lat, lon = rest_stops_finder.geocode_address(location)
                    
                    if lat and lon:
                        # Search for places
                        places_data = rest_stops_finder.find_rest_stops(
                            lat, lon, int(radius), facility
                        )
                        
                        if places_data:
                            filtered_places = [
                                (p['name'], p['type'], p['address'], p['distance'])
                                for p in places_data
                            ]
                        else:
                            # Fallback to sample data
                            status_label.config(text="⚠️ Không tìm thấy, hiển thị dữ liệu mẫu", foreground="#f39c12")
                            sample_data = rest_stops_finder.get_sample_data(location)
                            filtered_places = [
                                (p['name'], p['type'], p['address'], p['distance'])
                                for p in sample_data
                                if facility == "Tất cả" or p['type'] == facility
                            ]
                    else:
                        # Geocoding failed, use sample data
                        status_label.config(text="⚠️ Không thể xác định vị trí, hiển thị dữ liệu mẫu", foreground="#f39c12")
                        sample_data = rest_stops_finder.get_sample_data(location)
                        filtered_places = [
                            (p['name'], p['type'], p['address'], p['distance'])
                            for p in sample_data
                            if facility == "Tất cả" or p['type'] == facility
                        ]
                else:
                    # Use sample data when API not available
                    sample_places = [
                        ("Trạm xăng Petrolimex", "Trạm xăng", "123 Đường ABC, Hà Nội", "1.2 km"),
                        ("Highlands Coffee", "Quán cà phê", "456 Đường DEF, Hà Nội", "2.5 km"),
                        ("Nhà hàng Phở Gia Truyền", "Nhà hàng", "789 Đường GHI, Hà Nội", "3.0 km"),
                        ("Trạm xăng Shell", "Trạm xăng", "321 Đường JKL, Hà Nội", "3.5 km"),
                        ("Cà phê Trung Nguyên", "Quán cà phê", "654 Đường MNO, Hà Nội", "4.2 km"),
                        ("KFC", "Nhà hàng", "987 Đường PQR, Hà Nội", "4.8 km"),
                        ("Trạm dừng chân cao tốc", "Trạm xăng", "147 Cao tốc Hà Nội - Hải Phòng", "6.5 km"),
                        ("Khách sạn Mường Thanh", "Khách sạn", "258 Đường STU, Hà Nội", "7.2 km"),
                        ("Starbucks", "Quán cà phê", "369 Đường VWX, Hà Nội", "8.0 km"),
                        ("Nhà hàng Buffet Poseidon", "Nhà hàng", "741 Đường YZ, Hà Nội", "9.5 km"),
                    ]

                    # Filter by facility type
                    for place in sample_places:
                        if facility == "Tất cả" or place[1] == facility:
                            # Check if within radius
                            distance = float(place[3].replace(" km", ""))
                            if distance <= float(radius):
                                filtered_places.append(place)

                # Display results
                if filtered_places:
                    for idx, place in enumerate(filtered_places):
                        tag = "evenrow" if idx % 2 == 0 else "oddrow"
                        tree.insert("", "end", values=place, tags=(tag,))
                    
                    tree.tag_configure("evenrow", background="#ecf0f1")
                    tree.tag_configure("oddrow", background="#ffffff")
                    
                    status_label.config(text=f"✅ Tìm thấy {len(filtered_places)} địa điểm", foreground="#27ae60")
                else:
                    status_label.config(text="❌ Không tìm thấy địa điểm nào phù hợp", foreground="#e74c3c")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}", parent=map_window)
                status_label.config(text="❌ Lỗi khi tìm kiếm", foreground="#e74c3c")

        def open_in_google_maps():
            """Mở bản đồ Google Maps"""
            location = location_var.get().strip()
            if location:
                # Encode location for URL
                encoded_location = parse.quote(location)
                url = f"https://www.google.com/maps/search/rest+stops+near+{encoded_location}"
                webbrowser.open(url)
            else:
                messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập địa chỉ!", parent=map_window)

        def get_directions():
            """Lấy chỉ dẫn đến địa điểm được chọn"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("⚠️ Chú ý", "Vui lòng chọn một địa điểm!", parent=map_window)
                return
            
            item = tree.item(selected[0])
            place_name = item['values'][0]
            place_address = item['values'][2]
            
            # Open Google Maps directions
            origin = parse.quote(location_var.get().strip())
            destination = parse.quote(f"{place_name}, {place_address}")
            url = f"https://www.google.com/maps/dir/{origin}/{destination}"
            webbrowser.open(url)

        # Button frame
        button_frame = ttk.Frame(map_window)
        button_frame.pack(pady=15)

        search_btn = ttk.Button(button_frame, text="🔍 TÌM KIẾM", 
                               command=search_places, bootstyle="primary",
                               width=18)
        search_btn.grid(row=0, column=0, padx=5, ipadx=10, ipady=10)

        map_btn = ttk.Button(button_frame, text="🗺️ MỞ GOOGLE MAPS", 
                            command=open_in_google_maps, bootstyle="info-outline",
                            width=20)
        map_btn.grid(row=0, column=1, padx=5, ipadx=10, ipady=10)

        direction_btn = ttk.Button(button_frame, text="🧭 CHỈ ĐƯỜNG", 
                                  command=get_directions, bootstyle="success-outline",
                                  width=18)
        direction_btn.grid(row=0, column=2, padx=5, ipadx=10, ipady=10)

        close_btn = ttk.Button(button_frame, text="✖️ ĐÓNG", 
                              command=map_window.destroy, bootstyle="danger-outline",
                              width=12)
        close_btn.grid(row=0, column=3, padx=5, ipadx=10, ipady=10)

        # Auto search on open
        map_window.after(500, search_places)
    
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mở bản đồ trạm dừng chân:\n{str(e)}")
        print(f"Lỗi show_rest_stops_map: {e}")
        import traceback
        traceback.print_exc()


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
    try:
        show_notification("Thông báo\nĐang khởi động camera...")
        # Chạy file nhận diện với cửa sổ terminal hiện lên
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PhatHienMetMoi.py")
        subprocess.Popen([sys.executable, script_path], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
        print("✓ Camera đã được khởi động")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file PhatHienMetMoi.py!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể khởi động camera:\n{str(e)}")

def select_exercise():
    exercise_window = Toplevel(root)
    exercise_window.title("🏋️ Bài Tập Thể Dục")
    window_width = 750
    window_height = 550

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    exercise_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    exercise_window.resizable(False, False)

    # Header
    header_frame = ttk.Frame(exercise_window)
    header_frame.pack(fill=X, pady=(15, 10), padx=20)
    
    title_label = ttk.Label(header_frame, text="🏋️ BÀI TẬP THỂ DỤC", 
                           font=("Segoe UI", 18, "bold"), foreground="#27ae60")
    title_label.pack()
    
    subtitle_label = ttk.Label(header_frame, text="Luyện tập giữa giờ để giảm mệt mỏi", 
                              font=("Segoe UI", 10), foreground="#7f8c8d")
    subtitle_label.pack()

    # Image frame with border
    image_container = ttk.Frame(exercise_window, relief="solid", borderwidth=2)
    image_container.pack(pady=15, padx=20)
    
    image_exercise = ttk.Label(image_container)
    image_exercise.pack(padx=3, pady=3)

    list_image = os.listdir("./excercise")
    list_image = [img for img in list_image if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

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

    # Button frame
    button_frame = ttk.Frame(exercise_window)
    button_frame.pack(pady=15)

    change_button = ttk.Button(button_frame, text="🔄 ĐỔI BÀI TẬP KHÁC", 
                              command=change_image, bootstyle="success-outline",
                              width=25)
    change_button.grid(row=0, column=0, padx=5, ipadx=10, ipady=8)
    
    close_button = ttk.Button(button_frame, text="✖️ ĐÓNG", 
                             command=exercise_window.destroy, bootstyle="danger-outline",
                             width=15)
    close_button.grid(row=0, column=1, padx=5, ipadx=10, ipady=8)

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
    nutrition_window.title("🥗 Gợi Ý Dinh Dưỡng")
    nutrition_window.resizable(True, True)
    window_width = 900
    window_height = 750  # Tăng chiều cao từ 650 lên 750

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    nutrition_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Header
    header_frame = ttk.Frame(nutrition_window)
    header_frame.grid(row=0, column=0, columnspan=3, pady=(15, 10), padx=20, sticky="ew")
    
    title_label = ttk.Label(header_frame, text="🥗 GỢI Ý DINH DƯỠNG", 
                           font=("Segoe UI", 18, "bold"), foreground="#e67e22")
    title_label.pack()
    
    subtitle_label = ttk.Label(header_frame, text="Tính toán nhu cầu dinh dưỡng và gợi ý thực đơn phù hợp", 
                              font=("Segoe UI", 10), foreground="#7f8c8d")
    subtitle_label.pack()

    # Input section
    input_frame = ttk.Labelframe(nutrition_window, text="📝 Thông Tin Cá Nhân", padding=15)
    input_frame.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")

    labels = ["Năm sinh", "Chiều cao (cm)", "Cân nặng (kg)", "Giới tính", 
              "Mức độ vận động", "Mức độ luyện tập", "Thời gian luyện tập (giờ)"]
    entries = {}

    options = {
        "Giới tính": ["Nam", "Nữ"],
        "Mức độ vận động": ["Thụ động", "Nhẹ", "Trung bình", "Năng động", "Rất tích cực"],
        "Mức độ luyện tập": ["Không luyện tập", "Nhẹ", "Trung bình", "Nặng"]
    }

    for i, label_text in enumerate(labels):
        label = ttk.Label(input_frame, text=label_text + ":", font=("Segoe UI", 10))
        label.grid(row=i, column=0, padx=10, pady=8, sticky="w")

        var = StringVar()
        if label_text in options:
            combo = ttk.Combobox(input_frame, textvariable=var, values=options[label_text], 
                               width=28, state="readonly", font=("Segoe UI", 10))
            combo.grid(row=i, column=1, padx=10, pady=8, sticky="w")
            combo.set(options[label_text][0])
        else:
            entry = ttk.Entry(input_frame, textvariable=var, width=30, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="w")
        
        entries[label_text] = var

    # Results section
    results_frame = ttk.Labelframe(nutrition_window, text="📊 Kết Quả Phân Tích", padding=15)
    results_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    
    result_labels = {
        "calo_mat_di": ttk.Label(results_frame, text="⚡ Calo tiêu hao: --", 
                                font=("Segoe UI", 10), foreground="#e74c3c"),
        "BMR": ttk.Label(results_frame, text="💪 Chỉ số BMR: --", 
                        font=("Segoe UI", 10), foreground="#3498db"),
        "BMI": ttk.Label(results_frame, text="📏 Chỉ số BMI: --", 
                        font=("Segoe UI", 10), foreground="#9b59b6"),
        "tinh_trang": ttk.Label(results_frame, text="🏥 Tình trạng: --", 
                               font=("Segoe UI", 10, "bold"), foreground="#2ecc71"),
        "TEE": ttk.Label(results_frame, text="🔥 TEE: --", 
                        font=("Segoe UI", 10), foreground="#f39c12"),
        "TE": ttk.Label(results_frame, text="🍽️ Calo cần/ngày: --", 
                       font=("Segoe UI", 10, "bold"), foreground="#16a085")
    }
    
    for idx, (key, label) in enumerate(result_labels.items()):
        label.grid(row=idx, column=0, padx=10, pady=8, sticky="w")
    
    progressbar = ttk.Progressbar(results_frame, length=250, mode='determinate')
    progressbar.grid(row=len(result_labels), column=0, padx=10, pady=15, sticky="ew")

    # Calculate button
    calculate_frame = ttk.Frame(nutrition_window)
    calculate_frame.grid(row=2, column=0, columnspan=2, pady=10)
    
    filter_button = ttk.Button(calculate_frame, text="🧮 TÍNH TOÁN & GỢI Ý", 
                              bootstyle="success", width=30)
    filter_button.pack(ipadx=15, ipady=10)

    # Food suggestions section
    food_frame = ttk.Labelframe(nutrition_window, text="🍱 Gợi Ý Thực Đơn", padding=10)
    food_frame.grid(row=3, column=0, columnspan=2, pady=(10, 20), padx=20, sticky="nsew")

    tree = ttk.Treeview(food_frame, columns=("Tên món ăn", "Calo", "Trọng lượng"), 
                       show="headings", height=8)
    tree.heading("Tên món ăn", text="🍜 Tên Món Ăn", anchor="center")
    tree.heading("Calo", text="🔥 Calo", anchor="center")
    tree.heading("Trọng lượng", text="⚖️ Trọng Lượng", anchor="center")
    tree.column("Tên món ăn", width=350, anchor="w")
    tree.column("Calo", width=120, anchor="center")
    tree.column("Trọng lượng", width=150, anchor="center")

    scrollbar = ttk.Scrollbar(food_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill=BOTH)

    # Configure grid weights
    nutrition_window.columnconfigure(0, weight=1)
    nutrition_window.columnconfigure(1, weight=1)
    nutrition_window.rowconfigure(1, weight=1)
    nutrition_window.rowconfigure(3, weight=1)

    def filter_and_suggest():
        try:
            # Check for empty fields first
            if not entries["Năm sinh"].get().strip():
                messagebox.showerror("Lỗi", "Vui lòng nhập Năm sinh!", 
                                   parent=nutrition_window)
                return
            
            if not entries["Chiều cao (cm)"].get().strip():
                messagebox.showerror("Lỗi", "Vui lòng nhập Chiều cao!", 
                                   parent=nutrition_window)
                return
            
            if not entries["Cân nặng (kg)"].get().strip():
                messagebox.showerror("Lỗi", "Vui lòng nhập Cân nặng!", 
                                   parent=nutrition_window)
                return
            
            if not entries["Thời gian luyện tập (giờ)"].get().strip():
                messagebox.showerror("Lỗi", "Vui lòng nhập Thời gian luyện tập!\nVí dụ: 0 (nếu không luyện tập), 1, 1.5, 2", 
                                   parent=nutrition_window)
                return
            
            # Validate and convert inputs with specific error messages
            try:
                age = int(entries["Năm sinh"].get())
                if age < 1900 or age > 2025:
                    messagebox.showerror("Lỗi", "Năm sinh không hợp lệ!\nVui lòng nhập năm từ 1900 đến 2025", 
                                       parent=nutrition_window)
                    return
            except ValueError:
                messagebox.showerror("Lỗi", "Năm sinh phải là số nguyên!\nVí dụ: 1990, 2000, 2005", 
                                   parent=nutrition_window)
                return
            
            try:
                height = float(entries["Chiều cao (cm)"].get())
                if height <= 0 or height > 300:
                    messagebox.showerror("Lỗi", "Chiều cao không hợp lệ!\nVui lòng nhập chiều cao từ 1-300 cm", 
                                       parent=nutrition_window)
                    return
            except ValueError:
                messagebox.showerror("Lỗi", "Chiều cao phải là số!\nVí dụ: 170 hoặc 170.5", 
                                   parent=nutrition_window)
                return
            
            try:
                weight = float(entries["Cân nặng (kg)"].get())
                if weight <= 0 or weight > 500:
                    messagebox.showerror("Lỗi", "Cân nặng không hợp lệ!\nVui lòng nhập cân nặng từ 1-500 kg", 
                                       parent=nutrition_window)
                    return
            except ValueError:
                messagebox.showerror("Lỗi", "Cân nặng phải là số!\nVí dụ: 65 hoặc 65.5", 
                                   parent=nutrition_window)
                return
            
            try:
                exercise_hours = float(entries["Thời gian luyện tập (giờ)"].get())
                if exercise_hours < 0 or exercise_hours > 24:
                    messagebox.showerror("Lỗi", "Thời gian luyện tập không hợp lệ!\nVui lòng nhập từ 0-24 giờ", 
                                       parent=nutrition_window)
                    return
            except ValueError:
                messagebox.showerror("Lỗi", "Thời gian luyện tập phải là số!\nVí dụ: 0, 1, 1.5, 2", 
                                   parent=nutrition_window)
                return
            
            gender = entries["Giới tính"].get()
            activity_level = ["Thụ động", "Nhẹ", "Trung bình", "Năng động", "Rất tích cực"].index(entries["Mức độ vận động"].get()) + 1
            exercise_type = entries["Mức độ luyện tập"].get()
            
            now_year = datetime.datetime.now().year
            age = now_year - age
            BMI = weight / ((height / 100) ** 2)
            
            if gender == "Nữ":
                BMR = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
            else:
                BMR = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
            
            BMR = round(BMR, 1)

            calculator = TEECalculator(BMR, BMI, activity_level, exercise_type, exercise_hours)
            
            result_labels["calo_mat_di"].config(text=f"⚡ Calo tiêu hao: {calculator.exercise_addition} kcal")
            result_labels["BMR"].config(text=f"💪 Chỉ số BMR: {round(BMR, 2)}")
            result_labels["BMI"].config(text=f"📏 Chỉ số BMI: {round(BMI, 1)}")
            
            if BMI < 18.5:
                result_labels["tinh_trang"].config(text="🏥 Tình trạng: Thiếu cân", foreground="#3498db")
                progressbar.config(bootstyle="info")
            elif BMI >= 18.5 and BMI <= 24.9:
                result_labels["tinh_trang"].config(text="🏥 Tình trạng: Bình Thường", foreground="#2ecc71")
                progressbar.config(bootstyle="success")
            elif BMI >= 25 and BMI <= 29.9:
                result_labels["tinh_trang"].config(text="🏥 Tình trạng: Thừa cân", foreground="#f39c12")
                progressbar.config(bootstyle="warning")
            else:
                result_labels["tinh_trang"].config(text="🏥 Tình trạng: Béo phì", foreground="#e74c3c")
                progressbar.config(bootstyle="danger")
            
            progressbar["value"] = 100
            progressbar.update_idletasks()
            
            result_labels["TEE"].config(text=f"🔥 TEE: {calculator.TEE} kcal")
            result_labels["TE"].config(text=f"🍽️ Calo cần/ngày: {calculator.TE} kcal")
            
            selector = MealSelector(calculator.TE)
            selected_foods = selector.select_food_items()
            model = selector.train_linear_regression()
            selector.save_results(selected_foods, model)

            update_treeview()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Vui lòng kiểm tra lại thông tin nhập vào!\n{str(e)}", 
                               parent=nutrition_window)

    def update_treeview():
        food_data = read_food_data()
        for i in tree.get_children():
            tree.delete(i)
        for idx, food in enumerate(food_data):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            tree.insert("", "end", values=food, tags=(tag,))
        tree.tag_configure("evenrow", background="#ecf0f1")
        tree.tag_configure("oddrow", background="#ffffff")

    filter_button.config(command=filter_and_suggest)

def show_fatigue_history():
    try:
        with open("./database/fatigue_log.csv", "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file lịch sử")
        return

    history_window = Toplevel(root)
    history_window.title("📜 Lịch Sử Mệt Mỏi")
    window_width = 550
    window_height = 550

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    history_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Header
    header_frame = ttk.Frame(history_window)
    header_frame.pack(fill=X, pady=(15, 10), padx=20)
    
    title_label = ttk.Label(header_frame, text="📜 LỊCH SỬ MỆT MỎI", 
                           font=("Segoe UI", 18, "bold"), foreground="#e67e22")
    title_label.pack()
    
    subtitle_label = ttk.Label(header_frame, text=f"Tổng số bản ghi: {len(data)}", 
                              font=("Segoe UI", 10), foreground="#7f8c8d")
    subtitle_label.pack()

    # Main frame
    main_frame = ttk.Labelframe(history_window, text="📊 Dữ Liệu Theo Dõi", padding=15)
    main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=(0, 10))

    # Treeview with custom style
    tree = ttk.Treeview(main_frame, columns=("Thời Gian", "Trạng Thái"), 
                       show="headings", selectmode="browse", height=15)
    tree.heading("Thời Gian", text="🕐 Thời Gian", anchor="center")
    tree.heading("Trạng Thái", text="📋 Trạng Thái", anchor="center")
    tree.column("Thời Gian", width=180, anchor="center")
    tree.column("Trạng Thái", width=300, anchor="center")

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add data with alternating colors
    for i, row in enumerate(data):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", tk.END, values=row, tags=(tag,))
    
    tree.tag_configure("evenrow", background="#ecf0f1", foreground="#2c3e50")
    tree.tag_configure("oddrow", background="#ffffff", foreground="#34495e")

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Chú ý", "Vui lòng chọn dòng cần xoá!", 
                                  parent=history_window)
            return
        
        if messagebox.askyesno("🗑️ Xác nhận", "Bạn có chắc chắn muốn xoá dòng này?", 
                              parent=history_window):
            index = tree.index(selected[0])
            tree.delete(selected[0])
            del data[index]
            with open("./database/fatigue_log.csv", "w", encoding="utf-8-sig", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(data)
            subtitle_label.config(text=f"Tổng số bản ghi: {len(data)}")
            messagebox.showinfo("✅ Thành công", "Đã xoá dòng đã chọn!", 
                              parent=history_window)

    def delete_all():
        if not data:
            messagebox.showinfo("ℹ️ Thông báo", "Không có dữ liệu để xoá!", 
                              parent=history_window)
            return
            
        if messagebox.askyesno("⚠️ Cảnh báo", 
                              "Bạn có chắc chắn muốn xoá TOÀN BỘ lịch sử?\nHành động này không thể hoàn tác!", 
                              parent=history_window):
            tree.delete(*tree.get_children())
            data.clear()
            with open("./database/fatigue_log.csv", "w", encoding="utf-8-sig", newline="") as file:
                pass  
            subtitle_label.config(text=f"Tổng số bản ghi: 0")
            messagebox.showinfo("✅ Thành công", "Đã xoá toàn bộ lịch sử!", 
                              parent=history_window)

    # Button frame
    button_frame = ttk.Frame(history_window)
    button_frame.pack(pady=15)

    delete_btn = ttk.Button(button_frame, text="🗑️ XOÁ DÒNG ĐÃ CHỌN", 
                           command=delete_selected, bootstyle="warning-outline",
                           width=22)
    delete_btn.grid(row=0, column=0, padx=8, ipadx=10, ipady=8)

    clear_btn = ttk.Button(button_frame, text="🗑️ XOÁ TOÀN BỘ", 
                          command=delete_all, bootstyle="danger-outline",
                          width=18)
    clear_btn.grid(row=0, column=1, padx=8, ipadx=10, ipady=8)
    
    close_btn = ttk.Button(button_frame, text="✖️ ĐÓNG", 
                          command=history_window.destroy, bootstyle="secondary-outline",
                          width=12)
    close_btn.grid(row=0, column=2, padx=8, ipadx=10, ipady=8)

root = tb.Window(themename="cosmo")

window_width = 600
window_height = 750

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)

# Style configuration
style = tb.Style()
style.configure("TButton", font=("Segoe UI", 11, "bold"), borderwidth=0)
style.configure("Custom.TFrame", background="#f8f9fa")
style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), foreground="#2c3e50")
style.configure("Subtitle.TLabel", font=("Segoe UI", 11), foreground="#7f8c8d")

# Main container with gradient-like effect
main_container = tb.Frame(root, bootstyle="light")
main_container.pack(fill=BOTH, expand=True)

# Header Section with improved design
header_frame = tb.Frame(main_container, bootstyle="light")
header_frame.pack(pady=20, padx=30, fill=X)

# Icon with border
try:
    icon_path = "./images/icon.jpg"
    icon = Image.open(icon_path)
    resized_icon = icon.resize((100, 100), Image.LANCZOS)
    icon = ImageTk.PhotoImage(resized_icon)
    icon_label = tb.Label(header_frame, image=icon, bootstyle="light")
    icon_label.image = icon
    icon_label.pack()
except:
    pass

# Title and subtitle
title_label = tb.Label(header_frame, text="FocusGuard", style="Title.TLabel", bootstyle="light")
title_label.pack(pady=(10, 5))

subtitle_label = tb.Label(header_frame, text="Chăm sóc sức khỏe của bạn mỗi ngày", 
                         style="Subtitle.TLabel", bootstyle="light")
subtitle_label.pack()

# Separator line
separator = ttk.Separator(main_container, orient='horizontal')
separator.pack(fill=X, padx=30, pady=15)

# Main content area
content_frame = tb.Frame(main_container, bootstyle="light")
content_frame.pack(pady=10, padx=30, fill=BOTH, expand=True)

# Camera Section - Featured button
camera_section = tb.Labelframe(content_frame, text="🎥 Giám Sát Thời Gian Thực", 
                                bootstyle="primary", padding=15)
camera_section.pack(fill=X, pady=(0, 15))

camera_btn = tb.Button(camera_section, text="📷 BẬT MÁY ẢNH NHẬN DIỆN", 
                       bootstyle="primary-outline", command=turn_on_camera)
camera_btn.pack(ipadx=20, ipady=15, fill=X)

# Features Section - Grid layout
features_section = tb.Labelframe(content_frame, text="⚡ Các Tính Năng Chính", 
                                  bootstyle="info", padding=15)
features_section.pack(fill=X, pady=(0, 15))

features_inner = tb.Frame(features_section, bootstyle="light")
features_inner.pack(fill=X)

exercise_btn = tb.Button(features_inner, text="🏋️\nBài Tập\nThể Dục", 
                        bootstyle="success-outline", command=select_exercise)
exercise_btn.grid(row=0, column=0, padx=5, pady=5, ipadx=15, ipady=15, sticky="ew")

meal_btn = tb.Button(features_inner, text="🥗\nGợi Ý\nThực Đơn", 
                    bootstyle="info-outline", command=meal_suggestions)
meal_btn.grid(row=0, column=1, padx=5, pady=5, ipadx=15, ipady=15, sticky="ew")

map_btn = tb.Button(features_inner, text="🗺️\nTrạm Dừng\nChân", 
                   bootstyle="danger-outline", command=show_rest_stops_map)
map_btn.grid(row=0, column=2, padx=5, pady=5, ipadx=15, ipady=15, sticky="ew")

features_inner.columnconfigure(0, weight=1)
features_inner.columnconfigure(1, weight=1)
features_inner.columnconfigure(2, weight=1)

# History Section
history_section = tb.Labelframe(content_frame, text="📊 Lịch Sử & Thống Kê", 
                                 bootstyle="warning", padding=15)
history_section.pack(fill=X, pady=(0, 15))

history_btn = tb.Button(history_section, text="📜 XEM LỊCH SỬ MỆT MỎI", 
                       bootstyle="warning-outline", command=show_fatigue_history)
history_btn.pack(ipadx=20, ipady=12, fill=X, pady=(0, 8))

update_button = tb.Button(history_section, text="📈 CẬP NHẬT BIỂU ĐỒ PHÂN TÍCH", 
                         bootstyle="secondary-outline", command=update_fatigue_pie_chart)
update_button.pack(ipadx=20, ipady=12, fill=X)

# Chart Section
chart_section = tb.Labelframe(content_frame, text="📉 Biểu Đồ Trực Quan", 
                               bootstyle="secondary", padding=15)
chart_section.pack(fill=BOTH, expand=True)

frame_plot = tb.Frame(chart_section, bootstyle="light")
frame_plot.pack(expand=True, fill=BOTH)

# Footer
footer_frame = tb.Frame(main_container, bootstyle="light")
footer_frame.pack(pady=10)

footer_label = tb.Label(footer_frame, text="© 2025 FocusGuard - Phát triển bởi Team", 
                       font=("Segoe UI", 9), foreground="#95a5a6", bootstyle="light")
footer_label.pack()

show_empty_chart()
root.mainloop()
>>>>>>> c96edbf52c8ea0fd75d2a8d412179c28bac51bff
