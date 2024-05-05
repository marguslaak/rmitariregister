from typing import Any


class IDCodeCheckException(Exception):
    pass


def check_id_code(id_code: Any) -> True or IDCodeCheckException:
    """
    Check if given ID code is valid and return the result.
    :param id_code: Any
    :return: bool
    """
    try:
        id_code: str = str(id_code)
    except TypeError:
        raise IDCodeCheckException('%(id_code)s is malformed!')

    if not id_code.isdigit():
        raise IDCodeCheckException('%(id_code)s is not a digit!')
    if len(id_code) != 11:
        raise IDCodeCheckException('%(id_code)s must be 11 digits long!')

    gender_number: int = int(id_code[0:1])
    year_number: int = int(id_code[1:3])
    month_number: int = int(id_code[3:5])
    day_number: int = int(id_code[5:7])
    born_order: int = int(id_code[7:10])

    a: bool = check_gender_number(gender_number)
    b: bool = check_year_number_two_digits(year_number)
    c: bool = check_month_number(month_number)
    d: bool = check_day_number(check_year(gender_number, year_number), month_number, day_number)
    e: bool = check_born_order(born_order)
    f: bool = check_control_number(id_code)

    if a and b and c and d and e and f:
        return True
    else:
        raise IDCodeCheckException('%(id_code)s is invalid!')


def check_year(gender_number: int, year_number: int) -> int:
    """
    Make the 2 digit year_number variable into a full year date
    :param gender_number: int
    :param year_number: int
    :return: year_number
    """
    if gender_number == 1 or gender_number == 2:
        year_number += 1800
    elif gender_number == 3 or gender_number == 4:
        year_number += 1900
    elif gender_number == 5 or gender_number == 6:
        year_number += 2000
    return year_number


def check_gender_number(gender_number: int) -> bool:
    """
    Check if given value is correct for gender number in ID code
    :param gender_number: int
    :return: boolean
    """
    if gender_number in range(1, 7):
        return True

    return False


def check_year_number_two_digits(year_number: int) -> bool:
    """
    Check if given value is correct for year number in ID code
    :param year_number: int
    :return: boolean
    """
    if year_number in range(0, 100):
        return True

    return False


def check_month_number(month_number: int) -> bool:
    """
    Check if given value is correct for month number in ID code
    :param month_number: int
    :return: boolean
    """
    if month_number in range(1, 13):
        return True

    return False


def check_day_number(year_number: int, month_number: int, day_number: int) -> bool:
    """
    Check if given value is correct for day number in ID code
    :param year_number: int
    :param month_number: int
    :param day_number: int
    :return: boolean
    """
    day_limit = 0
    day_31 = (1, 3, 5, 7, 8, 10, 12)
    day_30 = (4, 6, 9, 11)

    if month_number in day_31:
        day_limit = 31
    elif month_number in day_30:
        day_limit = 30
    elif month_number == 2:
        if check_leap_year(year_number):
            day_limit = 29
        else:
            day_limit = 28

    if day_number <= day_limit:
        return True
    else:
        return False


def check_leap_year(year_number: int) -> bool:
    """
    Check if given year is a leap year
    :param year_number: int
    :return: boolean
    """
    if year_number % 400 == 0:
        return True
    elif year_number % 4 == 0 and year_number % 100 != 0:
        return True
    elif year_number % 4 == 0 and year_number % 100 == 0:
        return False
    elif year_number % 100 == 0:
        return False
    else:
        return False


def check_born_order(born_order: int) -> bool:
    """
    Check if given value is correct for born order number in ID code
    :param born_order: int
    :return: boolean
    """
    if born_order in range(0, 1000):
        return True

    return False


def check_control_number(id_code: str) -> bool:
    """
    Check if given value is correct for control number in ID code
    :param id_code: string
    :return: boolean
    """
    phase_1: str = "1234567891"
    phase_2: str = "3456789123"
    check_1: int = 0

    for i in range(0, 10):
        id_code_piece: str = id_code[i]
        step_1_piece: str = phase_1[i]
        check_1 += (int(id_code_piece) * int(step_1_piece))

    result: int = check_1 % 11

    if str(result) == id_code[10] and result != 10:
        return True
    else:
        if result == 10:
            check_2: int = 0

            for i in range(0, 10):
                id_code_piece: str = id_code[i]
                step_2_piece: str = phase_2[i]
                check_2 += (int(id_code_piece) * int(step_2_piece))

            result_2: int = check_2 % 11
        else:
            return False

        if str(result_2) == id_code[10] and result_2 != 10:
            return True
        else:
            if int(id_code[10]) == 0 and result_2 >= 10:
                return True
            else:
                if str(result_2) == 0:
                    return True
                else:
                    return False
