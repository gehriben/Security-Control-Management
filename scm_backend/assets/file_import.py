import pandas as pd
import traceback
import math
import configparser

from .models import Asset
from .models import Assettype
from .web_crawler import WebCrawler
from properties.models import Property


SOFTWARE_ASSETS_FILE_PATH = "static/Software_Assets_Simplified.xlsx"
HARDWARE_ASSETS_FILE_PATH = "static/Hardware_Assets_Simplified.xlsx"
USED_COLUMNS_SOFTWARE = [
    "Application Name",
    "Family",
    "Requires License",
    "Category",
    "Platform",
    "GDPR Risk",
    "Manufacturer GDPR Compliant",
    "Manufacturer PS/SH Compliant",
    "Manufacturer DPD Compliant",
    "Part of Suite"
]

USED_COLUMNS_HARDWARE = [
    "Computer Name",
    "Operating System",
    "Server",
    "Laptop",
    "Cloud",
    "Virtual",
    "Hypervisor",
    "SPLA Server",
    "Terminal Server",
    "Part of Suite"
]

FILTERED_ROWS = {
    # 'Server': False
}

class FileImport():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')

        self.software_path = SOFTWARE_ASSETS_FILE_PATH
        self.hardware_path = HARDWARE_ASSETS_FILE_PATH
        self.web_crawler = WebCrawler()

    def do_import(self):
        self.import_file(self.software_path, "Application Name", "Software")
        self.import_file(self.hardware_path, "Computer Name", "Hardware")

    def import_file(self, path, name_column, assettype):
        # read by default 1st sheet of an excel file
        security_controls_excel = pd.read_excel(path)

        print("  --> Read of excel file complete adding assets to DB")
        
        count = 0
        for index, row in security_controls_excel.iterrows():
            if not self.filter_row(row):
                name = str(row[name_column])
                if assettype == "Software":
                    description = self.web_crawler.crawl_asset_description(name)
                else:
                    description = self.web_crawler.crawl_asset_description(row["Operating System"])
                category = Assettype.objects.filter(name=assettype)[0]
                property_list = self.create_property(row)

                asset = Asset.objects.create(name=name, description=description, assettype=category)
                asset.properties.add(*property_list)

                count += 1
                if count >= int(self.config["Import"]["max_assets"]) and not int(self.config["Import"]["max_assets"]) <= 0:
                    break
        
        print("--- Import of assets completed ---")
        return "SUCCESS"
    
    def create_property(self, row):
        property_list = list()
        for column_name, column_value in row.items():
            field_content = self.check_field_validity(column_name, column_value)
            if field_content:
                property_name = self.get_property_name(column_name, column_value)

                property = Property.objects.filter(name=property_name)
                if not property:
                    property = Property.objects.create(name=property_name, description=field_content, parent_property=None)
                else:
                    property = property[0]
                property_list.append(property)

        return property_list

    def filter_row(self, row):
        for filtered_column_name, filtered_column_value in FILTERED_ROWS.items():
            if filtered_column_name in row and row[filtered_column_name] == filtered_column_value:
                return True
        
        return False

    def check_field_validity(self, column_name, column_value):
        if not pd.isnull(column_value):
            if column_name in USED_COLUMNS_SOFTWARE or column_name in USED_COLUMNS_HARDWARE:
                if column_value == True:
                    return str(column_name)
                elif column_value == False:
                    return None

                return str(column_value)
            else:
                return None
    
    def get_property_name(self, column_name, column_value):
        if column_value == True:
            return column_name
        else:
            return column_name + "_" + column_value