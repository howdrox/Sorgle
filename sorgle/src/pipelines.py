# pipelines.py

from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter, CsvItemExporter


class ProfessorPipeline:
    """
    A pipeline to validate, clean, normalize, and export professor items.
    """

    def open_spider(self, spider):
        # Open file handles for JSON and CSV output
        self.json_file = open('data/professors.json', 'wb')
        self.csv_file = open('data/professors.csv', 'wb')

        # Initialize exporters for JSON and CSV
        self.json_exporter = JsonItemExporter(
            self.json_file, encoding='utf-8', ensure_ascii=False
        )
        self.csv_exporter = CsvItemExporter(self.csv_file)

        # Start exporting: write headers where applicable
        self.json_exporter.start_exporting()
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 1. Validation: Ensure that 'name' field exists
        name = adapter.get('name')
        if not name or not name.strip():
            raise DropItem(f"Missing or empty 'name' in item: {item}")

        # 2. Cleaning: Strip whitespace from string fields and lists
        for field in ['name', 'title', 'department', 'email', 'research_interests']:
            value = adapter.get(field)
            if isinstance(value, list):
                # Strip whitespace for each element in a list
                cleaned_list = [v.strip() for v in value if isinstance(v, str) and v.strip()]
                adapter[field] = cleaned_list
            elif isinstance(value, str):
                adapter[field] = value.strip()

        # 3. Normalization: Lowercase the email if present
        email = adapter.get('email')
        if email:
            adapter['email'] = email.lower()

        # 4. Export the cleaned item to both JSON and CSV
        self.json_exporter.export_item(dict(adapter))
        self.csv_exporter.export_item(dict(adapter))

        return item

    def close_spider(self, spider):
        # Finish exporting and close file handles
        self.json_exporter.finish_exporting()
        self.csv_exporter.finish_exporting()

        self.json_file.close()
        self.csv_file.close()
