from enum import Enum
import re


class VersionTokenType(Enum):
    SNAP = 10
    SNAPSHOT = 10
    M = 10
    EAP = 25
    PRE = 25
    PREVIEW = 25
    ALPHA = 30
    A = 30
    BETA = 40
    BETTA = 40
    B = 40
    RC = 50
    _WS = 60
    SP = 70
    REL = 80
    RELEASE = 80
    R = 80
    FINAL = 80
    _WORD = 90
    _DIGITS = 100
    BUNDLED = 666

    def __init__(self, priority):
        self.__my_priority = priority

    @staticmethod
    def lookup(string):
        if string is None:
            return VersionTokenType._WS

        string = string.strip()
        if not string:
            return VersionTokenType._WS

        for token_type in VersionTokenType.__members__.keys():
            if token_type[0] != '_' and token_type == string:
                return VersionTokenType[token_type]

        if bool(re.fullmatch('0+', string)):
            return VersionTokenType._WS

        if bool(re.fullmatch('\d+', string)):
            return VersionTokenType._DIGITS

        return VersionTokenType._WORD

    def get_priority(self):
        return self.__my_priority


def pad_with_nones(s1, s2):
    if len(s1) != len(s2):
        while len(s1) < len(s2):
            s1.append(None)

        while len(s1) > len(s2):
            s2.append(None)


def get_priority(string):
    return VersionTokenType.lookup(string).get_priority()


def compare_priorities(version1, version2):
    priority1 = VersionTokenType.lookup(version1).get_priority()
    priority2 = VersionTokenType.lookup(version2).get_priority()

    if priority1 == priority2:
        return 0
    elif priority1 > priority2:
        return 1
    else:
        return -1


def compare_objects(object1, object2):
    if type(object1) != type(object2):
        raise TypeError('Objects types are not equal.')

    if object1 == object2:
        return 0
    elif object1 > object2:
        return 1
    else:
        return -1


def compare(version1, version2):
    if version1 is None:
        return 0 if version2 is None else -1
    elif version2 is None:
        return 1

    version1 = version1.lower()
    version2 = version2.lower()

    s1 = re.split('[-.]', version1)
    s2 = re.split('[-.]', version2)

    pad_with_nones(s1, s2)

    for i in range(len(s1)):
        elem1 = s1[i]
        elem2 = s2[i]
        token1 = VersionTokenType.lookup(elem1)

        result = compare_priorities(elem1, elem2)
        print(result)

        if result != 0:
            return result
        elif token1 == VersionTokenType._WORD:
            result = compare_objects(elem1, elem2)
        elif token1 == VersionTokenType._DIGITS:
            result = compare_objects(int(elem1), int(elem2))

        if result != 0:
            return result

    return 0