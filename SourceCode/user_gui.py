import tkinter as tk
from tkinter import ttk, messagebox
from ticket_gui import TicketGUI
from login_gui import LoginApp
from parking_lot import ParkingLot
from GenericManager import GenericManager

class ParkingGUI:
    def __init__(self, root):
        self.parking_manager = GenericManager('parkings.json', ParkingLot)
        self.root = root

        # Cấu hình style
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#E6F0FA")
        style.configure("Custom.TLabel", background="#E6F0FA", foreground="#333333", font=("Arial", 10))
        style.configure("Custom.TButton", background="#4A90E2", foreground="#333333", padding=6, font=("Arial", 10, "bold"))
        style.map("Custom.TButton", background=[("active", "#357ABD")])
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", background="#DCE4F5", foreground="#333333", font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#B3D4FC")])

        # Frame chính
        main_frame = ttk.Frame(root, style="Custom.TFrame", padding=10)
        main_frame.pack(fill="both", expand=True)

        # Nút
        ttk.Button(main_frame, text="Làm mới", command=self.refresh, style="Custom.TButton").grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(main_frame, text="Hiển thị bãi còn trống", command=self.show_available_parkings, style="Custom.TButton").grid(row=0, column=1, padx=5, pady=5)

        # Bảng danh sách
        self.tree = ttk.Treeview(main_frame, columns=("location", "status", "current_vehicles", "max_capacity"), show='headings', style="Treeview")
        self.tree.heading("location", text="Vị trí")
        self.tree.heading("status", text="Trạng thái")
        self.tree.heading("current_vehicles", text="Số xe hiện tại")
        self.tree.heading("max_capacity", text="Sức chứa")
        self.tree.column("location", width=100)
        self.tree.column("status", width=100)
        self.tree.column("current_vehicles", width=100)
        self.tree.column("max_capacity", width=100)
        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        # Frame chi tiết
        self.detail_frame = ttk.LabelFrame(main_frame, text="Chi tiết bãi đỗ", style="Custom.TFrame")
        self.detail_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        self.detail_location = ttk.Label(self.detail_frame, text="Vị trí: Chưa chọn bãi đỗ", style="Custom.TLabel")
        self.detail_status = ttk.Label(self.detail_frame, text="Trạng thái: ", style="Custom.TLabel")
        self.detail_capacity = ttk.Label(self.detail_frame, text="Sức chứa: ", style="Custom.TLabel")
        self.detail_vehicles_count = ttk.Label(self.detail_frame, text="Số xe hiện tại: ", style="Custom.TLabel")
        self.detail_vehicles = ttk.Label(self.detail_frame, text="Danh sách xe: ", wraplength=400, style="Custom.TLabel")
        self.detail_location.grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.detail_status.grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.detail_capacity.grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.detail_vehicles_count.grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.detail_vehicles.grid(row=4, column=0, sticky='w', padx=5, pady=2)

        self.refresh()

    def refresh(self):
        self.parking_manager.reload()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.parking_manager.items:
            current_vehicles_count = len(p.current_vehicles)
            self.tree.insert("", "end", values=(p.location, p.status, current_vehicles_count, p.max_capacity))

    def show_available_parkings(self):
        self.parking_manager.reload()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.parking_manager.items:
            current_vehicles_count = len(p.current_vehicles)
            if p.status == "Còn chỗ":
                self.tree.insert("", "end", values=(p.location, p.status, current_vehicles_count, p.max_capacity))

    def on_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, 'values')
        if values:
            location = values[0]
            parking = next((p for p in self.parking_manager.items if p.location == location), None)
            if parking:
                vehicles = ", ".join(parking.current_vehicles) if parking.current_vehicles else "Không có xe"
                self.detail_location.config(text=f"Vị trí: {parking.location}")
                self.detail_status.config(text=f"Trạng thái: {parking.status}")
                self.detail_capacity.config(text=f"Sức chứa: {parking.max_capacity}")
                self.detail_vehicles_count.config(text=f"Số xe hiện tại: {len(parking.current_vehicles)}")
                self.detail_vehicles.config(text=f"Danh sách xe: {vehicles}")
            else:
                self.clear_details()

    def clear_details(self):
        self.detail_location.config(text="Vị trí: Chưa chọn bãi đỗ")
        self.detail_status.config(text="Trạng thái: ")
        self.detail_capacity.config(text="Sức chứa: ")
        self.detail_vehicles_count.config(text="Số xe hiện tại: ")
        self.detail_vehicles.config(text="Danh sách xe: ")

class UserMenuGUI:
    def __init__(self, root, login_app):
        self.root = root
        self.login_app = login_app
        self.root.title("Giao diện Người dùng")

        # Cấu hình style cho notebook
        style = ttk.Style()
        style.configure("Custom.TNotebook", background="#E6F0FA")
        style.configure("Custom.TNotebook.Tab", background="#DCE4F5", foreground="#000000", padding=[10, 5])
        style.map("Custom.TNotebook.Tab", background=[("selected", "#FFFFFF")], foreground=[("selected", "#000000")])

        self.notebook = ttk.Notebook(root, style="Custom.TNotebook")
        self.notebook.pack(padx=10, pady=10, fill='both', expand=True)

        self.add_tab("Đặt vé", TicketGUI)
        self.add_tab("Bãi đỗ", ParkingGUI)

        ttk.Button(root, text="Đăng xuất", command=self.logout, style="Custom.TButton").pack(pady=5)

    def add_tab(self, title, gui_class):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        gui_class(frame)

    def logout(self):
        self.root.destroy()
        self.login_app.show()