import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image, ImageTk


def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Quản lý Nhà xe")
        self.root.geometry("450x600")
        self.root.resizable(False, False)

        # Thiết lập hình nền
        self.setup_background()

        # Cấu hình giao diện
        self.configure_styles()

        # Khung chính (card-like)
        self.main_container = tk.Frame(self.root, bg="#FFFFFF", bd=0)
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=550)
        self.main_container.config(highlightbackground="#D0D4D8", highlightthickness=1, relief="solid")

        # Tiêu đề
        title_label = tk.Label(
            self.main_container,
            text="Hệ thống Quản lý Nhà xe",
            font=("Segoe UI", 16, "bold"),
            fg="#333333",
            bg="#FFFFFF",
            pady=10
        )
        title_label.pack(fill="x")

        # Notebook
        self.notebook = ttk.Notebook(self.main_container)
        self.tab_login = ttk.Frame(self.notebook)
        self.tab_register = ttk.Frame(self.notebook)
        self.tab_forgot = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_login, text='Đăng nhập')
        self.notebook.add(self.tab_register, text='Đăng ký')
        self.notebook.add(self.tab_forgot, text='Quên mật khẩu')
        self.notebook.pack(padx=20, pady=10, fill='both', expand=True)

        # Nhãn trạng thái
        self.status_label = tk.Label(
            self.main_container,
            text="",
            font=("Segoe UI", 10),
            fg="#333333",
            bg="#FFFFFF",
            wraplength=350
        )
        self.status_label.pack(pady=5)

        # Xây dựng các tab
        self.build_login()
        self.build_register()
        self.build_forgot()

        self.smtp_email = "maxacnhanbdx@gmail.com"
        self.smtp_password = "tgnc dzkp ezxg smkv"

    def setup_background(self):
        try:
            bg_img = Image.open("abb.png")
            bg_img = bg_img.resize((450, 600), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Không thể tải hình nền: {str(e)}")
            self.root.configure(bg="#F5F7FA")

    def configure_styles(self):
        style = ttk.Style()
        # Notebook
        style.configure("TNotebook", background="#FFFFFF")
        style.configure("TNotebook.Tab",
                        background="#E6E8EB",
                        foreground="#333333",
                        font=("Segoe UI", 11),
                        padding=[15, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", "#FFFFFF"), ("active", "#F0F2F5")],
                  foreground=[("selected", "#4A90E2"), ("active", "#4A90E2")])

        # Nút
        style.configure("TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=10,
                        background="#4A90E2",
                        foreground="#333333")
        style.map("TButton",
                  background=[("active", "#357ABD")],
                  foreground=[("active", "#FFFFFF")])

        # Nhãn
        style.configure("TLabel",
                        font=("Segoe UI", 11),
                        background="#FFFFFF",
                        foreground="#333333")

        # Trường nhập liệu
        style.configure("TEntry",
                        fieldbackground="#F0F2F5",
                        foreground="#333333",
                        padding=8)
        style.map("TEntry",
                  fieldbackground=[("focus", "#FFFFFF")],
                  highlightcolor=[("focus", "#4A90E2")])

        # Combobox
        style.configure("TCombobox",
                        fieldbackground="#F0F2F5",
                        foreground="#333333",
                        padding=8)
        style.map("TCombobox",
                  fieldbackground=[("focus", "#FFFFFF")],
                  selectbackground=[("focus", "#FFFFFF")])

    def build_login(self):
        form_frame = tk.Frame(self.tab_login, bg="#FFFFFF")
        form_frame.pack(pady=30, padx=20, fill="both", expand=True)

        ttk.Label(form_frame, text="Tài khoản", style="TLabel").pack(pady=(0, 5))
        self.login_user = ttk.Entry(form_frame, style="TEntry")
        self.login_user.pack(fill="x", pady=(0, 10))
        self.login_user.insert(0, "Nhập tài khoản")
        self.login_user.bind("<FocusIn>", lambda e: self.clear_placeholder(self.login_user, "Nhập tài khoản"))
        self.login_user.bind("<FocusOut>", lambda e: self.set_placeholder(self.login_user, "Nhập tài khoản"))

        ttk.Label(form_frame, text="Mật khẩu", style="TLabel").pack(pady=(0, 5))
        self.login_pass = ttk.Entry(form_frame, show="*", style="TEntry")
        self.login_pass.pack(fill="x", pady=(0, 10))
        self.login_pass.insert(0, "Nhập mật khẩu")
        self.login_pass.bind("<FocusIn>", lambda e: self.clear_placeholder(self.login_pass, "Nhập mật khẩu", show="*"))
        self.login_pass.bind("<FocusOut>", lambda e: self.set_placeholder(self.login_pass, "Nhập mật khẩu", show="*"))

        login_button = ttk.Button(form_frame, text="Đăng nhập", command=self.login, style="TButton")
        login_button.pack(pady=20)

    def build_register(self):
        form_frame = tk.Frame(self.tab_register, bg="#FFFFFF")
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)

        labels = ["Tài khoản", "Mật khẩu", "Số điện thoại", "Email"]
        self.register_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=label, style="TLabel").grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entry = ttk.Entry(form_frame, style="TEntry")
            if label == "Mật khẩu":
                entry.config(show="*")
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            placeholder = f"Nhập {label.lower()}"
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e, p=placeholder: self.clear_placeholder(e.widget, p))
            entry.bind("<FocusOut>", lambda e, p=placeholder: self.set_placeholder(e.widget, p,
                                                                                   show="*" if label == "Mật khẩu" else ""))
            self.register_entries[label.lower()] = entry

        ttk.Label(form_frame, text="Vai trò", style="TLabel").grid(row=len(labels), column=0, padx=5, pady=5,
                                                                   sticky='w')
        self.role_var = tk.StringVar(value="user")
        role_dropdown = ttk.Combobox(form_frame, textvariable=self.role_var, values=["user", "admin"], state="readonly",
                                     style="TCombobox")
        role_dropdown.grid(row=len(labels), column=1, padx=5, pady=5, sticky='ew')
        role_dropdown.bind("<<ComboboxSelected>>", self.toggle_admin)

        self.admin_code_label = ttk.Label(form_frame, text="Mã Admin", style="TLabel")
        self.admin_code_entry = ttk.Entry(form_frame, style="TEntry")
        self.admin_code_entry.insert(0, "Nhập mã admin")
        self.admin_code_entry.bind("<FocusIn>",
                                   lambda e: self.clear_placeholder(self.admin_code_entry, "Nhập mã admin"))
        self.admin_code_entry.bind("<FocusOut>", lambda e: self.set_placeholder(self.admin_code_entry, "Nhập mã admin"))
        self.toggle_admin(None)

        register_button = ttk.Button(form_frame, text="Đăng ký", command=self.register, style="TButton")
        register_button.grid(row=len(labels) + 2, column=0, columnspan=2, pady=15, sticky='ew')

        form_frame.grid_columnconfigure(1, weight=1)

    def build_forgot(self):
        form_frame = tk.Frame(self.tab_forgot, bg="#FFFFFF")
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ttk.Label(form_frame, text="Tài khoản", style="TLabel").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.forgot_user = ttk.Entry(form_frame, style="TEntry")
        self.forgot_user.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.forgot_user.insert(0, "Nhập tài khoản")
        self.forgot_user.bind("<FocusIn>", lambda e: self.clear_placeholder(self.forgot_user, "Nhập tài khoản"))
        self.forgot_user.bind("<FocusOut>", lambda e: self.set_placeholder(self.forgot_user, "Nhập tài khoản"))

        ttk.Label(form_frame, text="Email", style="TLabel").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.forgot_contact = ttk.Entry(form_frame, style="TEntry")
        self.forgot_contact.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.forgot_contact.insert(0, "Nhập email")
        self.forgot_contact.bind("<FocusIn>", lambda e: self.clear_placeholder(self.forgot_contact, "Nhập email"))
        self.forgot_contact.bind("<FocusOut>", lambda e: self.set_placeholder(self.forgot_contact, "Nhập email"))

        send_code_button = ttk.Button(form_frame, text="Gửi mã xác nhận", command=self.send_code, style="TButton")
        send_code_button.grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')

        ttk.Label(form_frame, text="Mã xác nhận", style="TLabel").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.entry_code = ttk.Entry(form_frame, style="TEntry")
        self.entry_code.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.entry_code.insert(0, "Nhập mã xác nhận")
        self.entry_code.bind("<FocusIn>", lambda e: self.clear_placeholder(self.entry_code, "Nhập mã xác nhận"))
        self.entry_code.bind("<FocusOut>", lambda e: self.set_placeholder(self.entry_code, "Nhập mã xác nhận"))

        ttk.Label(form_frame, text="Mật khẩu mới", style="TLabel").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.entry_newpass = ttk.Entry(form_frame, show="*", style="TEntry")
        self.entry_newpass.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        self.entry_newpass.insert(0, "Nhập mật khẩu mới")
        self.entry_newpass.bind("<FocusIn>",
                                lambda e: self.clear_placeholder(self.entry_newpass, "Nhập mật khẩu mới", show="*"))
        self.entry_newpass.bind("<FocusOut>",
                                lambda e: self.set_placeholder(self.entry_newpass, "Nhập mật khẩu mới", show="*"))

        reset_button = ttk.Button(form_frame, text="Đặt lại mật khẩu", command=self.reset_password, style="TButton")
        reset_button.grid(row=5, column=0, columnspan=2, pady=15, sticky='ew')

        form_frame.grid_columnconfigure(1, weight=1)
        self.confirmation_code = ""

    def clear_placeholder(self, entry, placeholder, show=None):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            if show:
                entry.config(show=show)

    def set_placeholder(self, entry, placeholder, show=None):
        if not entry.get():
            entry.insert(0, placeholder)
            if show:
                entry.config(show="")

    def toggle_admin(self, event=None):
        if self.role_var.get() == "admin":
            self.admin_code_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
            self.admin_code_entry.grid(row=5, column=1, padx=5, pady=5, sticky='ew')
        else:
            self.admin_code_label.grid_remove()
            self.admin_code_entry.grid_remove()
            self.admin_code_entry.delete(0, tk.END)
            self.admin_code_entry.insert(0, "Nhập mã admin")

    def validate_phone(self, phone):
        return bool(re.match(r"^0\d{9}$", phone))

    def validate_email(self, email):
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

    def login(self):
        self.status_label.config(text="Đang xử lý...", fg="#333333")
        self.root.update()
        username = self.login_user.get().strip()
        password = self.login_pass.get().strip()

        if username == "Nhập tài khoản" or password == "Nhập mật khẩu":
            messagebox.showerror("Lỗi", "Vui lòng nhập tài khoản và mật khẩu.")
            self.status_label.config(text="", fg="#333333")
            return

        users = load_data('users.json')
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if not user:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu.")
            self.status_label.config(text="Đăng nhập thất bại", fg="#D32F2F")
            return
        messagebox.showinfo("Thành công", f"Đăng nhập thành công với vai trò {user['role']}.")
        self.status_label.config(text="Đăng nhập thành công", fg="#388E3C")
        self.hide()
        if user['role'] == "admin":
            from admin_gui import AdminGUI
            admin_root = tk.Toplevel()
            AdminGUI(admin_root, self)
        else:
            from user_gui import UserMenuGUI
            user_root = tk.Toplevel()
            UserMenuGUI(user_root, self)

    def register(self):
        self.status_label.config(text="Đang xử lý...", fg="#333333")
        self.root.update()
        data = {k: e.get().strip() for k, e in self.register_entries.items()}
        role = self.role_var.get()
        admin_code = self.admin_code_entry.get().strip() if role == "admin" else ""

        if any(v in ["Nhập tài khoản", "Nhập mật khẩu", "Nhập số điện thoại", "Nhập email"] for v in data.values()):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            self.status_label.config(text="", fg="#333333")
            return

        if role == "admin" and not admin_code:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã admin.")
            self.status_label.config(text="", fg="#333333")
            return
        if role == "admin" and admin_code != "admin123":
            messagebox.showerror("Lỗi", "Mã admin không đúng.")
            self.status_label.config(text="", fg="#333333")
            return

        if not all(data.values()):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            self.status_label.config(text="", fg="#333333")
            return

        if not self.validate_phone(data['số điện thoại']):
            messagebox.showerror("Lỗi", "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0.")
            self.status_label.config(text="", fg="#333333")
            return

        if not self.validate_email(data['email']):
            messagebox.showerror("Lỗi", "Email không hợp lệ (ví dụ: user@domain.com).")
            self.status_label.config(text="", fg="#333333")
            return

        if len(data['mật khẩu']) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự.")
            self.status_label.config(text="", fg="#333333")
            return

        users = load_data('users.json')
        if any(u['username'] == data['tài khoản'] for u in users):
            messagebox.showerror("Lỗi", "Tài khoản đã tồn tại.")
            self.status_label.config(text="", fg="#333333")
            return
        if any(u['phone'] == data['số điện thoại'] for u in users):
            messagebox.showerror("Lỗi", "Số điện thoại đã được sử dụng.")
            self.status_label.config(text="", fg="#333333")
            return

        new_user = {
            "username": data['tài khoản'],
            "password": data['mật khẩu'],
            "phone": data['số điện thoại'],
            "email": data['email'],
            "role": role
        }
        users.append(new_user)
        save_data(users, 'users.json')
        messagebox.showinfo("Thành công", "Đăng ký thành công. Vui lòng đăng nhập.")
        self.status_label.config(text="Đăng ký thành công", fg="#388E3C")
        self.notebook.select(self.tab_login)
        self.clear_register_entries()

    def clear_register_entries(self):
        for entry in self.register_entries.values():
            entry.delete(0, tk.END)
            entry.insert(0,
                         f"Nhập {entry.master.winfo_children()[entry.grid_info()['row'] * 2].cget('text').replace(':', '').lower()}")
        self.admin_code_entry.delete(0, tk.END)
        self.admin_code_entry.insert(0, "Nhập mã admin")
        self.role_var.set("user")
        self.toggle_admin()

    def send_code(self):
        self.status_label.config(text="Đang gửi mã...", fg="#333333")
        self.root.update()
        username = self.forgot_user.get().strip()
        contact = self.forgot_contact.get().strip()

        if username == "Nhập tài khoản" or contact == "Nhập email":
            messagebox.showerror("Lỗi", "Vui lòng nhập tài khoản và email.")
            self.status_label.config(text="", fg="#333333")
            return

        users = load_data('users.json')
        user_found = None

        for user in users:
            if user['username'] == username and (user['phone'] == contact or user['email'] == contact):
                user_found = user
                break

        if not user_found:
            messagebox.showerror("Lỗi", "Không tìm thấy tài khoản hoặc thông tin liên hệ không khớp.")
            self.status_label.config(text="", fg="#333333")
            return

        self.confirmation_code = str(random.randint(100000, 999999))

        if self.validate_email(contact):
            try:
                self.send_email(contact, self.confirmation_code)
                messagebox.showinfo("Thành công", f"Mã xác nhận đã được gửi đến {contact}.")
                self.status_label.config(text="Mã xác nhận đã gửi", fg="#388E3C")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể gửi email: {str(e)}")
                self.status_label.config(text="", fg="#333333")
                return
        else:
            messagebox.showinfo("Mã xác nhận", f"Mã xác nhận của bạn là: {self.confirmation_code}")
            self.status_label.config(text="Mã xác nhận đã hiển thị", fg="#388E3C")

    def send_email(self, recipient_email, code):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_email
        msg['To'] = recipient_email
        msg['Subject'] = "Mã xác nhận đặt lại mật khẩu"

        body = f"""
        Chào bạn,

        Mã xác nhận để đặt lại mật khẩu của bạn là: **{code}**

        Vui lòng sử dụng mã này để tiếp tục quá trình đặt lại mật khẩu.
        Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.

        Trân trọng,
        Hệ thống Quản lý Nhà xe
        """
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.smtp_email, self.smtp_password)
                server.sendmail(self.smtp_email, recipient_email, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            raise Exception("Thông tin đăng nhập SMTP không hợp lệ. Vui lòng kiểm tra email và App Password.")
        except Exception as e:
            raise Exception(f"Lỗi gửi email: {str(e)}")

    def reset_password(self):
        self.status_label.config(text="Đang xử lý...", fg="#333333")
        self.root.update()
        username = self.forgot_user.get().strip()
        input_code = self.entry_code.get().strip()
        new_pass = self.entry_newpass.get().strip()

        if username == "Nhập tài khoản" or input_code == "Nhập mã xác nhận" or new_pass == "Nhập mật khẩu mới":
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            self.status_label.config(text="", fg="#333333")
            return
        if input_code != self.confirmation_code:
            messagebox.showerror("Lỗi", "Mã xác nhận không đúng.")
            self.status_label.config(text="", fg="#333333")
            return

        users = load_data('users.json')
        for user in users:
            if user['username'] == username:
                user['password'] = new_pass
                save_data(users, 'users.json')
                messagebox.showinfo("Thành công", "Mật khẩu đã được cập nhật.")
                self.status_label.config(text="Đặt lại mật khẩu thành công", fg="#388E3C")
                self.notebook.select(self.tab_login)
                self.clear_forgot_entries()
                return
        messagebox.showerror("Lỗi", "Không tìm thấy tài khoản.")
        self.status_label.config(text="", fg="#333333")

    def clear_forgot_entries(self):
        self.forgot_user.delete(0, tk.END)
        self.forgot_user.insert(0, "Nhập tài khoản")
        self.forgot_contact.delete(0, tk.END)
        self.forgot_contact.insert(0, "Nhập email")
        self.entry_code.delete(0, tk.END)
        self.entry_code.insert(0, "Nhập mã xác nhận")
        self.entry_newpass.delete(0, tk.END)
        self.entry_newpass.insert(0, "Nhập mật khẩu mới")
        self.confirmation_code = ""

    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.deiconify()
        self.notebook.select(self.tab_login)
        self.clear_register_entries()
        self.login_user.delete(0, tk.END)
        self.login_user.insert(0, "Nhập tài khoản")
        self.login_pass.delete(0, tk.END)
        self.login_pass.insert(0, "Nhập mật khẩu")