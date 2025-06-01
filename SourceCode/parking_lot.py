class ParkingLot:
    def __init__(self, status, location, max_capacity, current_vehicles=None):
        self.status = status
        self.location = location
        self.max_capacity = max_capacity
        self.current_vehicles = current_vehicles if current_vehicles is not None else []

    def add_vehicle(self, vehicle_id):
        if len(self.current_vehicles) < self.max_capacity:
            self.current_vehicles.append(vehicle_id)
            self.update_status()
        else:
            raise Exception("Bãi đỗ đã đầy")

    def remove_vehicle(self, vehicle_id):
        if vehicle_id in self.current_vehicles:
            self.current_vehicles.remove(vehicle_id)
            self.update_status()

    def update_status(self):
        self.status = 'Còn chỗ' if len(self.current_vehicles) < self.max_capacity else 'Hết chỗ'