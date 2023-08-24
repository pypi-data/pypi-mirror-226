from dataclasses import dataclass
from . import models

@dataclass
class Remap:
    data: dict
    def init(self, path: list[models.RemapData]):
        for item in path:
            value = self.get(item.from_path)
            tmp = self.get(item.to_path)
            if not value or not tmp:
                continue
            if isinstance(value, dict):
                for v_key, v_value in value.items():
                    tmp[v_key] = v_value
            else:
                tmp[item.from_path.get_last() if not item.new_name else item.new_name] = value
            self.data = x if (x:= self.remove(item.from_path)) else self.data
        return self.data
            
    def get(self, path: models.RemapUrl):
        arr = path.to_array()
        if len(arr) == 1 and arr[0] == "":
            return self.data
        tmp = self.data
        for url in arr:
            if tmp and url in tmp:
                tmp = tmp[url]
            else:
                return None
        return tmp
    def remove(self, path: models.RemapUrl):
        first = True
        while True:
            last = path.get_last()
            if last == "":
                break
            parent = path.remove_last()
            if len(parent.to_array()) == 0:
                break
            data = self.get(parent)
            if not data or last not in data:
                return None
            if isinstance(data[last], dict) and not first:
                if len(data[last].keys()) > 0:
                    return self.data
                else:
                    del data[last]
            else:
                del data[last]
            first = False
        return self.data
    def set(self, data: dict):
        self.data = data
        return self