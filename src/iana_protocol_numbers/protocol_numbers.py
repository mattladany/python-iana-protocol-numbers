import requests
import csv
from io import StringIO

class IANAProtocolNumbers:

    NUMBER_COLUMN = 0
    KEYWORD_COLUMN = 1
    PROTOCOL_COLUMN = 2
    IPv6_EXTENSION_HEADER_COLUMN = 3
    REFERENCE_COLUMN = 4

    protocol_numbers = []

    def __init__(self, load_local: bool = False):
        if load_local:
            self.load_local()
        else:
            self.fetch_latest()

    def number_to_keyword(self, num: int) -> str:
        for proto in self.protocol_numbers:
            if int(proto[self.NUMBER_COLUMN]) == num:
                return proto[self.KEYWORD_COLUMN]
        return None

    def keyword_to_number(self, keyword: str) -> int:
        for proto in self.protocol_numbers:
            if proto[self.KEYWORD_COLUMN] == keyword:
                return int(proto[self.NUMBER_COLUMN])
        return -1

    def load_local(self):
        with open("data/protocol-numbers-1.csv", "r") as f:
            csv_content = f.read()
            self.protocol_numbers = self.parse_csv(StringIO(csv_content))

    def fetch_latest(self, url: str = "https://www.iana.org/assignments/protocol-numbers/protocol-numbers-1.csv", timeout: int = 5000):
        try:
            response = requests.get(url, timeout=timeout/1000)
            response.raise_for_status()
            
            self.protocol_numbers = self.parse_csv(StringIO(response.text))

        except requests.RequestException as e:
            raise Exception(f"Failed to fetch protocol numbers: {str(e)}")

    def parse_csv(self, csv_content: str):
        reader = csv.reader(csv_content)
        
        next(reader)
        
        csv_as_array = []
        for row in reader:
            if len(row) >= 5:
                try:
                    int(row[self.NUMBER_COLUMN])
                    csv_as_array.append([
                        int(row[self.NUMBER_COLUMN]),
                        row[self.KEYWORD_COLUMN],
                        row[self.PROTOCOL_COLUMN],
                        row[self.IPv6_EXTENSION_HEADER_COLUMN],
                        row[self.REFERENCE_COLUMN]
                    ])
                except ValueError:
                    range_values = row[self.NUMBER_COLUMN].split("-")
                    for i in range(int(range_values[0]), int(range_values[1]) + 1):
                        csv_as_array.append([
                            i,
                            row[self.KEYWORD_COLUMN],
                            row[self.PROTOCOL_COLUMN],
                            row[self.IPv6_EXTENSION_HEADER_COLUMN],
                            row[self.REFERENCE_COLUMN]
                        ])
        return csv_as_array
