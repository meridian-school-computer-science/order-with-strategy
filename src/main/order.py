from csv import DictReader


class DataReader:

    def __init__(self, target_order_list, source_file):
        self.source_file = source_file
        self.all_rows = []
        self.order_list = target_order_list
        self.read_from_csv()
        self.process_csv_to_order()

    def read_from_csv(self):
        with open(self.source_file) as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                self.all_rows.append(row)
                line_count += 1

    def process_csv_to_order(self):
        for i in self.all_rows:
            this_order = Order(i)
            self.order_list.add_order(this_order)


class AllOrders:

    def __init__(self):
        self.items = []

    def add_order(self, an_order):
        self.items.append(an_order)

    def show_orders(self):
        for each in self.items:
            print(each)


class Order:

    def __init__(self, one_order):
        self.ordered_data = one_order
        self.orderID = one_order['orderID']
        self.cost = one_order['cost']
        self.tax_status = one_order['tax status']
        self.gift_card = one_order['gift card']
        self.savings_code = one_order['savings code']
        self.shipping_mode = one_order['shipping mode']
        self.customer_name = one_order['customer name']
        self.street_address = one_order['street address']
        self.city = one_order['city']
        self.state = one_order['state']
        self.zip_code = one_order['zip code']
        self.order_status = one_order['order status']

    def __str__(self):
        return f"{self.orderID}: ${self.cost} status:{self.order_status}"


order_list = AllOrders()
d = DataReader(order_list, 'order data.csv')
order_list.show_orders()


