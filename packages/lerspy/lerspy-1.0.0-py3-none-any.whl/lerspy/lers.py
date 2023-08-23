"""
Open-source and maintened at:
https://github.com/IAmNotIsaac/python-lers/tree/main
"""


from types import FunctionType as _FunctionType
from typing import Any as _Any, Self as _Self, TypeVar as _TypeVar


__all__ = ['evar', 'Enum']

_T = _TypeVar('_T')


class evar:
    def __init__(self, *args, **kwargs) -> None:
        self.ordered_attrs = args
        self.attrs = kwargs


class _EnumVariantConstructor:
    def __init__(self, attrs: dict, ordered_attrs: tuple, variant_name: str, variant_index: int, enum_name: str, enum_attrs: dict) -> None:
        self.attrs = attrs
        self.ordered_attrs = ordered_attrs
        self.variant_name = variant_name
        self.variant_index = variant_index
        self.enum_name = enum_name
        self.enum_attrs = enum_attrs

    def __call__(self, *args: _Any, **kwargs: _Any) -> '_EnumVariant':
        attrs = {}
        ordered_attrs = []
        
        # ensure correct number of *args
        n_ordered_attrs = len(self.ordered_attrs)
        n_args = len(args)
        if n_ordered_attrs != n_args:
            raise TypeError(f'Expected {n_ordered_attrs} ordered argument(s), got {n_args}')
        
        # ensure correct number of **kwargs
        n_attrs = len(self.attrs)
        n_args = len(kwargs)
        if n_attrs != len(kwargs):
            raise TypeError(f'Expected {n_attrs} keyword argument(s), got {n_args}.')

        # consider *args and ordered attrs
        i = 0
        for arg_value in args:
            expected_type = self.ordered_attrs[i]
            if not isinstance(arg_value, expected_type):
                raise TypeError(f'Expected type {expected_type}, got type {type(arg_value).__name__} ({repr(arg_value)}).')
            ordered_attrs.append(arg_value)
            i += 1
        
        # consider **kwargs and attrs
        for arg_name, arg_value in kwargs.items():
            if arg_name not in self.attrs:
                raise AttributeError(f"Non-existent '{arg_name}' on {self.type.__name__}.")
            expected_type = self.attrs[arg_name]
            if not isinstance(arg_value, expected_type):
                raise TypeError(f'{self.variant_name}.{arg_name} expected type {expected_type.__name__}, got type {type(arg_value).__name__} ({repr(arg_value)}).')
            attrs[arg_name] = arg_value
        
        # consider functions
        funcs = {}

        for attr_name, attr_value in self.enum_attrs.items():
            if isinstance(attr_value, _FunctionType):
                funcs[attr_name] = attr_value

        # generate enum variant
        variant_instance = type(self.variant_name, (_EnumVariant,), attrs | funcs)()
        variant_instance.__enumname__ = self.enum_name
        variant_instance.__name__ = self.variant_name
        variant_instance.__attrkeys__ = attrs.keys()
        variant_instance.__orderedattrs__ = ordered_attrs
        variant_instance.__index__ = self.variant_index

        return variant_instance
    
    def __repr__(self) -> str:
        return f'<constructor of {self.enum_name}.{self.variant_name}>'
    
    def __getitem__(self, i: int) -> str:
        if not isinstance(i, int):
            raise TypeError(f'Expected index to be type int, got type {type(i).__name__}.')
        raise TypeError(f"'_EnumVariantConstructor' object is not subscriptable. Did you mean to index an instance? `{self.enum_name}.{self.variant_name}(...)[{int}]`.")


class _EnumVariant:
    def __repr__(self) -> str:
        default_name = f"{self.__enumname__}.{self.__name__}"
        if self.__attrkeys__ or self.__orderedattrs__:
            oattrs = [str(v) for v in self.__orderedattrs__]
            attrs = [f"{k}={getattr(self, k)}" for k in self.__attrkeys__]
            return f"{default_name}({', '.join(oattrs+attrs)})"
        return default_name

    def __eq__(self, other: _Self | _EnumVariantConstructor) -> bool:
        if isinstance(other, _EnumVariant):
            if self.__index__ != other.__index__:
                return False
            
            a = self._attr_keys_and_values()
            b = other._attr_keys_and_values()

            return a == b
        
        elif isinstance(other, _EnumVariantConstructor):
            return self.__index__ == other.variant_index
        
        return False

    def _attr_keys_and_values(self) -> dict:
        attrs = {}

        for k in self.__attrkeys__:
            attrs[k] = getattr(self, k, None)
        
        return attrs

    def __getitem__(self, i: int) -> _Any:
        if isinstance(i, slice):
            raise TypeError(f'slicing is not supported. To slice ordered attributes, access {self.__name__}().__orderedattrs__.')
        
        if not isinstance(i, int):
            raise TypeError(f'Expected index to be type int, got type {type(i).__name__}.')

        if i >= (l := len(self.__orderedattrs__)):
            raise IndexError(f'{self.__name__}()[{i}] >= {l}; Index out of range.')
        if i < (l := -len(self.__orderedattrs__)):
            raise IndexError(f'{self.__name__}()[{i}] < {l}; Index out of range.')
        
        return self.__orderedattrs__[i]
    
    def __setitem__(self, i: int, value: _T) -> None:
        if not isinstance(i, int):
            raise TypeError(f'Expected index to be type int, got type {type(i).__name__}.')

        if i >= (l := len(self.__orderedattrs__)):
            raise IndexError(f'{self.__name__}()[{i}] >= {l}; Index out of range.')        
        if i < (l := -len(self.__orderedattrs__)):
            raise IndexError(f'{self.__name__}()[{i}] < {l}; Index out of range.')

        expected_type = type(self.__orderedattrs__[i])
        if not isinstance(value, expected_type):
            raise TypeError(f'Expected assignment to be type {expected_type.__name__}, got type {type(value).__name__} ({repr(value)}).')

        self.__orderedattrs__[i] = value

    def __hash__(self) -> int:
        # TODO
        return 0


class _EnumMeta(type):
    def __new__(metacls, cls: str, bases: tuple, classdict: dict) -> _Self:
        enum_class = super().__new__(metacls, cls, bases, classdict)

        attrs = enum_class.__dict__.copy()
        
        # The purpose of this bit of code is to create the constructors for the variants.
        # What happens behind the scenes, is either an evar, dict, or tuple is taken
        # as a placeholder and for defining the types of attributes to which an enum
        # variant will be privy to. It then replaces that placeholder with the
        # constructor with all its configurations. A placeholder must be used instead
        # of writing the constructor directly in order to reduce the amount of imformation
        # passed on the user's end.
        variant_index = 0
        for attr_name, val in attrs.items():
            # Detect evar
            if isinstance(val, evar):
                constructor = _EnumVariantConstructor(val.attrs, val.ordered_attrs, attr_name, variant_index, cls, attrs)
                setattr(enum_class, attr_name, constructor)
                variant_index += 1
            
            # Detect dict (equivalent to evar with **kwargs only)
            elif isinstance(val, dict):
                constructor = _EnumVariantConstructor(val, (), attr_name, variant_index, cls, attrs)
                setattr(enum_class, attr_name, constructor)
                variant_index += 1

            # Detect tuple (equivalent to evar with *args only)
            elif isinstance(val, tuple):
                constructor = _EnumVariantConstructor({}, val, attr_name, variant_index, cls, attrs)
                setattr(enum_class, attr_name, constructor)
                variant_index += 1
        
        return enum_class


class Enum(metaclass=_EnumMeta):
    pass


class Example(Enum):
    VA = evar()

print(type(Example.VA()))

# print(Example.VariantA(60, name="Steve")[0:1])

# print(Example.VariantA(0, name="bob", surname="ball").test())


# print(Example.VariantA())
# print(Example.VariantB(1))

# print(Example.VariantB(1) == Example.VariantB(1))
# print(Example.VariantB(1) == Example.VariantB(2))


"""
An enum may have its variants constructed in various ways:

```
class Example(Enum):
    # Evar method, named properties
    Foo = evar(
        a=int,
        b=str
    )

    # Evar method, ordered properties
    Bar = evar(int, str)

    # Evar method, mixed properties
    Baz = evar(
        int, str,
        a=int,
        b=str
    )

    # Dict method, named properties
    Dict = {
        "c": int,
        "d": str
    }

    # Tuple method, ordered properties
    Tuple = (int, str)
```
"""