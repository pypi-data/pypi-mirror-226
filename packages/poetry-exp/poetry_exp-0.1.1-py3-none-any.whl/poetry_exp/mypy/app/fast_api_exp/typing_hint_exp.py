from typing import Union
from enum import Enum


def add(a: int, b: int) -> int:
    # Its just typing hint, still you can pass str/float,
    # and to access its corresponding method and params in IDE
    return a + b  # now if you type a. (will shows methods int object only)


def add2(a: Union[int, str], b: Union[int, str]) -> Union[int, str]:
    return a + b  # now if you type a. (will shows methods from str and int object)


class Gender(Enum):
    MALE = "M"
    FEMALE = "F"
    OTHERS = "O"


def print_gender(g: Union[Gender, str]):
    print(g)

    if g == Gender.MALE or g == Gender.MALE.value:
        print(f'its Male')
    elif g == Gender.FEMALE or g == Gender.FEMALE.value:
        print(f'its Female')
    else:
        print('its not Male or Female')


if __name__ == '__main__':
    print(add('a', 'b'))
    print(add(1, 2))
    print(add2('a', 'b'))
    print(add2(1, 2))

    print_gender(Gender.MALE)
    print_gender(Gender.FEMALE)
    print_gender('M')
    print_gender('F')
