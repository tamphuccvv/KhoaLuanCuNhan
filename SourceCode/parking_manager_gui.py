import tkinter as tk
from tkinter import ttk, messagebox
from parking_lot import ParkingLot
from GenericManager import GenericManager
import re

class ParkingManagerGUI:
    def __init__(self, root):
        self.manager = GenericManager('parkings.json', ParkingLot)
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
        ttk.Label(main_frame, text="Vị trí", style="Custom.TLabel").grid(row=0, column=0, sticky='ew')
        ttk.Label(main_frame, text="Sức chứa", style="Custom.TLabel").grid(row=1, column=0, sticky='ew')
        ttk.Label(main_frame, text="Trạng thái", style="Custom.TLabel").grid(row=2, column=0, sticky='ew')

        self.entry_location = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_max_capacity = ttk.Entry(main_frame, style="Custom.TEntry")
        self.status_var = tk.StringVar(value="Còn chỗ")
        self.status_dropdown = ttk.Combobox(main_frame, textvariable=self.status_var,
                                           values=["Còn chỗ", "Hết chỗ"], state="readonly", style="Custom.TCombobox")

        self.entry_location.grid(row=0, column=1, sticky='w')
        self.entry_max_capacity.grid(row=1, column=1, sticky='w')
        self.status_dropdown.grid(row=2, column=1, sticky='w')

        ttk.Button(main_frame, text="Thêm", command=self.add_parking, style="Custom.TButton").grid(row=3, column=0, pady=5)
        ttk.Button(main_frame, text="Cập nhật", command=self.update_parking, style="Custom.TButton").grid(row=3, column=1, pady=5)
        ttk.Button(main_frame, text="Xóa", command=self.delete_parking, style="Custom.TButton").grid(row=3, column=2, pady=5)

        # Bảng danh sách
        self.tree = ttk.Treeview(main_frame, columns=("location", "status", "current_vehicles", "max_capacity"), show='headings', style="Treeview")
        self.tree.heading("location", text="Vị trí")
        self.tree.heading("status", text="Trạng thái")
        self.tree.heading("current_vehicles", text="Số xe hiện tại")
        self.tree.heading("max_capacity", text="Sức chứa")
        self.tree.column("location", width=150)
        self.tree.column("status", width=100)
        self.tree.column("current_vehicles", width=100)
        self.tree.column("max_capacity", width=100)
        self.tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.refresh_table()

    def validate_max_capacity(self, max_capacity):
        try:
            value = int(max_capacity)
            return value > 0
        except ValueError:
            return False

    def add_parking(self):
        try:
            location = self.entry_location.get().strip()
            max_capacity = self.entry_max_capacity.get().strip()
            status = self.status_var.get()

            if not all([location, max_capacity]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
                return
            if any(p.location == location for p in self.manager.items):
                messagebox.showerror("Lỗi", f"Vị trí {location} đã tồn tại.")
                return
            if not self.validate_max_capacity(max_capacity):
                messagebox.showerror("Lỗi", "Sức chứa phải là số nguyên dương.")
                return

            parking = ParkingLot(status=status, location=location, max_capacity=int(max_capacity))
            self.manager.add(parking)
            self.refresh_table()
            self.clear_entries()
            messagebox.showinfo("Thành công", "Thêm bãi đỗ thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def update_parking(self):
        try:
            location = self.entry_location.get().strip()
            max_capacity = self.entry_max_capacity.get().strip()
            status = self.status_var.get()

            if not all([location, max_capacity]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
                return
            if not self.validate_max_capacity(max_capacity):
                messagebox.showerror("Lỗi", "Sức chứa phải là số nguyên dương.")
                return

            parking = self.manager.get_by_id("location", location)
            if not parking:
                messagebox.showerror("Lỗi", f"Bãi đỗ tại {location} không tồn tại.")
                return

            if int(max_capacity) < len(parking.current_vehicles):
                messagebox.showerror("Lỗi", "Sức chứa mới không được nhỏ hơn số xe hiện tại.")
                return

            new_data = {
                "status": status,
                "location": location,
                "max_capacity": int(max_capacity),
                "current_vehicles": parking.current_vehicles
            }
            self.manager.update_by_id("location", location, new_data)
            self.refresh_table()
            self.clear_entries()
            messagebox.showinfo("Thành công", "Cập nhật bãi đỗ thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def delete_parking(self):
        try:
            location = self.entry_location.get().strip()
            if not location:
                messagebox.showerror("Lỗi", "Vui lòng chọn bãi đỗ để xóa.")
                return

            parking = self.manager.get_by_id("location", location)
            if not parking:
                messagebox.showerror("Lỗi", f"Bãi đỗ tại {location} không tồn tại.")
                return
            if parking.current_vehicles:
                messagebox.showerror("Lỗi", "Không thể xóa bãi đỗ đang chứa xe.")
                return

            if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa bãi đỗ tại {location}?"):
                return

            self.manager.delete_by_id("location", location)
            self.refresh_table()
            self.clear_entries()
            messagebox.showinfo("Thành công", "Xóa bãi đỗ thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def on_select(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values:
            self.entry_location.delete(0, tk.END)
            self.entry_location.insert(0, values[0])
            self.status_var.set(values[1])
            self.entry_max_capacity.delete(0, tk.END)
            self.entry_max_capacity.insert(0, values[3])

    def clear_entries(self):
        self.entry_location.delete(0, tk.END)
        self.entry_max_capacity.delete(0, tk.END)
        self.status_var.set("Còn chỗ")

    def refresh_table(self):
        self.manager.reload()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.manager.items:
            current_vehicles_count = len(p.current_vehicles)
            self.tree.insert("", "end", values=(p.location, p.status, current_vehicles_count, p.max_capacity))