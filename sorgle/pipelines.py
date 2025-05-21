# pipelines.py

from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter, CsvItemExporter
import os


class ProfessorPipeline:
    """
    A flexible pipeline to clean, normalize, and export any items.
    Output filenames are based on the spider name.
    """

    def open_spider(self, spider):
        # Create output directory if it doesn't exist
        os.makedirs('data', exist_ok=True)

        # Determine output file paths based on spider name
        json_path = f"data/{spider.name}.json"
        csv_path = f"data/{spider.name}.csv"

        # Open file handles for JSON and CSV output
        self.json_file = open(json_path, 'wb')
        self.csv_file = open(csv_path, 'wb')

        # Initialize exporters
        self.json_exporter = JsonItemExporter(
            self.json_file, encoding='utf-8', ensure_ascii=False
        )
        self.csv_exporter = CsvItemExporter(self.csv_file)

        # Start exporting
        self.json_exporter.start_exporting()
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 1. Validation: Ensure item is not empty
        if not adapter or not dict(adapter):
            raise DropItem(f"Empty item: {item}")

        # 2. Cleaning: Strip whitespace from string fields and lists
        for field, value in adapter.items():
            if isinstance(value, list):
                adapter[field] = [v.strip() for v in value if isinstance(v, str) and v.strip()]
            elif isinstance(value, str):
                adapter[field] = value.strip()

        # 3. Normalization: lowercase emails if field name includes 'email'
        for field in adapter.field_names():
            if 'email' in field.lower() and isinstance(adapter.get(field), str):
                adapter[field] = adapter[field].lower()

        # 4. Export the cleaned item
        self.json_exporter.export_item(dict(adapter))
        self.csv_exporter.export_item(dict(adapter))

        return item

    def close_spider(self, spider):
        # Finish exporting and close file handles
        self.json_exporter.finish_exporting()
        self.csv_exporter.finish_exporting()

        self.json_file.close()
        self.csv_file.close()
