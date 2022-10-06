DELIVERY_MAP_CONFIG = '../config/delivery_map.txt'
ORDER_BATCH_CONFIG = '../config/order_batch.txt'


class Order:
    def __init__(self, id, item_name, customer, order_date, city, delivery_date, delivery_type):
        self._id = id
        self._item_name = item_name
        self._customer = customer
        self._order_date = order_date
        self._city = city
        self._delivery_date = delivery_date
        self._delivery_type = delivery_type

    def __str__(self):
        return f'ID - {self.id}, Item Name - {self.item_name}, Order Date - {self.order_date}, Customer - {self.customer}, City - {self.city}, Delivery Date - {self.delivery_date}, Delivery Type - {self.delivery_type}'

    @property
    def id(self):
        return self._id

    @property
    def item_name(self):
        return self._item_name

    @property
    def order_date(self):
        return self._order_date

    @property
    def customer(self):
        return self._customer

    @property
    def city(self):
        return self._city

    @property
    def delivery_date(self):
        return self._delivery_date

    @property
    def delivery_type(self):
        return self._delivery_type

    def dispatch(self, delivery_route):
        print(f'Dispatching order {order}')
        delivery_route.process_order(self)


class OrderBatch:
    def __init__(self):
        self._order_batch = []

    def __str__(self):
        pass

    def read_config(self, order_batch_config):
        with open(order_batch_config, 'r') as obatch_file:
            obatch_lines = [obatch_line.rstrip() for obatch_line in obatch_file]

        for order_entry in obatch_lines:
            order_details = order_entry.split('-')
            order = Order(order_details[0], order_details[1], order_details[2], order_details[3], order_details[4],
                          order_details[5], order_details[6])

            self._order_batch.append(order)

    def get_orders(self):
        return self._order_batch


class DeliveryMap:
    def __init__(self):
        self._destinations_delivery_type = []
        self._delivery_map = {}

    def __str__(self):
        pass

    def read_config(self, delivery_map_config):
        with open(delivery_map_config, 'r') as dmap_file:
            dmap_lines = [dmap_line.rstrip() for dmap_line in dmap_file]

        # Store the delivery stages in the map with key as a tuple of destination and delivery type
        for line in dmap_lines:
            destination, delivery_type, stages = line.split(' ')
            self._destinations_delivery_type.append((destination, delivery_type))
            stages = stages.split(',')
            self._delivery_map[(destination, delivery_type)] = stages
        print(f'Destinations with delivery type options: {self._destinations_delivery_type}')

    def get_destinations_delivery_type(self):
        return self._destinations_delivery_type

    def routing_map(self):
        return self._delivery_map

    def get_stages(self, destination, delivery_type):
        return self._delivery_map[destination, delivery_type]


class DeliveryStage:
    def __init__(self, source, destination):
        self._source = source
        self._destination = destination
        self._next_stage = None

    @property
    def next_stage(self):
        return self._next_stage

    @next_stage.setter
    def next_stage(self, successor):
        self._next_stage = successor

    def process_order(self, order):
        pass


class TrainDispatch(DeliveryStage):
    def __init__(self, source, destination):
        super().__init__(source, destination)

    def __str__(self):
        return f'Train from {self._source} to {self._destination}'

    def process_order(self, order):
        print(f'Order {order.id} - Train Dispatch from {self._source} to {self._destination}')

        if self.next_stage:
            return self.next_stage.process_order(order)
        else:
            return None


class FlightDispatch(DeliveryStage):
    def __init__(self, source, destination):
        super().__init__(source, destination)

    def __str__(self):
        return f'Flight from {self._source} to {self._destination}'

    def process_order(self, order):
        print(f'Order {order.id} - Flight Dispatch from {self._source} to {self._destination}')

        if self.next_stage:
            return self.next_stage.process_order(order)
        else:
            return None


class TruckDispatch(DeliveryStage):
    def __init__(self, source, destination):
        super().__init__(source, destination)

    def __str__(self):
        return f'Truck from {self._source} to {self._destination}'

    def process_order(self, order):
        print(f'Order {order.id} - Truck Dispatch from {self._source} to {self._destination}')

        if self.next_stage:
            return self.next_stage.process_order(order)
        else:
            return None


class BoatDispatch(DeliveryStage):
    def __init__(self, source, destination):
        super().__init__(source, destination)

    def __str__(self):
        return f'Boat from {self._source} to {self._destination}'

    def process_order(self, order):
        print(f'Order {order.id} - Boat Dispatch from {self._source} to {self._destination}')

        if self.next_stage:
            return self.next_stage.process_order(order)
        else:
            return None


class ShipDispatch(DeliveryStage):
    def __init__(self, source, destination):
        super().__init__(source, destination)

    def __str__(self):
        return f'Ship from {self._source} to {self._destination}'

    def process_order(self, order):
        print(f'Order {order.id} - Ship Dispatch from {self._source} to {self._destination}')

        if self.next_stage:
            return self.next_stage.process_order(order)
        else:
            return None


class DeliveryRoute:
    def __init__(self, stage_list, destination, delivery_type):
        self._stage_list = stage_list
        self._destination = destination
        self._delivery_type = delivery_type

    def __str__(self):
        route = ','.join(str(stage) for stage in self._stage_list)
        return f'{self._delivery_type} Route to {self._destination}: {route}\n'

    def process_order(self, order):
        self._stage_list[0].process_order(order)


class DeliverySystem:
    def __init__(self):
        self.delivery_centers_delivery_type = []
        self.stage_routes = {}

    def populate_route(self, center, delivery_type, stages):
        stage_list = []
        for stage in stages:
            source, dispatch_method, destination = stage.split('-')
            if (dispatch_method == 'truck'):
                stage_list.append(TruckDispatch(source, destination))
            elif (dispatch_method == 'train'):
                stage_list.append(TrainDispatch(source, destination))
            elif (dispatch_method == 'flight'):
                stage_list.append(FlightDispatch(source, destination))
            elif (dispatch_method == 'boat'):
                stage_list.append(BoatDispatch(source, destination))
            elif (dispatch_method == 'ship'):
                stage_list.append(ShipDispatch(source, destination))

        for i in range(0, len(stage_list) - 1):
            stage_list[i].next_stage = stage_list[i + 1]

        # Below line used 'destination' variable instead of 'center' in V1. Practically both these variables would have the same value at
        # the end of for loop on stages, but ideally it should be the 'center' variable as that contains the final destination of the complete route.
        route = DeliveryRoute(stage_list, center, delivery_type)
        print(route)

        return route

    def configure(self, DELIVERY_MAP_CONFIG):
        delivery_map = DeliveryMap()
        delivery_map.read_config(DELIVERY_MAP_CONFIG)

        self.delivery_centers_delivery_type.extend(delivery_map.get_destinations_delivery_type())

        for (center, delivery_type) in self.delivery_centers_delivery_type:
            stages = delivery_map.get_stages(center, delivery_type)
            route = self.populate_route(center, delivery_type, stages)
            self.stage_routes[center, delivery_type] = route

    def get_route(self, destination, delivery_type):
        return self.stage_routes[destination, delivery_type]


# Client Context

delivery_system = DeliverySystem()
delivery_system.configure(DELIVERY_MAP_CONFIG)

order_batch = OrderBatch()
order_batch.read_config(ORDER_BATCH_CONFIG)

orders = order_batch.get_orders()

for order in orders:
    route = delivery_system.get_route(order.city, order.delivery_type)
    order.dispatch(route)
    print('\n')