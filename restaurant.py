class Restaurant:
    def __init__(self, name, address, specialty, coordinates):
        self.name = name
        self.address = address
        self.specialty = specialty
        self.coordinates = coordinates

    def __repr__(self):
        return f"Restaurant({self.name}, {self.address}, {self.specialty}, {self.coordinates})"
