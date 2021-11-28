from typing import Optional, Any, Dict
import abc

class Option(metaclass=abc.ABCMeta):
    '''Abstract type for config option.'''

    def __init__(self, readable_name: str, value: Any, typeStr:str):
        '''
        Constructor of option.
        
        Parameters:
        readable_name: Human readable name.
        value: Value of option
        typeStr: Type of option in string
        '''

        self._readable_name:str = readable_name
        self._value = value
        self.type:str = typeStr
    
    @abc.abstractclassmethod
    def load_json(self, json) -> None:
        '''Abstract method which loads from json necessary information.'''

        pass

    def to_json(self) -> Dict[str, Any]:
        '''Convert option to json'''

        prop = dict()
        prop['readable_name'] = self.human_readable_name
        prop['value'] = str(self._value)
        prop['type'] = self.type
        return prop
    
    @property
    def human_readable_name(self) ->str:
        return self._readable_name

    @property
    def value(self)->Any:
        return self._value
    
    @value.setter
    def value(self, val)->None:
        if self._validate_value(val):
            self._value = val
        else:
            raise RuntimeError("Incompatible value or value type!")
        
    def _validate_value(self, value)->bool:
        '''Helper method which will be used to check if value can be set'''
        return type(self._value) == type(value)

class IntOption(Option):
    '''Option which can holds integer type with optional value range.'''

    def __init__(self, readable_name:str, value:int, minimum:Optional[int]=None, maximum:Optional[int]=None):
        '''
        Construct int option.
        
        Parameters:
        readable_name: Human readable name.
        value: Value of option
        minimum: Optional minimum value
        maximum: Optional maximum value
        '''

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

    def _validate_value(self, value):
        valid_type = super()._validate_value(value) 
        in_range = True     
        if self._min is not None:
            in_range = in_range and int(self._min) <= value
        if self._max is not None:
            in_range = in_range and int(self._max) >= value
        return valid_type and in_range

class FloatOption(Option):
    '''
        Construct float option.
        
        Parameters:
        readable_name: Human readable name.
        value: Value of option
        minimum: Optional minimum value
        maximum: Optional maximum value
    '''
        
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

    def _validate_value(self, value):
        valid_type = super()._validate_value(value) 
        in_range = True
        if self._min is not None:
            in_range = in_range and int(self._min) <= value
        if self._max is not None:
            in_range = in_range and int(self._max) >= value
        return valid_type and in_range

class StringOption(Option):
    '''
        Construct string option.
        
        Parameters:
        readable_name: Human readable name.
        value: Value of option
        minimum: Optional minimum value
        maximum: Optional maximum value
    '''
    
    def __init__(self, readable_name:str, value:str):
        super().__init__(readable_name, value, "STRING")

    def to_json(self):
        prop = super().to_json()
        return prop
    
    def load_json(self, json):
        self._value = json['value']

class BooleanOption(Option):
    '''
        Construct bool option.
        
        Parameters:
        readable_name: Human readable name.
        value: Value of option
        minimum: Optional minimum value
        maximum: Optional maximum value
    '''
        
    def __init__(self, readable_name:str, value:bool):
        super().__init__(readable_name, value, "BOOLEAN")

    def to_json(self):
        prop = super().to_json()
        return prop
    
    def load_json(self, json):
        self._value = bool(json['value'])
