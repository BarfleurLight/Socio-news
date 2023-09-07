import csv
import json
import os, time
from pathlib import Path


COUNTER_JSON = Path("revork_file/counter/counter.json")


def check_date(func):
    def wrapper(extension, num=1):
        current_date = str(time.strftime("%Y%m%d", time.localtime()))
        with open(COUNTER_JSON, "r", encoding='utf-8') as file:
            counter_json = json.load(file)
        if counter_json['date'] != current_date:
            counter_json['date'] = current_date
            counter_json['image'] = 0
            counter_json['doc'] = 0
            counter_json['zip'] = 0

        with open(COUNTER_JSON, "w", encoding='utf-8') as file:
            json.dump(counter_json, file, indent=3)

        return func(extension, num)
    return wrapper


class Counter:
    def get_name(self, start_name=None):
        if start_name is None:
            return str(time.strftime("%Y%m%d", time.localtime())) + \
            self._get_count('image') + '.jpg'
        extension = start_name.split('.')[1]
        if extension in ('jpg', 'png', 'jpeg'):
            return str(time.strftime("%Y%m%d", time.localtime())) + \
            self._get_count('image') + '.jpg'
        if extension in ('zip', '7z'):
            return 'zip_' + self._get_count('zip') + '.' + extension
        return str(time.strftime("%Y%m%d", time.localtime())) + \
            self._get_count('doc') + '.' + extension

    @staticmethod
    @check_date
    def _get_count(extension, num=1):
        with open(COUNTER_JSON, "r", encoding='utf-8') as file:
            counter_json = json.load(file)

        count = counter_json[extension]
        counter_json[extension] = count + num

        with open(COUNTER_JSON, "w", encoding='utf-8') as file:
            json.dump(counter_json, file, indent=3)
        return str(count).zfill(2)

    def decrease_count(self, name):
        extension = name.split('.')[1]
        if extension in ('jpg', 'png', 'jpeg'):
            return self._get_count('image', -1)
        if extension in ('zip', '7z'):
            return self._get_count('image', -1)
        return self._get_count('doc', -1)

