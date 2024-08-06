class EntryObject:

    def __init__(self, name: str, bytes: int, type: str) -> None:
        self.name = name
        self.bytesize = bytes
        self.type = type
        self.size_group = self.set_size_group(bytes)
        self.groupedsize = self.set_groupedsize(self.size_group)


    def get_name(self) -> str:
        return self.name
    
    def get_bytesize(self) -> int:
        return self.bytesize
    
    def get_type(self) -> str:
        return self.type
    
    def get_size_group(self) -> int:
        return self.size_group
    
    def get_groupedsize(self) -> int:
        return self.groupedsize

    def set_size_group(self, b: int):
        if b < 1024:
            return "B"
        if b >= 1024 and b < 1024 ** 2:
            return "KB"
        elif b >= 1024 ** 2 and b < 1024 ** 3:
            return "MB"
        else:
            return "GB"
    def set_groupedsize(self, size_group: str):
        if size_group == "KB":
            return round(self.bytesize / 1024, 2)
        elif size_group == "MB":
            return round(self.bytesize / (1024 ** 2), 2)
        elif size_group == "GB":
            return round(self.bytesize / (1024 ** 3), 2)
        else:
            return self.bytesize
