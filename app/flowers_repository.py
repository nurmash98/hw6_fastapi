from attrs import define


@define
class Flower:
    name: str
    count: int
    cost: int
    id: int = 0


class FlowersRepository:
    flowers: list[Flower]

    def __init__(self):
        self.flowers = []

    # необходимые методы сюда
    def get_all(self):
        return self.flowers
    def get_flower_by_id(id):
        for flower in self.flowers:
            if flower.id == id:
                return flower
        return None
    
    def save(self, name, count, cost):
        id = len(self.flowers) + 1
        self.flowers.append(Flower(name = name, count = count, cost = cost, id = id))
    
    def get_flowers_by_cart(self, cart_ids):
        flowers = []
        for id in cart_ids:
            for flower in self.flowers:
                if int(id) == flower.id:
                    flowers.append(flower)

        return flowers
        
    # конец решения
