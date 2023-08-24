from dataclasses import dataclass

@dataclass
class RemapUrl:
    url: str
    def add(self, url: str):
        self.url = f"{self.url}.{url}"
        return self
    def set(self, url: str):
        self.url = url
        return self
    def remove_last(self):
        self.url = ".".join(self.to_array()[:-1])
        return self
    def to_array(self):
        return self.url.split(".")
    def get_last(self):
        return self.to_array()[-1]
    def __str__(self):
        return f"{self.url}"
    
@dataclass
class RemapData:
    from_path: RemapUrl or str
    to_path: RemapUrl or str
    new_name: str or None = None
    def __str__(self) -> str:
        return f"{self.from_path} -> {self.to_path}"
    def __post_init__(self):
        if isinstance(self.from_path, str):
            self.from_path = RemapUrl(self.from_path)
        if isinstance(self.to_path, str):
            self.to_path = RemapUrl(self.to_path)