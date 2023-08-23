from datetime import datetime, timezone
import json
from typing import Dict, Any

class JSONStructureLogMessage:
    def __init__(self, message: str, level: str = "NOTSET!!", **kwargs):
        self.data = {}
        self.message = message
        # self.data = kwargs
        self.datetime = datetime.now(tz=timezone.utc)
        self.timestamp = self.datetime.timestamp()
        self.data["level"] = level
        self.data["timestamp"] = self.timestamp
        self.data["message"] = self.message
        self.data["utcString"] = self.datetime.isoformat()
        # python 9 added the ability to do this: self.data = self.data | kwargs
        # TODO: feel like there is probably a faster way to combine these dict, or to handle this issue generally
        self.data["context"] =  kwargs

    def add_property(self, name: str, value: Any):
        self.data[name] = value

    def add_dict(self, data: Dict[str, Any]):
        self.data = {**self.data, **data}
        
    def __str__(self) -> str:
        return json.dumps(self.data)