from csv import DictReader, DictWriter

class DataHandler:
    def __init__(self, file_path, encoding='utf-8-sig', text_column='text', label_column='label'):
        self.file_path = file_path
        self.encoding = encoding
        self.text_column = text_column
        self.label_column = label_column
        self.texts = []
        self.labels = []

    def load_data(self):
        texts = []
        labels = []
        with open(self.file_path, 'r', encoding=self.encoding) as file:
            reader = DictReader(file)
            for row in reader:
                texts.append(row[self.text_column])
                labels.append(int(row[self.label_column]))
        self.texts = texts
        self.labels = labels

    def save_data(self):
        with open(self.file_path, 'r', encoding=self.encoding) as file:
            reader = DictReader(file)
            fieldnames = reader.fieldnames
            rows = list(reader)

        with open(self.file_path, 'w', encoding=self.encoding, newline='') as file:
            writer = DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for row in rows:
                row[self.text_column] = self.texts.pop(0)
                row[self.label_column] = self.labels.pop(0)
                writer.writerow(row)

def test():
    dh = DataHandler('test.csv')
    dh.load_data()
    print(dh.labels)
    dh.save_data()

if __name__ == "__main__":
    test()