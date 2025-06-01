import tkinter as tk
from tkinter import ttk, messagebox
import re
from ticket import Ticket
from driver import Driver
from vehicle import Vehicle
from parking_lot import ParkingLot
from GenericManager import GenericManager
from datetime import datetime, timedelta

class TicketGUI:
    def __init__(self, master):
        self.ticket_manager = GenericManager('tickets.json', Ticket)
        self.driver_manager = GenericManager('drivers.json', Driver)
        self.vehicle_manager = GenericManager('vehicles.json', Vehicle)
        self.parking_manager = GenericManager('parkings.json', ParkingLot)
        self.master = master

        # Cấu hình style
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#87CEFA")
        style.configure("Custom.TLabel", background="#E6F0FA", foreground="#333333", font=("Arial", 10))
        style.configure("Custom.TButton", background="#4A90E2", foreground="#FFFFFF", padding=6, font=("Arial", 10, "bold"))
        style.map("Custom.TButton", background=[("active", "#357ABD")])
        style.configure("Custom.TEntry", fieldbackground="#FFFFFF", foreground="#333333")
        style.configure("Custom.TCombobox", fieldbackground="#FFFFFF", foreground="#333333")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", background="#DCE4F5", foreground="#333333", font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#B3D4FC")])

        main_frame = ttk.Frame(master, style="Custom.TFrame", padding=10)
        main_frame.pack(fill="both", expand=True)

        top_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        top_frame.pack(fill="x", pady=(0, 5))

        input_frame = ttk.LabelFrame(top_frame, text="Thông tin vé", padding=10, style="Custom.TFrame")
        input_frame.pack(side="left", fill="x", expand=True)

        labels = [
            "Biển số xe", "Tên tài xế", "Số điện thoại", "Tình trạng bằng lái",
            "Loại xe", "Loại vé", "Bãi đỗ", "Giá vé"
        ]
        self.entries = {}
        self.dropdowns = {}
        row = 0
        for label in labels:
            ttk.Label(input_frame, text=label, style="Custom.TLabel").grid(row=row, column=0, sticky='w', padx=5, pady=2)
            if label == "Tình trạng bằng lái":
                self.license_status_var = tk.StringVar(value="Còn hiệu lực")
                self.dropdowns['license_status'] = ttk.Combobox(
                    input_frame, textvariable=self.license_status_var,
                    values=["Còn hiệu lực", "Hết hạn", "Bị thu hồi"], state="readonly", style="Custom.TCombobox"
                )
                self.dropdowns['license_status'].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            elif label == "Loại xe":
                self.vehicle_type_var = tk.StringVar(value="Ô tô")
                self.dropdowns['vehicle_type'] = ttk.Combobox(
                    input_frame, textvariable=self.vehicle_type_var,
                    values=["Ô tô", "Xe máy", "Xe tải"], state="readonly", style="Custom.TCombobox"
                )
                self.dropdowns['vehicle_type'].grid(row=row, column=1, sticky='w', padx=5, pady=2)
                self.dropdowns['vehicle_type'].bind("<<ComboboxSelected>>", lambda event: self.update_price_label())
            elif label == "Loại vé":
                self.ticket_type_var = tk.StringVar(value="Vé ngày")
                self.dropdowns['ticket_type'] = ttk.Combobox(
                    input_frame, textvariable=self.ticket_type_var,
                    values=["Vé ngày", "Vé tháng"], state="readonly", style="Custom.TCombobox"
                )
                self.dropdowns['ticket_type'].grid(row=row, column=1, sticky='w', padx=5, pady=2)
                self.dropdowns['ticket_type'].bind("<<ComboboxSelected>>", lambda event: self.update_price_label())
            elif label == "Giá vé":
                self.price_label_var = tk.StringVar(value="50,000 VNĐ")
                self.entries['price'] = ttk.Label(input_frame, textvariable=self.price_label_var, style="Custom.TLabel")
                self.entries['price'].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            elif label == "Bãi đỗ":
                self.parking_var = tk.StringVar()
                self.dropdowns['parking'] = ttk.Combobox(
                    input_frame, textvariable=self.parking_var, state="readonly", style="Custom.TCombobox"
                )
                self.dropdowns['parking'].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            else:
                self.entries[label.lower().replace(" ", "_")] = ttk.Entry(input_frame, style="Custom.TEntry")
                self.entries[label.lower().replace(" ", "_")].grid(row=row, column=1, sticky='w', padx=5, pady=2)
            row += 1

        price_frame = ttk.LabelFrame(top_frame, text="Bảng giá vé", padding=10, style="Custom.TFrame")
        price_frame.pack(side="right", fill="y", padx=(10, 0))

        self.price_table = ttk.Treeview(
            price_frame,
            columns=("Loại vé", "Ô tô", "Xe máy", "Xe tải"),
            show="headings", style="Treeview", height=2
        )
        self.price_table.heading("Loại vé", text="Loại vé")
        self.price_table.heading("Ô tô", text="Ô tô")
        self.price_table.heading("Xe máy", text="Xe máy")
        self.price_table.heading("Xe tải", text="Xe tải")
        self.price_table.column("Loại vé", width=80, anchor="center")
        self.price_table.column("Ô tô", width=80, anchor="center")
        self.price_table.column("Xe máy", width=80, anchor="center")
        self.price_table.column("Xe tải", width=80, anchor="center")
        self.price_table.pack(fill="both", expand=True)

        price_data = {
            "Vé ngày": {"Ô tô": 50000, "Xe máy": 20000, "Xe tải": 100000},
            "Vé tháng": {"Ô tô": 1000000, "Xe máy": 400000, "Xe tải": 2000000}
        }
        for ticket_type, prices in price_data.items():
            self.price_table.insert("", "end", values=(
                ticket_type,
                f"{prices['Ô tô']:,} VNĐ",
                f"{prices['Xe máy']:,} VNĐ",
                f"{prices['Xe tải']:,} VNĐ"
            ))

        button_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        button_frame.pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Đặt vé", command=self.add_ticket, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hủy vé", command=self.cancel_ticket, style="Custom.TButton").pack(side="left", padx=5)

        self.tree = ttk.Treeview(
            main_frame,
            columns=("Mã vé", "ID tài xế", "ID xe", "Thời gian đến", "Thời gian đi", "Giá vé", "Loại vé", "Số điện thoại", "Tình trạng bằng", "Bãi đỗ", "Loại xe"),
            show="headings", style="Treeview"
        )
        self.tree.heading("Mã vé", text="Mã vé")
        self.tree.heading("ID tài xế", text="ID tài xế")
        self.tree.heading("ID xe", text="ID xe")
        self.tree.heading("Thời gian đến", text="Thời gian đến")
        self.tree.heading("Thời gian đi", text="Thời gian đi")
        self.tree.heading("Giá vé", text="Giá vé")
        self.tree.heading("Loại vé", text="Loại vé")
        self.tree.heading("Số điện thoại", text="Số điện thoại")
        self.tree.heading("Tình trạng bằng", text="Tình trạng bằng")
        self.tree.heading("Bãi đỗ", text="Bãi đỗ")
        self.tree.heading("Loại xe", text="Loại xe")
        self.tree.column("Mã vé", width=50, anchor="center")
        self.tree.column("ID tài xế", width=80, anchor="center")
        self.tree.column("ID xe", width=80, anchor="center")
        self.tree.column("Thời gian đến", width=120, anchor="center")
        self.tree.column("Thời gian đi", width=120, anchor="center")
        self.tree.column("Giá vé", width=80, anchor="center")
        self.tree.column("Loại vé", width=80, anchor="center")
        self.tree.column("Số điện thoại", width=100, anchor="center")
        self.tree.column("Tình trạng bằng", width=100, anchor="center")
        self.tree.column("Bãi đỗ", width=80, anchor="center")
        self.tree.column("Loại xe", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.refresh()
        self.update_price_label()

    def update_price_label(self, event=None):
        try:
            vehicle_type = self.vehicle_type_var.get()
            ticket_type = self.ticket_type_var.get()

            if not vehicle_type or not ticket_type:
                self.price_label_var.set("Chưa chọn loại xe/vé")
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

            if ticket_type not in price_table or vehicle_type not in price_table[ticket_type]:
                self.price_label_var.set("Loại xe/vé không hợp lệ")
                return

            price = price_table[ticket_type][vehicle_type]
            self.price_label_var.set(f"{price:,} VNĐ")
        except Exception as e:
            self.price_label_var.set("Lỗi hiển thị giá")
            messagebox.showerror("Lỗi", f"Lỗi hiển thị giá: {str(e)}")

    def generate_id(self, items, prefix):
        return f"{prefix}{len(items) + 1:03d}"

    def validate_inputs(self, license_plate, driver_name, phone, parking_location):
        if not all([license_plate, driver_name, phone, parking_location]):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return False
        # Kiểm tra định dạng số điện thoại
        if not re.match(r"^0\d{9}$", phone):
            messagebox.showerror("Lỗi", "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0.")
            return False
        # Kiểm tra bãi đỗ
        parking = next(
            (p for p in self.parking_manager.items if p.location == parking_location and p.status == "Còn chỗ"),
            None)
        if not parking:
            messagebox.showerror("Lỗi", "Bãi đỗ không tồn tại hoặc đã đầy.")
            return False
        # Kiểm tra định dạng biển số xe dựa trên loại xe
        vehicle_type = self.dropdowns['vehicle_type'].get()
        license_plate = license_plate.replace(" ", "").upper()

        if vehicle_type == "Xe máy":
            if not re.match(r"^\d{2}[A-Z]-?\d{5}$", license_plate):
                messagebox.showerror("Lỗi", "Biển số xe máy phải có định dạng XXA-12345 (VD: 29A-12345).")
                return False

        elif vehicle_type == "Ô tô":
            if not re.match(r"^\d{2}[A-Z]-?\d{4,5}$", license_plate):
                messagebox.showerror("Lỗi", "Biển số ô tô phải có định dạng XXA-1234 hoặc XXA-12345 (VD: 30A-12345).")
                return False

        elif vehicle_type == "Xe tải":
            if not re.match(r"^\d{2}[A-ZT]-?\d{4,5}$", license_plate):
                messagebox.showerror("Lỗi",
                                     "Biển số xe tải phải có định dạng XXA-12345 hoặc XXT-12345 (VD: 29C-12345).")
                return False

        return True

    def add_ticket(self):
        try:
            license_plate = self.entries['biển_số_xe'].get().strip()
            driver_name = self.entries['tên_tài_xế'].get().strip()
            phone = self.entries['số_điện_thoại'].get().strip()
            license_status = self.dropdowns['license_status'].get()
            vehicle_type = self.dropdowns['vehicle_type'].get()
            ticket_type = self.dropdowns['ticket_type'].get()
            parking_location = self.dropdowns['parking'].get()

            if not self.validate_inputs(license_plate, driver_name, phone, parking_location):
                return

            if not messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đặt vé này?"):
                return

            driver = next(
                (d for d in self.driver_manager.items if d.name.lower() == driver_name.lower() and d.phone == phone),
                None)
            if not driver:
                driver_id = self.generate_id(self.driver_manager.items, "D")
                driver = Driver(driver_id, driver_name, phone, license_status)
                self.driver_manager.add(driver)
            driver_id = driver.driver_id

            vehicle = next((v for v in self.vehicle_manager.items if v.license_plate.lower() == license_plate.lower()), None)
            if not vehicle:
                vehicle_id = self.generate_id(self.vehicle_manager.items, "V")
                vehicle = Vehicle(vehicle_id, license_plate, vehicle_type, "Hoạt động")
                self.vehicle_manager.add(vehicle)
            vehicle_id = vehicle.vehicle_id

            for ticket in self.ticket_manager.items:
                if ticket.vehicle_id == vehicle_id:
                    messagebox.showerror("Lỗi", f"Xe {license_plate} đã có vé đang hoạt động.")
                    return

            ticket_id = self.generate_id(self.ticket_manager.items, "T")
            arrival_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            arrival_datetime = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S")

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
            price = price_table[ticket_type][vehicle_type]

            if ticket_type == "Vé ngày":
                departure_time = (arrival_datetime + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
            else:
                departure_time = (arrival_datetime + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

            ticket = Ticket(
                ticket_id=ticket_id,
                driver_id=driver_id,
                vehicle_id=vehicle_id,
                arrival_time=arrival_time,
                departure_time=departure_time,
                price=price,
                ticket_type=ticket_type
            )
            self.ticket_manager.add(ticket)

            parking = next((p for p in self.parking_manager.items if p.location == parking_location), None)
            parking.add_vehicle(vehicle_id)
            self.parking_manager.save()

            self.refresh()
            self.clear_entries()
            messagebox.showinfo(
                "Thành công",
                f"Đặt vé thành công!\nMã vé: {ticket_id}\nID tài xế: {driver_id}\nID xe: {vehicle_id}\nThời gian đến: {arrival_time}\nThời gian đi: {departure_time}\nGiá: {price:,} VNĐ"
            )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def cancel_ticket(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showerror("Lỗi", "Vui lòng chọn một vé để hủy.")
                return

            values = self.tree.item(selected[0], 'values')
            if not values or len(values) < 3:
                messagebox.showerror("Lỗi", "Dữ liệu vé không hợp lệ.")
                return

            ticket_id = values[0]
            driver_id = values[1]
            vehicle_id = values[2]

            ticket = self.ticket_manager.get_by_id("ticket_id", ticket_id)
            if not ticket:
                messagebox.showerror("Lỗi", f"Vé {ticket_id} không tồn tại.")
                return

            if not messagebox.askyesno(
                "Xác nhận",
                f"Bạn có chắc chắn muốn hủy vé {ticket_id}? Tài xế {driver_id} và xe {vehicle_id} sẽ bị xóa."
            ):
                return

            for parking in self.parking_manager.items:
                if vehicle_id in parking.current_vehicles:
                    parking.remove_vehicle(vehicle_id)
                    break

            self.ticket_manager.delete_by_id("ticket_id", ticket_id)

            driver = self.driver_manager.get_by_id("driver_id", driver_id)
            if driver:
                self.driver_manager.delete_by_id("driver_id", driver_id)
            else:
                messagebox.showwarning("Cảnh báo", f"Tài xế {driver_id} không tồn tại.")

            vehicle = self.vehicle_manager.get_by_id("vehicle_id", vehicle_id)
            if vehicle:
                self.vehicle_manager.delete_by_id("vehicle_id", vehicle_id)
            else:
                messagebox.showwarning("Cảnh báo", f"Xe {vehicle_id} không tồn tại.")

            self.ticket_manager.save()
            self.parking_manager.save()
            self.driver_manager.save()
            self.vehicle_manager.save()

            self.refresh()
            self.clear_entries()
            messagebox.showinfo(
                "Thành công",
                f"Hủy vé {ticket_id} thành công! Tài xế {driver_id} và xe {vehicle_id} đã được xóa."
            )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi hủy vé: {str(e)}")

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], 'values')
        if values:
            ticket_id, driver_id, vehicle_id, arrival_time, departure_time, price, ticket_type, phone, license_status, parking, vehicle_type = values
            self.entries['biển_số_xe'].delete(0, tk.END)
            vehicle = self.vehicle_manager.get_by_id("vehicle_id", vehicle_id)
            self.entries['biển_số_xe'].insert(0, vehicle.license_plate if vehicle else "")
            self.entries['tên_tài_xế'].delete(0, tk.END)
            driver = self.driver_manager.get_by_id("driver_id", driver_id)
            self.entries['tên_tài_xế'].insert(0, driver.name if driver else "")
            self.entries['số_điện_thoại'].delete(0, tk.END)
            self.entries['số_điện_thoại'].insert(0, phone)
            self.dropdowns['license_status'].set(license_status)
            self.dropdowns['vehicle_type'].set(vehicle_type)
            self.dropdowns['ticket_type'].set(ticket_type)
            self.dropdowns['parking'].set(parking)
            self.update_price_label()

    def clear_entries(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
        self.dropdowns['license_status'].set("Còn hiệu lực")
        self.dropdowns['vehicle_type'].set("Ô tô")
        self.dropdowns['ticket_type'].set("Vé ngày")
        self.dropdowns['parking'].set("")
        self.update_price_label()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in self.ticket_manager.items:
            driver = self.driver_manager.get_by_id("driver_id", t.driver_id)
            vehicle = self.vehicle_manager.get_by_id("vehicle_id", t.vehicle_id)
            parking_location = ""
            for parking in self.parking_manager.items:
                if t.vehicle_id in parking.current_vehicles:
                    parking_location = parking.location
                    break
            phone = driver.phone if driver else ""
            license_status = driver.license_status if driver else ""
            vehicle_type = vehicle.vehicle_type if vehicle else ""
            self.tree.insert("", "end",
                             values=(t.ticket_id, t.driver_id, t.vehicle_id, t.arrival_time, t.departure_time,
                                     t.price, t.ticket_type, phone, license_status, parking_location, vehicle_type))

        available_parkings = [p.location for p in self.parking_manager.items if p.status == "Còn chỗ"]
        self.dropdowns['parking']['values'] = available_parkings
        if available_parkings:
            self.dropdowns['parking'].set(available_parkings[0])
        else:
            self.dropdowns['parking'].set("")
            self.dropdowns['parking']['values'] = []