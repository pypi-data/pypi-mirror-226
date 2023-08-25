# coding: utf-8
from enum import Enum


class WebIdType(Enum):
    Full = 'Full'
    IDOnly = 'IDOnly'
    PathOnly = 'PathOnly'
    LocalIDOnly = 'LocalIDOnly'
    DefaultIDOnly = 'DefaultIDOnly'
