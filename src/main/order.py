from csv import DictReader


class DataReader:

    def __init__(self, target_order_list):
        self.source_file = ''
        self.all_rows = []
        self.order_list = target_order_list : AllOrders

    def read_from_csv(self):
        with open(self.source_file) as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                self.all_rows.append(row)
                line_count += 1

    def __str__(self):
        for i in self.all_rows:
            print(i)

    def process_csv_to_order(self):
        for i in self.all_rows:
            this_order = Order(i)
            self.order_list.add_order(this_order)



class AllOrders:

    def __init__(self):
        self.items = []

    def add_order(self, an_order : Order):
        self.items.append(an_order)

class Order:

    def __init__(self, ordered_data):
        self.ordered_data = ordered_data
        self.build_order()

    def build_order(self):



d = DataReader()
d.source_file = 'order data.csv'
d.read_from_csv()
print(d)

# orderID,cost,tax status,gift card,savings code,shipping mode,customer name,street address,city,state,zip code,order status
