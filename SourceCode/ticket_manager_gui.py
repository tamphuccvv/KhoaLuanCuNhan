import tkinter as tk
from tkinter import ttk, messagebox
import vehicle_gui
from ticket import Ticket
from driver import Driver
from vehicle import Vehicle
from parking_lot import ParkingLot
from GenericManager import GenericManager
from datetime import datetime, timedelta
import re

class TicketManagerGUI:
    def __init__(self, root):
        self.ticket_manager = GenericManager('tickets.json', Ticket)
        self.driver_manager = GenericManager('drivers.json', Driver)
        self.vehicle_manager = GenericManager('vehicles.json', Vehicle)
        self.parking_manager = GenericManager('parkings.json', ParkingLot)
        self.root = root

        # Tìm AdminGUI từ parent
        parent = self.root
        self.admin_gui = parent

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

        # Frame nhập liệu
        input_frame = ttk.LabelFrame(main_frame, text="Thông tin vé", padding=10, style="Custom.TFrame")
        input_frame.pack(side="left", fill="x", expand=True)

        # Các trường nhập liệu
        labels = [
            "Mã vé", "ID tài xế", "ID xe", "Thời gian đến",
            "Thời gian đi", "Loại vé", "Bãi đỗ", "Giá vé"
        ]
        self.entries = {}
        self.dropdowns = {}
        row = 0
        for label in labels:
            ttk.Label(input_frame, text=label, style="Custom.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
            if label == "Loại vé":
                self.ticket_type_var = tk.StringVar(value="Vé ngày")
                self.dropdowns['ticket_type'] = ttk.Combobox(
                    input_frame, textvariable=self.ticket_type_var,
                    values=["Vé ngày", "Vé tháng"], state="readonly", style="Custom.TCombobox"
                )
                self.dropdowns['ticket_type'].grid(row=row, column=1, sticky='w', padx=5, pady=2)
                self.dropdowns['ticket_type'].bind("<<ComboboxSelected>>", lambda event: self.update_price_label())
            elif label == "Bãi đỗ":
                self.parking_var = tk.StringVar()
                self.dropdowns['parking'] = ttk.Combobox(
                    input_frame, textvariable=self.parking_var, state="readonly", style="Custom.TCombobox"
                )
                self.dropdowns['parking'].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            elif label == "Giá vé":
                self.price_label_var = tk.StringVar(value="50,000 VNĐ")
                self.entries['price'] = ttk.Label(input_frame, textvariable=self.price_label_var, style="Custom.TLabel")
                self.entries['price'].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            else:
                self.entries[label.lower().replace(" ", "_")] = ttk.Entry(input_frame, style="Custom.TEntry")
                self.entries[label.lower().replace(" ", "_")].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            row += 1

        # Frame nút
        button_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        button_frame.pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Cập nhật", command=self.update_ticket, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_ticket, style="Custom.TButton").pack(side="left", padx=5)

        # Bảng danh sách vé
        self.tree = ttk.Treeview(
            main_frame,
            columns=("Mã vé", "ID tài xế", "ID xe", "Thời gian đến", "Thời gian đi", "Giá vé", "Loại vé", "Bãi đỗ"),
            show="headings", style="Treeview"
        )
        for col in ("Mã vé", "ID tài xế", "ID xe", "Thời gian đến", "Thời gian đi", "Giá vé", "Loại vé", "Bãi đỗ"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Thanh cuộn
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.refresh()

    def update_price_label(self, event=None):
        try:
            vehicle_id = self.entries['id_xe'].get().strip()
            ticket_type = self.ticket_type_var.get()

            vehicle = self.vehicle_manager.get_by_id("vehicle_id", vehicle_id)
            if not vehicle:
                self.price_label_var.set("Xe không tồn tại")
                return

            price_table = {
                "Vé ngày": {
                    "Ô tô": 50000,
                    "Xe máy": 20000,
                    "Xe tải": 100000
                },
                "Vé tháng": {
                    "Ô tô": 1000000,
                    "Xe máy": 400000,
                    "Xe tải": 2000000
                }
            }

            if ticket_type not in price_table or vehicle.vehicle_type not in price_table[ticket_type]:
                self.price_label_var.set("Loại vé/xe không hợp lệ")
                return

            price = price_table[ticket_type][vehicle.vehicle_type]
            self.price_label_var.set(f"{price:,} VNĐ")
        except Exception as e:
            self.price_label_var.set("Lỗi hiển thị giá")
            messagebox.showerror("Lỗi", f"Lỗi hiển thị giá: {str(e)}")

    def validate_inputs(self, ticket_id, driver_id, vehicle_id, arrival_time, departure_time, parking_location):
        if not all([ticket_id, driver_id, vehicle_id, arrival_time, departure_time, parking_location]):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return False

        try:
            datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S")
            datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng thời gian không hợp lệ (YYYY-MM-DD HH:MM:SS).")
            return False

        driver = self.driver_manager.get_by_id("driver_id", driver_id)
        if not driver:
            messagebox.showerror("Lỗi", f"Tài xế {driver_id} không tồn tại.")
            return False

        vehicle = self.vehicle_manager.get_by_id("vehicle_id", vehicle_id)
        if not vehicle:
            messagebox.showerror("Lỗi", f"Xe {vehicle_id} không tồn tại.")
            return False

        parking = next((p for p in self.parking_manager.items if p.location == parking_location), None)
        if not parking or (vehicle_id not in parking.current_vehicles and parking.status == "Hết chỗ"):
            messagebox.showerror("Lỗi", "Bãi đỗ không tồn tại hoặc đã đầy.")
            return False

        return True

    def update_ticket(self):
        try:
            ticket_id = self.entries['mã_vé'].get().strip()
            driver_id = self.entries['id_tài_xế'].get().strip()
            vehicle_id = self.entries['id_xe'].get().strip()
            arrival_time = self.entries['thời_gian_đến'].get().strip()
            departure_time = self.entries['thời_gian_đi'].get().strip()
            ticket_type = self.ticket_type_var.get()
            parking_location = self.dropdowns['parking'].get()

            if not self.validate_inputs(ticket_id, driver_id, vehicle_id, arrival_time, departure_time, parking_location):
                return

            ticket = self.ticket_manager.get_by_id("ticket_id", ticket_id)
            if not ticket:
                messagebox.showerror("Lỗi", f"Vé {ticket_id} không tồn tại.")
                return

            vehicle = self.vehicle_manager.get_by_id("vehicle_id", vehicle_id)
            price_table = {
                "Vé ngày": {
                    "Ô tô": 50000,
                    "Xe máy": 20000,
                    "Xe tải": 100000
                },
                "Vé tháng": {
                    "Ô tô": 1000000,
                    "Xe máy": 400000,
                    "Xe tải": 2000000
                }
            }
            price = price_table[ticket_type][vehicle.vehicle_type]

            # Cập nhật bãi đỗ
            old_parking = next((p for p in self.parking_manager.items if ticket.vehicle_id in p.current_vehicles), None)
            new_parking = next((p for p in self.parking_manager.items if p.location == parking_location), None)
            if old_parking and old_parking.location != parking_location:
                old_parking.remove_vehicle(ticket.vehicle_id)
                new_parking.add_vehicle(vehicle_id)
                self.parking_manager.save()

            # Cập nhật thông tin vé
            new_data = {
                "driver_id": driver_id,
                "vehicle_id": vehicle_id,
                "arrival_time": arrival_time,
                "departure_time": departure_time,
                "price": price,
                "ticket_type": ticket_type
            }
            self.ticket_manager.update_by_id("ticket_id", ticket_id, new_data)
            self.refresh()
            self.clear_entries()
            messagebox.showinfo("Thành công", "Cập nhật vé thành công!")
            if self.admin_gui:
                self.admin_gui.refresh_all_tabs()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def delete_ticket(self):
        try:
            ticket_id = self.entries['mã_vé'].get().strip()
            if not ticket_id:
                messagebox.showerror("Lỗi", "Vui lòng chọn vé để xóa.")
                return

            ticket = self.ticket_manager.get_by_id("ticket_id", ticket_id)
            if not ticket:
                messagebox.showerror("Lỗi", f"Vé {ticket_id} không tồn tại.")
                return

            if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa vé {ticket_id}?"):
                return

            # Xóa xe khỏi bãi đỗ
            parking_updated = False
            for parking in self.parking_manager.items:
                if ticket.vehicle_id in parking.current_vehicles:
                    parking.remove_vehicle(ticket.vehicle_id)
                    parking_updated = True
                    break
            if not parking_updated:
                messagebox.showwarning("Cảnh báo", f"Xe {ticket.vehicle_id} không có trong bãi đỗ nào.")

            # Xóa vé
            self.ticket_manager.delete_by_id("ticket_id", ticket_id)

            # Kiểm tra và xóa tài xế nếu không có vé nào khác sử dụng
            driver_id = ticket.driver_id
            other_tickets_with_driver = any(t.driver_id == driver_id for t in self.ticket_manager.items)
            if not other_tickets_with_driver:
                driver = self.driver_manager.get_by_id("driver_id", driver_id)
                if driver:
                    self.driver_manager.delete_by_id("driver_id", driver_id)
                else:
                    messagebox.showwarning("Cảnh báo", f"Tài xế {driver_id} không tồn tại.")
            else:
                messagebox.showinfo("Thông báo", f"Tài xế {driver_id} vẫn được sử dụng bởi vé khác, không xóa.")

            # Kiểm tra và xóa xe nếu không có vé nào khác sử dụng
            vehicle_id = ticket.vehicle_id
            other_tickets_with_vehicle = any(t.vehicle_id == vehicle_id for t in self.ticket_manager.items)
            if not other_tickets_with_vehicle:
                vehicle = self.vehicle_manager.get_by_id("vehicle_id", vehicle_id)
                if vehicle:
                    self.vehicle_manager.delete_by_id("vehicle_id", vehicle_id)
                else:
                    messagebox.showwarning("Cảnh báo", f"Xe {vehicle_id} không tồn tại.")
            else:
                messagebox.showinfo("Thông báo", f"Xe {vehicle_id} vẫn được sử dụng bởi vé khác, không xóa.")

            # Lưu tất cả thay đổi
            self.ticket_manager.save()
            self.parking_manager.save()
            self.driver_manager.save()
            self.vehicle_manager.save()

            # Làm mới giao diện
            self.refresh()
            self.clear_entries()
            messagebox.showinfo("Thành công", f"Xóa vé {ticket_id} thành công!")
            if self.admin_gui:
                self.admin_gui.refresh_all_tabs()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa vé: {str(e)}")

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], 'values')
        if values:
            ticket_id, driver_id, vehicle_id, arrival_time, departure_time, price, ticket_type, parking = values
            self.entries['mã_vé'].delete(0, tk.END)
            self.entries['mã_vé'].insert(0, ticket_id)
            self.entries['id_tài_xế'].delete(0, tk.END)
            self.entries['id_tài_xế'].insert(0, driver_id)
            self.entries['id_xe'].delete(0, tk.END)
            self.entries['id_xe'].insert(0, vehicle_id)
            self.entries['thời_gian_đến'].delete(0, tk.END)
            self.entries['thời_gian_đến'].insert(0, arrival_time)
            self.entries['thời_gian_đi'].delete(0, tk.END)
            self.entries['thời_gian_đi'].insert(0, departure_time)
            self.dropdowns['ticket_type'].set(ticket_type)
            self.dropdowns['parking'].set(parking)
            self.update_price_label()

    def clear_entries(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
        self.dropdowns['ticket_type'].set("Vé ngày")
        self.dropdowns['parking'].set("")
        self.price_label_var.set("50,000 VNĐ")

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in self.ticket_manager.items:
            parking_location = ""
            for parking in self.parking_manager.items:
                if t.vehicle_id in parking.current_vehicles:
                    parking_location = parking.location
                    break
            self.tree.insert("", "end",
                             values=(t.ticket_id, t.driver_id, t.vehicle_id, t.arrival_time, t.departure_time,
                                    f"{t.price:,} VNĐ", t.ticket_type, parking_location))

        available_parkings = [p.location for p in self.parking_manager.items if p.status == "Còn chỗ"]
        self.dropdowns['parking']['values'] = available_parkings
        if available_parkings:
            self.dropdowns['parking'].set(available_parkings[0])
        else:
            self.dropdowns['parking'].set("")
            self.dropdowns['parking']['values'] = []