import csv
import json


class Counter:
    @staticmethod
    def get_count_image():
        with open("revork_file/counter/counter.json", "r", encoding='utf-8') as file:
            counter_json = json.load(file)
        print(counter_json)
        count_image = counter_json['count_image']
        counter_json['count_image'] = count_image + 1

        with open("revork_file/counter/counter.json", "w", encoding='utf-8') as file:
            json.dump(counter_json, file, indent=3)
        return str(count_image).zfill(2)

    @staticmethod
    def get_count_doc():
        with open("revork_file/counter/counter.json", "r", encoding='utf-8') as file:
            counter_json = json.load(file)
        print(counter_json)
        count_doc = counter_json['count_doc']
        counter_json['count_doc'] = count_doc + 1

        with open("revork_file/counter/counter.json", "w", encoding='utf-8') as file:
            json.dump(counter_json, file, indent=3)
        return str(count_doc).zfill(2)

