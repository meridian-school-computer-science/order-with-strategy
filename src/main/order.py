from csv import DictReader, DictWriter


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


class DataWriter:

    def __init__(self, source_order_list, target_file):
        self.target_file = target_file
        self.all_rows = []
        self.order_list = source_order_list
        self.build_ordered_dicts()

    def write_to_csv(self):
        with open(self.target_file, 'w', newline='') as csv_file:
            field_names = ['orderID',
                           'cost',
                           'tax status',
                           'gift card',
                           'savings code',
                           'shipping mode',
                           'customer name',
                           'street address',
                           'city',
                           'state',
                           'zip code',
                           'order status',
                           'final cost']
            csv_writer = DictWriter(csv_file, fieldnames=field_names)
            csv_writer.writeheader()
            for a_row in self.all_rows:
                csv_writer.writerow(a_row)

    def build_ordered_dicts(self):
        for each_order in self.order_list.items:
            self.all_rows.append(each_order.get_ordered_dict())


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
        self.cost = float(one_order['cost'])
        self.tax_status = one_order['tax status']
        self.gift_card = float(one_order['gift card'])
        self.savings_code = one_order['savings code']
        self.shipping_mode = one_order['shipping mode']
        self.customer_name = one_order['customer name']
        self.street_address = one_order['street address']
        self.city = one_order['city']
        self.state = one_order['state']
        self.zip_code = one_order['zip code']
        self.order_status = one_order['order status']
        self.final_cost = self.cost

    def __str__(self):
        return f"{self.orderID}: ${self.cost:.2f}=> ${self.final_cost:.2f} /{self.tax_status}/{self.savings_code}/ status:{self.order_status}"

    def get_ordered_dict(self):
        return {'orderID': self.orderID,
                'cost': f"{self.cost:.2f}",
                'tax status': self.tax_status,
                'gift card': f"{self.gift_card:.2f}",
                'savings code': self.savings_code,
                'shipping mode': self.shipping_mode,
                'customer name': self.customer_name,
                'street address': self.street_address,
                'city': self.city,
                'state': self.state,
                'zip code': self.zip_code,
                'order status': self.order_status,
                'final cost': f"{self.final_cost:.2f}"}



class ProcessAllOrders:

    def __init__(self, order_list, strategies):
        self.order_list = order_list
        self.strategies = strategies

    def execute_process(self):
        for each_order in self.order_list:
            if each_order.order_status == 'pending final cost':
                processor = ProcessOneOrder(each_order,
                                            self.strategies[each_order.tax_status],
                                            self.strategies[each_order.shipping_mode],
                                            self.strategies[each_order.savings_code])
                processor.update_order()


class ProcessOneOrder:

    def __init__(self, an_order, tax, shipping, savings):
        self.order = an_order
        self.tax_processing = tax
        self.shipping = shipping
        self.savings = savings

    def update_order(self):
        # Apply Savings Code
        self.order.savings_code = self.savings.get_updated_text()
        self.order.final_cost = self.order.final_cost * self.savings.get_updated_amount()

        # Tax Processing
        self.order.tax_status = self.tax_processing.get_updated_text()
        self.order.final_cost = self.order.final_cost * self.tax_processing.get_updated_amount()

        # Apply any gift card
        self.apply_gift_card()

        # Add Shipping Cost (after tax)
        self.order.final_cost += self.shipping.get_shipping_cost()

        # Set Order Status
        self.order.order_status = 'ready for billing'

    def apply_gift_card(self):
        if self.order.gift_card > self.order.final_cost:
            self.order.final_cost = 0.0
        else:
            self.order.final_cost -= self.order.gift_card


class SavingsCode:

    def __init__(self, text, amount):
        self.text = text
        self.amount = amount

    def get_updated_text(self):
        return self.text

    def get_updated_amount(self):
        return (100 - self.amount)/100


class Meridian(SavingsCode):

    def __init__(self, amount):
        super().__init__('MERIDIAN applied', amount)


class Liberty(SavingsCode):

    def __init__(self, amount):
        super().__init__('LIBERTY applied', amount)


class Veteran(SavingsCode):

    def __init__(self, amount):
        super().__init__('VETERAN applied', amount)


class YouTube(SavingsCode):

    def __init__(self, amount):
        super().__init__('YOUTUBE applied', amount)


class Arnhem(SavingsCode):

    def __init__(self, amount):
        super().__init__('ARNHEM applied', amount)


class SmithJ(SavingsCode):

    def __init__(self, amount):
        super().__init__('SMITHJ applied', amount)


class NoCode(SavingsCode):

    def __init__(self):
        super().__init__('No Code', 0)


class Tax:

    def __init__(self, text, amount):
        self.text = text
        self.amount = amount

    def get_updated_text(self):
        return f"{self.text}"

    def get_updated_amount(self):
        return self.amount


class FullTax(Tax):

    def __init__(self):
        super().__init__('Tax Charged', 1.08)


class TaxFreeFed(Tax):

    def __init__(self):
        super().__init__('No Tax: Federal', 1.00)


class TaxFreeState(Tax):

    def __init__(self):
        super().__init__('No Tax: State', 1.00)


class Shipping:

    def __init__(self, amount):
        self.amount = amount

    def get_shipping_cost(self):
        return self.amount


class UspsGround(Shipping):

    def __init__(self):
        super().__init__(9.91)


class UspsPriority(Shipping):

    def __init__(self):
        super().__init__(19.25)


class Ups(Shipping):

    def __init__(self):
        super().__init__(10.91)


class FedEx(Shipping):

    def __init__(self):
        super().__init__(45.00)


# setup Shipping Strategies
usps_ground = UspsGround()
usps_priority = UspsPriority()
ups = Ups()
fedex = FedEx()


# setup Tax Strategies (first strategies built here)
full_tax = FullTax()
no_tax_fed = TaxFreeFed()
no_tax_state = TaxFreeState()

# setup Savings Codes (last strategies built)
veteran_5 = Veteran(5)
veteran_10 = Veteran(10)
veteran_15 = Veteran(15)
youtube_5 = YouTube(5)
youtube_10 = YouTube(10)
youtube_15 = YouTube(15)
meridian_5 = Meridian(5)
meridian_10 = Meridian(10)
meridian_15 = Meridian(15)
liberty_5 = Liberty(5)
liberty_10 = Liberty(10)
liberty_15 = Liberty(15)
smithj_5 = SmithJ(5)
smithj_10 = SmithJ(10)
smithj_15 = SmithJ(15)
arnhem_5 = Arnhem(5)
arnhem_10 = Arnhem(10)
arnhem_15 = Arnhem(15)
no_code = NoCode()


# build order_list of order objects from a CSV
order_list = AllOrders()
d = DataReader(order_list, 'order data.csv')

# process all orders
all_strategies = {'tax': full_tax,
                  'tax free Fed': no_tax_fed,
                  'tax free State': no_tax_state,
                  'USPS Ground': usps_ground,
                  'USPS Priority': usps_priority,
                  'UPS': ups,
                  'FedEx': fedex,
                  'VETERAN5': veteran_5,
                  'VETERAN10': veteran_10,
                  'VETERAN15': veteran_15,
                  'YOUTUBE5': youtube_5,
                  'YOUTUBE10': youtube_10,
                  'YOUTUBE15': youtube_15,
                  'MERIDIAN5': meridian_5,
                  'MERIDIAN10': meridian_10,
                  'MERIDIAN15': meridian_15,
                  'LIBERTY5': liberty_5,
                  'LIBERTY10': liberty_10,
                  'LIBERTY15': liberty_15,
                  'SMITHJ5': smithj_5,
                  'SMITHJ10': smithj_10,
                  'SMITHJ15': smithj_15,
                  'ARNHEM5': arnhem_5,
                  'ARNHEM10': arnhem_10,
                  'ARNHEM15': arnhem_15,
                  '': no_code}

master_processor = ProcessAllOrders(order_list.items, all_strategies)
master_processor.execute_process()

# produce output CSV file
output_writer = DataWriter(order_list, 'processed order list.csv')
output_writer.write_to_csv()

# print for testing updates
#order_list.show_orders()


