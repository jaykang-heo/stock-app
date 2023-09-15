import csv


class StockFileManager:

    @staticmethod
    def get_stock_codes_from_csv(csv_path):
        """Extract stock codes from a CSV file."""
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            return [row['코드번호'][1:] for row in reader]  # Remove 'A' and return list directly
