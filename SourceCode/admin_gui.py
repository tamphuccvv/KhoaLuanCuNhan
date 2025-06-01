import tkinter as tk
from tkinter import ttk
from driver_gui import DriverGUI
from employee_gui import EmployeeGUI
from vehicle_gui import VehicleGUI
from ticket_manager_gui import TicketManagerGUI
from parking_manager_gui import ParkingManagerGUI
from user_manager_gui import UserGUI

class AdminGUI:
    def __init__(self, root, login_app):
        self.root = root
        self.login_app = login_app
        self.root.title("Giao diện Quản trị viên")
        self.gui_instances = {}  # Lưu trữ các instance của GUI

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, fill='both', expand=True)

        # Thêm tabs Và lưu trữ GUI instances
        self.add_tab("Quản lý tài xế", DriverGUI)
        self.add_tab("Quản lý nhân viên", EmployeeGUI)
        self.add_tab("Quản lý xe", VehicleGUI)
        self.add_tab("Quản lý vé", TicketManagerGUI)
        self.add_tab("Quản lý bãi đỗ", ParkingManagerGUI)
        self.add_tab("Quản lý người dùng", UserGUI)

        # Logout button
        tk.Button(root, text="Đăng xuất", command=self.logout).pack(pady=5)

    # Trong admin_gui.py
    def add_tab(self, title, gui_class):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        gui_instance = gui_class(frame)
        if title == "Quản lý vé":
            gui_instance.admin_gui = self  # Truyền instance AdminGUI
        self.gui_instances[title] = gui_instance

    def refresh_all_tabs(self):
        """Làm mới tất cả các tab"""
        for gui in self.gui_instances.values():
            if hasattr(gui, 'refresh_table'):
                gui.refresh_table()
            elif hasattr(gui, 'refresh'):
                gui.refresh()

    def logout(self):
        self.root.destroy()
        self.login_app.show()