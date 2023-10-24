import csv
from stock_analyzer import StockAnalyzer


class StockFileManager:

    @staticmethod
    def get_stock_codes_from_csv(csv_path):
        """Extract stock codes from a CSV file."""
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            return [row['코드번호'][1:] for row in reader]  # Remove 'A' and return list directly

    @staticmethod
    def get_stock_codes_from_txt(text_path: str):
        stock_codes = []
        with open(text_path, 'r', encoding='utf-8') as file:
            # Read lines from the file
            lines = file.readlines()

            # Loop over each line
            for line in lines:
                # Strip whitespace from the line
                stripped_line = line.strip()

                # Check if the stripped line is a digit
                if stripped_line.isdigit():
                    stock_code = stripped_line
                    if (StockAnalyzer.is_valid_stock_code(stock_code)):
                        if StockFileManager.validate_stock_code_by_ticker(stock_code, text_path):
                            stock_codes.append(stock_code)
        return stock_codes

    @staticmethod
    def validate_stock_code_by_ticker(ticker, text_path):
        name_df = StockAnalyzer.get_valid_stock_name(ticker)
        name = name_df if isinstance(name_df, str) else (name_df.iloc[0, 0] if not name_df.empty else None)

        if name is None:
            # Handle the case where name is None, e.g. return a default value, log an error, or raise an exception
            return False

        with open(text_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if name in line.strip():
                    return True

        return False
