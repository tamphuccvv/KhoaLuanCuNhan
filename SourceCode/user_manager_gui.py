import tkinter as tk
from tkinter import ttk, messagebox
from user import User
from GenericManager import GenericManager
import re

class UserGUI:
    def __init__(self, root):
        self.manager = GenericManager('users.json', User)
        self.root = root

        # Cấu hình style
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#E6F0FA")
        style.configure("Custom.TLabel", background="#E6F0FA", foreground="#333333", font=("Arial", 10))
        style.configure("Custom.TButton", background="#4A90E2", foreground="#333333", padding=6, font=("Arial", 10, "bold"))
        style.map("Custom.TButton", background=[("active", "#357ABD")])
        style.configure("Custom.TEntry", fieldbackground="#FFFFFF", foreground="#333333")
        style.configure("Custom.TCombobox", fieldbackground="#FFFFFF", foreground="#333333")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", background="#DCE4F5", foreground="#333333", font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#B3D4FC")])

        # Frame chính
        main_frame = ttk.Frame(root, style="Custom.TFrame", padding=10)
        main_frame.pack(fill="both", expand=True)

        # Form nhập liệu
        ttk.Label(main_frame, text="Tài khoản", style="Custom.TLabel").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Mật khẩu", style="Custom.TLabel").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Vai trò", style="Custom.TLabel").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Số điện thoại", style="Custom.TLabel").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Email", style="Custom.TLabel").grid(row=4, column=0, sticky='w', padx=5, pady=2)

        self.entry_username = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_password = ttk.Entry(main_frame, show="*", style="Custom.TEntry")
        self.role_var = tk.StringVar(value="user")
        self.role_dropdown = ttk.Combobox(
            main_frame, textvariable=self.role_var, values=["user"], state="readonly", style="Custom.TCombobox"
        )
        self.entry_phone = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_email = ttk.Entry(main_frame, style="Custom.TEntry")

        self.entry_username.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        self.entry_password.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        self.role_dropdown.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        self.entry_phone.grid(row=3, column=1, sticky='w', padx=5, pady=2)
        self.entry_email.grid(row=4, column=1, sticky='w', padx=5, pady=2)

        # Nút điều khiển
        ttk.Button(main_frame, text="Thêm", command=self.add_user, style="Custom.TButton").grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(main_frame, text="Cập nhật", command=self.update_user, style="Custom.TButton").grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Xóa", command=self.delete_user, style="Custom.TButton").grid(row=5, column=2, padx=5, pady=5)

        # Bảng danh sách
        self.tree = ttk.Treeview(
            main_frame, columns=("username", "password", "role", "phone", "email"), show='headings', style="Treeview"
        )
        self.tree.heading("username", text="Tài khoản")
        self.tree.heading("password", text="Mật khẩu")
        self.tree.heading("role", text="Vai trò")
        self.tree.heading("phone", text="Số điện thoại")
        self.tree.heading("email", text="Email")
        self.tree.column("username", width=150)
        self.tree.column("password", width=150)
        self.tree.column("role", width=100)
        self.tree.column("phone", width=100)
        self.tree.column("email", width=150)
        self.tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.refresh_table()

    def validate_phone(self, phone):
        """Kiểm tra định dạng số điện thoại (10 chữ số, bắt đầu bằng 0)"""
        return bool(re.match(r"^0\d{9}$", phone))

    def validate_email(self, email):
        """Kiểm tra định dạng email hợp lệ"""
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

    def add_user(self):
        try:
            username = self.entry_username.get().strip()
            password = self.entry_password.get().strip()
            phone = self.entry_phone.get().strip()
            email = self.entry_email.get().strip()

            if not all([username, password, phone, email]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
                return
            if any(u.username == username for u in self.manager.items):
                messagebox.showerror("Lỗi", f"Tài khoản {username} đã tồn tại.")
                return
            if not self.validate_phone(phone):
                messagebox.showerror("Lỗi", "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0.")
                return
            if not self.validate_email(email):
                messagebox.showerror("Lỗi", "Email không hợp lệ.")
                return

            user = User(
                username=username,
                password=password,
                role="user",
                phone=phone,
                email=email
            )
            self.manager.add(user)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Thêm người dùng thành công!")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def update_user(self):
        try:
            username = self.entry_username.get().strip()
            password = self.entry_password.get().strip()
            phone = self.entry_phone.get().strip()
            email = self.entry_email.get().strip()

            if not username:
                messagebox.showerror("Lỗi", "Tài khoản không được để trống.")
                return
            user = self.manager.get_by_id("username", username)
            if not user or user.role != "user":
                messagebox.showerror("Lỗi", "Chỉ có thể cập nhật tài khoản người dùng (user).")
                return
            if not all([password, phone, email]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
                return
            if not self.validate_phone(phone):
                messagebox.showerror("Lỗi", "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0.")
                return
            if not self.validate_email(email):
                messagebox.showerror("Lỗi", "Email không hợp lệ.")
                return

            new_data = {
                "password": password,
                "role": "user",
                "phone": phone,
                "email": email
            }
            self.manager.update_by_id("username", username, new_data)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Cập nhật người dùng thành công!")
            self.clear_entries()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def delete_user(self):
        try:
            username = self.entry_username.get().strip()
            if not username:
                messagebox.showerror("Lỗi", "Vui lòng chọn người dùng để xóa.")
                return
            user = self.manager.get_by_id("username", username)
            if not user or user.role != "user":
                messagebox.showerror("Lỗi", "Chỉ có thể xóa tài khoản người dùng (user).")
                return
            if not messagebox.askyesno("Confirm", f"Bạn có chắc chắn muốn xóa người dùng {username}?"):
                return

            self.manager.delete_by_id("username", username)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Xóa người dùng thành công!")
            self.clear_entries()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected, 'values')
            if values:
                self.entry_username.delete(0, tk.END)
                self.entry_username.insert(0, str(values[0]))
                self.entry_password.delete(0, tk.END)
                self.entry_password.insert(0, str(values[1]))
                self.role_var.set(str(values[2]))
                self.entry_phone.delete(0, tk.END)
                self.entry_phone.insert(0, str(values[3]))
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, str(values[4]))

    def clear_entries(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.role_var.set("user")

    def refresh_table(self):
        self.manager.reload()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for u in self.manager.items:
            if u.role == "user":  # Chỉ hiển thị tài khoản user
                self.tree.insert("", "end", values=(u.username, u.password, u.role, u.phone, u.email))