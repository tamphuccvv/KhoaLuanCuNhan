import tkinter as tk
from tkinter import ttk, messagebox
from employee import Employee
from GenericManager import GenericManager
import re

class EmployeeGUI:
    def __init__(self, root):
        self.manager = GenericManager('employees.json', Employee)
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
        ttk.Label(main_frame, text="Mã nhân viên", style="Custom.TLabel").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Tên", style="Custom.TLabel").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Số điện thoại", style="Custom.TLabel").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Tuổi", style="Custom.TLabel").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Ngày sinh", style="Custom.TLabel").grid(row=4, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Ca làm việc", style="Custom.TLabel").grid(row=5, column=0, sticky='w', padx=5, pady=2)

        self.entry_id = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_name = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_phone = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_age = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_birth_date = ttk.Entry(main_frame, style="Custom.TEntry")
        self.shift_var = tk.StringVar(value="Sáng")
        self.shift_dropdown = ttk.Combobox(
            main_frame, textvariable=self.shift_var, values=["Sáng", "Chiều", "Tối"],
            state="readonly", style="Custom.TCombobox"
        )

        self.entry_id.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        self.entry_name.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        self.entry_phone.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        self.entry_age.grid(row=3, column=1, sticky='w', padx=5, pady=2)
        self.entry_birth_date.grid(row=4, column=1, sticky='w', padx=5, pady=2)
        self.shift_dropdown.grid(row=5, column=1, sticky='w', padx=5, pady=2)

        # Nút điều khiển
        ttk.Button(main_frame, text="Thêm", command=self.add_employee, style="Custom.TButton").grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(main_frame, text="Cập nhật", command=self.update_employee, style="Custom.TButton").grid(row=6, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Xóa", command=self.delete_employee, style="Custom.TButton").grid(row=6, column=2, padx=5, pady=5)

        # Bảng danh sách
        self.tree = ttk.Treeview(
            main_frame, columns=("id", "name", "phone", "age", "birth_date", "shift"),
            show='headings', style="Treeview"
        )
        self.tree.heading("id", text="Mã nhân viên")
        self.tree.heading("name", text="Tên")
        self.tree.heading("phone", text="Số điện thoại")
        self.tree.heading("age", text="Tuổi")
        self.tree.heading("birth_date", text="Ngày sinh")
        self.tree.heading("shift", text="Ca làm việc")
        self.tree.column("id", width=100)
        self.tree.column("name", width=150)
        self.tree.column("phone", width=100)
        self.tree.column("age", width=50)
        self.tree.column("birth_date", width=100)
        self.tree.column("shift", width=100)
        self.tree.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.refresh_table()

    # Kiểm tra định dạng số điện thoại (10 chữ số, bắt đầu bằng 0)
    def validate_phone(self, phone):
        return bool(re.match(r"^0\d{9}$", phone))

    def add_employee(self):
        try:
            employee_id = self.entry_id.get().strip()
            name = self.entry_name.get().strip()
            phone = self.entry_phone.get().strip()
            age = self.entry_age.get().strip()
            birth_date = self.entry_birth_date.get().strip()
            shift = self.shift_var.get()

            if not all([employee_id, name, phone, age, birth_date]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
                return
            if not self.validate_phone(phone):
                messagebox.showerror("Lỗi", "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0.")
                return
            if any(e.employee_id == employee_id for e in self.manager.items):
                messagebox.showerror("Lỗi", f"Mã nhân viên {employee_id} đã tồn tại.")
                return
            employee = Employee(employee_id, name, phone, age, birth_date, shift)
            self.manager.add(employee)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Thêm nhân viên thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def update_employee(self):
        try:
            employee_id = self.entry_id.get().strip()
            name = self.entry_name.get().strip()
            phone = self.entry_phone.get().strip()
            age = self.entry_age.get().strip()
            birth_date = self.entry_birth_date.get().strip()
            shift = self.shift_var.get()

            if not all([employee_id, name, phone, age, birth_date]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
                return
            if not self.validate_phone(phone):
                messagebox.showerror("Lỗi", "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0.")
                return
            new_data = {
                "name": name,
                "phone": phone,
                "age": age,
                "birth_date": birth_date,
                "shift": shift
            }
            self.manager.update_by_id("employee_id", employee_id, new_data)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Cập nhật nhân viên thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def delete_employee(self):
        try:
            employee_id = self.entry_id.get().strip()
            if not employee_id:
                messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để xóa.")
                return
            if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa nhân viên {employee_id}?"):
                return
            self.manager.delete_by_id("employee_id", employee_id)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Xóa nhân viên thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def on_select(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values:
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, values[0])
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, values[1])
            self.entry_phone.delete(0, tk.END)
            self.entry_phone.insert(0, values[2])
            self.entry_age.delete(0, tk.END)
            self.entry_age.insert(0, values[3])
            self.entry_birth_date.delete(0, tk.END)
            self.entry_birth_date.insert(0, values[4])
            self.shift_var.set(values[5])

    def refresh_table(self):
        self.manager.reload()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for e in self.manager.items:
            self.tree.insert("", "end", values=(e.employee_id, e.name, e.phone, e.age, e.birth_date, e.shift))