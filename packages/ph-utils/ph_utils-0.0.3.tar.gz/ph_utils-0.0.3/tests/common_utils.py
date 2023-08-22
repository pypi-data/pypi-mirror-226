from decimal import Decimal
from ph_utils.common_utils import is_empty, is_blank, random, json_dumps


def test_is_empty():
    print(is_empty())
    print(is_empty(None))
    print(is_empty(""))
    print(is_empty(" "))
    print(is_empty(" a "))


def test_is_blank():
    print(is_blank())
    print(is_blank(None))
    print(is_blank(""))
    print(is_blank(" "))
    print(is_blank(" a "))


def test_random():
    print(random())
    print(random(only_num=True))
    print(random(only_num=True, first_zero=False))


def test_json_dumps():
    print(json_dumps({"name": "中文", "price": Decimal("0.0001")}, format=True))


test_json_dumps()
