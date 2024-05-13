import tkinter as tk
from PIL import Image, ImageTk

def Program_screen():
    # Thêm mã của chương trình của bạn ở đây
    pass

# Tạo cửa sổ giao diện
interface = tk.Tk()
interface.title("Button on Image")

# Load ảnh từ tệp interface.jpg
image = Image.open("Interface.png")
image = image.resize((940, 788))  # Thay đổi kích thước ảnh nếu cần
photo = ImageTk.PhotoImage(image)

# Hiển thị ảnh trên label
label = tk.Label(interface, image=photo)
label.pack()

# Tạo và đặt nút Btn trên ảnh
button = tk.Button(interface, text='Go to program', font=("Times New Roman", 20, "bold"),
                    bg="skyblue", fg='black', command=Program_screen)
button.place(x=450, y=550)  # Đặt vị trí của nút Btn trên ảnh

# Khởi chạy giao diện người dùng
interface.mainloop()
