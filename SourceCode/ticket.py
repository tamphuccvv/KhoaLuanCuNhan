class Ticket:
    def __init__(self, ticket_id, driver_id, vehicle_id, arrival_time, departure_time, price, ticket_type):
        self.ticket_id = ticket_id
        self.driver_id = driver_id
        self.vehicle_id = vehicle_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.price = price
        self.ticket_type = ticket_type