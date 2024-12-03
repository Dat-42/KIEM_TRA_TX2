#Nhập ma trận
#tÍNH ĐỊNH THỨC
#tÍNH HẠNG
import numpy as np
import tkinter as tk
import pandas as pd
from tkinter import messagebox, simpledialog, filedialog

# Biến lưu ma trận hiện tại
current_matrix = None

# Hàm tải ma trận từ file
def load_matrix_from_file():
    global current_matrix
    try:
        # Mở hộp thoại để chọn file
        file_path = filedialog.askopenfilename(
            title="Chọn tệp chứa ma trận",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        # Xử lý file theo định dạng
        if file_path.endswith('.csv'):
            matrix = pd.read_csv(file_path, header=None).values  # Đọc file CSV
        else:  # Mặc định đọc file văn bản
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if not lines:
                    raise ValueError("Tệp rỗng, không chứa dữ liệu.")
                matrix = [list(map(float, line.strip().split(','))) for line in lines]

        # Kiểm tra tính hợp lệ của ma trận
        row_lengths = [len(row) for row in matrix]
        if len(set(row_lengths)) != 1:
            raise ValueError("Các hàng trong tệp không có độ dài bằng nhau.")

        # Chuyển ma trận sang định dạng NumPy
        current_matrix = np.array(matrix)
        messagebox.showinfo("Thông báo", f"Ma trận đã được tải:\n{current_matrix}")

    except ValueError as e:
        messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {e}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi tải tệp: {e}")


# Hàm tạo cửa sổ nhập ma trận
def input_matrix():
    def create_matrix_window():
        try:
            rows = int(row_entry.get())
            cols = int(col_entry.get())
            if rows <= 0 or cols <= 0:
                raise ValueError("Số hàng và số cột phải lớn hơn 0.")

            input_window = tk.Toplevel(root)
            input_window.title("Nhập giá trị ma trận")

            entries = []

            for i in range(rows):
                row_entries = []
                for j in range(cols):
                    entry = tk.Entry(input_window, width=5, justify='center')
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                entries.append(row_entries)

            def confirm_matrix():
                global current_matrix
                try:
                    matrix = []
                    for i in range(rows):
                        row = []
                        for j in range(cols):
                            value = entries[i][j].get()
                            if not value.strip():
                                raise ValueError("Các ô nhập không được để trống.")
                            row.append(int(value))
                        matrix.append(row)
                    current_matrix = np.array(matrix)
                    messagebox.showinfo("Thông báo", f"Ma trận đã được nhập:\n{current_matrix}")
                    input_window.destroy()
                except ValueError as e:
                    messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {e}")

            confirm_button = tk.Button(input_window, text="Xác nhận", command=confirm_matrix)
            confirm_button.grid(row=rows, columnspan=cols, pady=10)

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hàng và số cột hợp lệ (số nguyên dương).")

            def confirm_matrix():
                global current_matrix
                try:
                    matrix = []
                    for i in range(rows):
                        row = []
                        for j in range(cols):
                            value = entries[i][j].get()
                            row.append(int(value))
                        matrix.append(row)
                    current_matrix = np.array(matrix)
                    messagebox.showinfo("Thông báo", f"Ma trận đã được nhập:\n{current_matrix}")
                    input_window.destroy()
                except ValueError:
                    messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ (số nguyên).")

            confirm_button = tk.Button(input_window, text="Xác nhận", command=confirm_matrix)
            confirm_button.grid(row=rows, columnspan=cols, pady=10)

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hàng và số cột hợp lệ (số nguyên dương).")

    size_window = tk.Toplevel(root)
    size_window.title("Chọn kích thước ma trận")

    tk.Label(size_window, text="Số hàng:").grid(row=0, column=0, padx=10, pady=5)
    row_entry = tk.Entry(size_window, width=5)
    row_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(size_window, text="Số cột:").grid(row=1, column=0, padx=10, pady=5)
    col_entry = tk.Entry(size_window, width=5)
    col_entry.grid(row=1, column=1, padx=10, pady=5)

    next_button = tk.Button(size_window, text="Tiếp tục", command=create_matrix_window)
    next_button.grid(row=2, columnspan=2, pady=10)

# Hàm tính toán cơ bản
def calculate_basic():
    if current_matrix is None:
        messagebox.showerror("Lỗi", "Vui lòng nhập hoặc tải ma trận trước!")
        return

    largest_element = current_matrix.max()
    row_wise_max = current_matrix.max(axis=1)
    col_wise_min = current_matrix.min(axis=0)
    total_sum = current_matrix.sum()
    cumulative_sum = current_matrix.cumsum(axis=1)

    result = (
        f"Ma trận:\n{current_matrix}\n\n"
        f"Phần tử lớn nhất: {largest_element}\n"
        f"Giá trị lớn nhất theo từng hàng: {row_wise_max}\n"
        f"Giá trị nhỏ nhất theo từng cột: {col_wise_min}\n"
        f"Tổng các phần tử: {total_sum}\n"
        f"Tổng tích lũy theo từng hàng:\n{cumulative_sum}\n"
    )
    messagebox.showinfo("Kết quả cơ bản", result)

# Hàm tính định thức và nghịch đảo
def calculate_determinant_and_inverse():
    if current_matrix is None:
        messagebox.showerror("Lỗi", "Vui lòng nhập hoặc tải ma trận trước!")
        return

    if current_matrix.shape[0] != current_matrix.shape[1]:
        messagebox.showinfo("Thông báo", "Chỉ áp dụng cho ma trận vuông!")
        return

    determinant = np.linalg.det(current_matrix)
    try:
        if np.isclose(determinant, 0):
            raise np.linalg.LinAlgError("Định thức bằng 0, không thể tính nghịch đảo.")
        inverse = np.linalg.inv(current_matrix)
        result = f"Định thức: {determinant:.2f}\nNghịch đảo ma trận:\n{inverse}\n"
    except np.linalg.LinAlgError as e:
        result = f"Định thức: {determinant:.2f}\n{e}\n"

    # Hiển thị kết quả và lưu file
    messagebox.showinfo("Định thức và nghịch đảo", result)
    save_to_file(result, filename="det_and_inverse.txt")


# Hàm tính hạng và chuyển vị
def calculate_rank_and_transpose():
    if current_matrix is None:
        messagebox.showerror("Lỗi", "Vui lòng nhập hoặc tải ma trận trước!")
        return

    rank = np.linalg.matrix_rank(current_matrix)
    transpose = current_matrix.T

    result = f"Hạng của ma trận: {rank}\nMa trận chuyển vị:\n{transpose}\n"

    # Hiển thị kết quả và lưu file
    messagebox.showinfo("Hạng và chuyển vị", result)
    save_to_file(result, filename="rank_and_transpose.txt")

def save_to_file(data, filename="result.txt", is_csv=False):
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt" if not is_csv else ".csv",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")] if not is_csv else [("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        if is_csv:
            # Ghi dữ liệu dưới dạng CSV nếu là ma trận
            pd.DataFrame(data).to_csv(file_path, index=False, header=False)
        else:
            # Ghi dữ liệu dạng văn bản
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(data))
        messagebox.showinfo("Thông báo", f"Kết quả đã được lưu vào file: {file_path}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")

def save_current_matrix():
    if current_matrix is None:
        messagebox.showerror("Lỗi", "Không có ma trận nào để lưu!")
        return
    save_to_file(current_matrix, filename="current_matrix.csv", is_csv=True)

# Giao diện chính
root = tk.Tk()
root.title("Matrix Processor")
root.geometry("500x450")

label = tk.Label(
    root,
    text="Chào mừng bạn đến với Matrix Processor!\nHãy nhập hoặc tải ma trận và chọn chức năng xử lý.",
    font=("Arial", 12),
    wraplength=480,
    justify="center"
)
label.pack(pady=20)

load_button = tk.Button(root, text="Tải ma trận từ tệp", command=load_matrix_from_file, font=("Arial", 12), bg="#87CEFA")
load_button.pack(pady=10)

input_button = tk.Button(root, text="Nhập ma trận", command=input_matrix, font=("Arial", 12), bg="#87CEEB")
input_button.pack(pady=10)

basic_button = tk.Button(root, text="Tính toán cơ bản", command=calculate_basic, font=("Arial", 12), bg="#FFB6C1")
basic_button.pack(pady=10)

det_inv_button = tk.Button(root, text="Định thức và nghịch đảo", command=calculate_determinant_and_inverse, font=("Arial", 12), bg="#98FB98")
det_inv_button.pack(pady=10)

rank_transpose_button = tk.Button(root, text="Hạng và chuyển vị", command=calculate_rank_and_transpose, font=("Arial", 12), bg="#FFD700")
rank_transpose_button.pack(pady=10)

save_matrix_button = tk.Button(root, text="Lưu Ma trận", command=save_current_matrix)
save_matrix_button.pack(pady=10)

save_results_button = tk.Button(root, text="Lưu Kết quả", command=lambda: save_to_file("Kết quả cụ thể"))
save_results_button.pack(pady=10)

root.mainloop()
