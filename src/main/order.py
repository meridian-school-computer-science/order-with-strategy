from csv import DictReader


class DataReader:

    def __init__(self):
        self.source_file = ''
        self.all_rows = []

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


class Order:

    def __init__(self):
        pass


d = DataReader()
d.source_file = 'order data.csv'
d.read_from_csv()
print(d)

# orderID,cost,tax status,gift card,savings code,shipping mode,customer name,street address,city,state,zip code,order status
