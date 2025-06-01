import tkinter as tk
from tkinter import ttk, messagebox
from vehicle import Vehicle
from GenericManager import GenericManager

class VehicleGUI:
    def __init__(self, root):
        self.manager = GenericManager('vehicles.json', Vehicle)
        self.root = root

        # Cấu hình style
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#E6F0FA")
        style.configure("Custom.TLabel", background="#E6F0FA", foreground="#333333", font=("Arial", 10))
        style.configure("Custom.TButton", background="#4A90E2", foreground="#333333", padding=6, font=("Arial", 10, "bold"))
        style.map("Custom.TButton", background=[("active", "#357ABD")])
        style.configure("Custom.TEntry", fieldbackground="#FFFFFF", foreground="#333333")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", background="#DCE4F5", foreground="#333333", font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#B3D4FC")])

        # Frame chính
        main_frame = ttk.Frame(root, style="Custom.TFrame", padding=10)
        main_frame.pack(fill="both", expand=True)

        # Form nhập liệu
        ttk.Label(main_frame, text="Mã xe", style="Custom.TLabel").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Biển số", style="Custom.TLabel").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Loại xe", style="Custom.TLabel").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(main_frame, text="Tình trạng", style="Custom.TLabel").grid(row=3, column=0, sticky='w', padx=5, pady=2)

        self.entry_id = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_plate = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_type = ttk.Entry(main_frame, style="Custom.TEntry")
        self.entry_status = ttk.Entry(main_frame, style="Custom.TEntry")

        self.entry_id.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        self.entry_plate.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        self.entry_type.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        self.entry_status.grid(row=3, column=1, sticky='w', padx=5, pady=2)

        # Nút điều khiển
        ttk.Button(main_frame, text="Thêm", command=self.add_vehicle, style="Custom.TButton").grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(main_frame, text="Cập nhật", command=self.update_vehicle, style="Custom.TButton").grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Xóa", command=self.delete_vehicle, style="Custom.TButton").grid(row=4, column=2, padx=5, pady=5)

        # Bảng danh sách
        self.tree = ttk.Treeview(
            main_frame, columns=("id", "plate", "type", "status"), show='headings', style="Treeview"
        )
        self.tree.heading("id", text="Mã xe")
        self.tree.heading("plate", text="Biển số")
        self.tree.heading("type", text="Loại xe")
        self.tree.heading("status", text="Tình trạng")
        self.tree.column("id", width=100)
        self.tree.column("plate", width=100)
        self.tree.column("type", width=100)
        self.tree.column("status", width=100)
        self.tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.refresh_table()

    def add_vehicle(self):
        vehicle = Vehicle(
            self.entry_id.get(),
            self.entry_plate.get(),
            self.entry_type.get(),
            self.entry_status.get()
        )
        self.manager.add(vehicle)
        self.refresh_table()

    def update_vehicle(self):
        vehicle_id = self.entry_id.get()
        new_data = {
            "license_plate": self.entry_plate.get(),
            "vehicle_type": self.entry_type.get(),
            "status": self.entry_status.get()
        }
        self.manager.update_by_id("vehicle_id", vehicle_id, new_data)
        self.refresh_table()

    def delete_vehicle(self):
        vehicle_id = self.entry_id.get()
        self.manager.delete_by_id("vehicle_id", vehicle_id)
        self.refresh_table()

    def on_select(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values:
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, values[0])
            self.entry_plate.delete(0, tk.END)
            self.entry_plate.insert(0, values[1])
            self.entry_type.delete(0, tk.END)
            self.entry_type.insert(0, values[2])
            self.entry_status.delete(0, tk.END)
            self.entry_status.insert(0, values[3])

    def refresh_table(self):
        self.manager.reload()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for v in self.manager.items:
            self.tree.insert("", "end", values=(v.vehicle_id, v.license_plate, v.vehicle_type, v.status))