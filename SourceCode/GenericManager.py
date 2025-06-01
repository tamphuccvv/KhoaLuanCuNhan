from data_handler import load_data, save_data

class GenericManager:
    def __init__(self, file_path, cls):
        self.file_path = file_path
        self.cls = cls
        self.items = self.load()

    def load(self):
        data = load_data(self.file_path)
        return [self.cls(**item) for item in data]

    def save(self):
        save_data([vars(item) for item in self.items], self.file_path)

    def add(self, item):
        self.items.append(item)
        self.save()

    def delete_by_id(self, id_field, id_value):
        self.items = [item for item in self.items if getattr(item, id_field) != id_value]
        self.save()

    def update_by_id(self, id_field, id_value, new_data):
        for item in self.items:
            if getattr(item, id_field) == id_value:
                for key, value in new_data.items():
                    setattr(item, key, value)
        self.save()

    def get_by_id(self, id_field, id_value):
        return next((item for item in self.items if getattr(item, id_field) == id_value), None)

    def reload(self):
        self.items = self.load()