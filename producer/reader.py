import csv


class CSVReader:
    def __init__(self, path: str):
        self.path = path

    def read_csv(self):
        """
        Documentation
        """
        with open(self.path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row