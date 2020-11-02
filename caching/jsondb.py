import json
import xml.etree.ElementTree as xml_tree


class ModelSerializer:

    def encode(self, any_object):
        with open("cache.json", "a") as file:
            json.dump(any_object, fp=file, default=lambda o: o.__dict__, sort_keys=True, indent=4)



        # def decode(file_name, path="/Users/trungtran/PycharmProjects/finance-core"):
        #     file_path = f"{path}/{file_name}"
        #     with open(file_path) as file:
        #         objects = json.load(file)
        #         print(objects)