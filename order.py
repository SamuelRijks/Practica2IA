class Order:
    def __init__(self, order_id, weight, restaurant, delivery_coords):
        self.order_id = order_id
        self.weight = weight
        self.restaurant = restaurant
        self.delivery_coords = delivery_coords

    def __repr__(self):
        return f"Order({self.order_id}, {self.weight}kg, {self.restaurant}, {self.delivery_coords})"
