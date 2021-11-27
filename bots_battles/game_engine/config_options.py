from typing import Optional
import abc

class Option(metaclass=abc.ABCMeta):
    def __init__(self, readable_name: str, value, typeStr:str):
        self._readable_name:str = readable_name
        self._value = value
        self.type:str = typeStr
    
    @abc.abstractclassmethod
    def load_json(self, json):
        pass

    def to_json(self):
        prop = dict()
        prop['readable_name'] = self.human_readable_name
        prop['value'] = str(self._value)
        prop['type'] = self.type
        return prop
    
    @property
    def human_readable_name(self):
        return self._readable_name

    @property
    def value(self):
        return self._value

class IntOption(Option):
    def __init__(self, readable_name:str, value:int, minimum:Optional[int]=None, maximum:Optional[int]=None):
        super().__init__(readable_name, value, "INTEGER")
        self._min = minimum
        self._max = maximum

    def to_json(self):
        prop = super().to_json()
        if self._min != None:
            prop['min'] = self._min
        if self._max != None:
            prop['max'] = self._max

        return prop
    
    def load_json(self, json):
        self._value = int(json['value'])
        

class FloatOption(Option):
    def __init__(self, readable_name:str, value:float, minimum:Optional[int]=None, maximum:Optional[int]=None):
        super().__init__(readable_name, value, "FLOAT")
        self._min = minimum
        self._max = maximum

    def to_json(self):
        prop = super().to_json()
        if self._min != None:
            prop['min'] = self._min[0]
        if self._max != None:
            prop['max'] = self._max[1]

        return prop

    def load_json(self, json):
        self._value = float(json['value'])


class StringOption(Option):
    def __init__(self, readable_name:str, value:str):
        super().__init__(readable_name, value, "STRING")

    def to_json(self):
        prop = super().to_json()
        return prop
    
    def load_json(self, json):
        self._value = json['value']

class BooleanOption(Option):
    def __init__(self, readable_name:str, value:bool):
        super().__init__(readable_name, value, "BOOLEAN")

    def to_json(self):
        prop = super().to_json()
        return prop
    
    def load_json(self, json):
        self._value = bool(json['value'])
