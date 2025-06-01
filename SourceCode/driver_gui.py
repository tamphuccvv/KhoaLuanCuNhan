import tkinter as tk
from tkinter import ttk, messagebox
from driver import Driver
from GenericManager import GenericManager
import re

class DriverGUI:
    def __init__(self, root):
        self.manager = GenericManager('drivers.json', Driver)
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
        ttk.Label(main_frame, text="Mã tài xế", style="Custom.TLabel").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Tên", style="Custom.TLabel").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Số điện thoại", style="Custom.TLabel").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Tình trạng bằng lái", style="Custom.TLabel").grid(row=3, column=0, sticky='w', padx=5, pady=2)

        self.entry_id = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_name = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_phone = ttk.Entry(main_frame, style="Custom.TEntry")
        self.status_var = tk.StringVar(value="Valid")
        self.status_dropdown = ttk.Combobox(
            main_frame, textvariable=self.status_var,
            values=["Valid", "Expired", "Suspended"], state="readonly", style="Custom.TCombobox"
        )

        self.entry_id.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        self.entry_name.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        self.entry_phone.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        self.status_dropdown.grid(row=3, column=1, sticky='w', padx=5, pady=2)

        # Nút điều khiển
        ttk.Button(main_frame, text="Thêm", command=self.add_driver, style="Custom.TButton").grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(main_frame, text="Cập nhật", command=self.update_driver, style="Custom.TButton").grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Xóa", command=self.delete_driver, style="Custom.TButton").grid(row=4, column=2, padx=5, pady=5)

        # Bảng danh sách
        self.tree = ttk.Treeview(
            main_frame, columns=("id", "name", "phone", "license_status"), show='headings', style="Treeview"
        )
        self.tree.heading("id", text="Mã tài xế")
        self.tree.heading("name", text="Tên")
        self.tree.heading("phone", text="Số điện thoại")
        self.tree.heading("license_status", text="Tình trạng bằng lái")
        self.tree.column("id", width=100)
        self.tree.column("name", width=150)
        self.tree.column("phone", width=100)
        self.tree.column("license_status", width=100)
        self.tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.refresh_table()

    # Kiểm tra định dạng số điện thoại
    def validate_phone(self, phone):
        return bool(re.match(r"^0\d{9}$", phone))

    def add_driver(self):
        try:
            driver_id = self.entry_id.get().strip()
            name = self.entry_name.get().strip()
            phone = self.entry_phone.get().strip()
            license_status = self.status_var.get()

            if not all([driver_id, name, phone]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
                return
            if not self.validate_phone(phone):
                messagebox.showerror("Lỗi", "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0.")
                return
            if any(d.driver_id == driver_id for d in self.manager.items):
                messagebox.showerror("Lỗi", f"Mã tài xế {driver_id} đã tồn tại.")
                return
            driver = Driver(driver_id, name, phone, license_status)
            self.manager.add(driver)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Thêm tài xế thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def update_driver(self):
        try:
            driver_id = self.entry_id.get().strip()
            name = self.entry_name.get().strip()
            phone = self.entry_phone.get().strip()
            license_status = self.status_var.get()

            if not all([driver_id, name, phone]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
                return
            if not self.validate_phone(phone):
                messagebox.showerror("Lỗi", "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0.")
                return
            new_data = {
                "name": name,
                "phone": phone,
                "license_status": license_status
            }
            self.manager.update_by_id("driver_id", driver_id, new_data)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Cập nhật tài xế thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def delete_driver(self):
        try:
            driver_id = self.entry_id.get().strip()
            if not driver_id:
                messagebox.showerror("Lỗi", "Vui lòng chọn tài xế để xóa.")
                return
            if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa tài xế {driver_id}?"):
                return
            self.manager.delete_by_id("driver_id", driver_id)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Xóa tài xế thành công!")
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
            self.status_var.set(values[3])

    def refresh_table(self):
        self.manager.reload()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for d in self.manager.items:
            self.tree.insert("", "end", values=(d.driver_id, d.name, d.phone, d.license_status))