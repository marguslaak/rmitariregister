from datetime import datetime
from typing import Optional, Dict, Any, List

import pandera as pa
from dateutil.parser import parse
from pandera import DataFrameSchema, Column

from metadata.id_code_check import check_id_code, IDCodeCheckException


def create_dataframe_schema_from_json(
        schema_dict: Optional[Dict[str, Dict[str, Any]]]
) -> Optional[DataFrameSchema]:
    if not schema_dict:
        return

    columns: Dict[str, Column] = {}

    # Define a mapping from JSON type strings to pandera dtypes
    dtype_mapping: Dict[str, pa.DataType] = {
        "int": pa.Int,
        "float": pa.Float,
        "string": pa.String,
        "datetime": pa.DateTime
    }

    for col_name, col_info in schema_dict.items():
        col_type: str = col_info['type']
        nullable: bool = col_info.get('nullable', False)
        unique: bool = col_info.get('unique', False)
        checks: List[pa.Check] = []

        if col_type in ['int', 'float'] and 'range' in col_info:
            col_range = col_info['range']
            min_val = col_range['min_val']
            max_val = col_range['max_val']
            checks.append(pa.Check.in_range(min_val, max_val))

        if col_type == 'string' and 'allowed' in col_info:
            allowed_values = col_info['allowed']
            checks.append(pa.Check.isin(allowed_values))

        if col_info.get('personal_code', False):
            checks.append(
                pa.Check(
                    check_fn=lambda code: validate_personal_code(code),
                    name='check_personal_code',
                    element_wise=True
                )
            )

        if col_info.get('business_code', False):
            checks.append(
                pa.Check(
                    check_fn=lambda code: validate_business_code(code),
                    name='check_business_code',
                    element_wise=True
                )
            )

        if col_info.get('business_code_or_personal_code', False):
            checks.append(
                pa.Check(
                    check_fn=lambda code: validate_business_code(code) or validate_personal_code(code),
                    name='check_personal_code_or_business_code',
                    element_wise=True
                )
            )

        if col_info.get('is_date', False):
            checks.append(pa.Check(check_fn=lambda inp: is_date(inp), name='check_is_date', element_wise=True))

        if col_info.get('compare_to', False):
            col_compare_to = col_info['compare_to']
            equals: bool = col_compare_to['equals']
            to: str = col_compare_to['to']

            checks.append(
                pa.Check(
                    check_fn=lambda inp: compare_to(inp, to, equals),
                    name=f'compare_to_{to}',
                    element_wise=True
                )
            )

        pandera_dtype: pa.DataType = dtype_mapping.get(col_type)

        if pandera_dtype is None:
            raise ValueError(f"Unsupported data type: {col_type}")

        columns[col_name] = Column(pandera_dtype, checks=checks, nullable=nullable, unique=unique)

    return DataFrameSchema(columns=columns, coerce=True)


def validate_personal_code(personal_code: Any) -> bool:
    """
    Validate that personal code conforms to EE personal code requirements

    :param personal_code: personal code
    :return: True if valid, else False
    """
    try:
        return check_id_code(id_code=personal_code)
    except IDCodeCheckException:
        return False


def validate_business_code(business_code: Any) -> bool:
    """
    Validate that business code conforms to EE business code requirements

    :param business_code: business code
    :return: True if valid, else False
    """
    if not business_code or business_code and len(str(business_code)) != 8:
        return False
    if not (isinstance(business_code, int) or isinstance(business_code, str) and business_code.isdigit()):
        return False

    # business_code_check_digit: str = str(business_code)[-1]  # TODO: Seems not to be applicable here!
    #
    # weights: List[int] = [7, 3, 1]
    # total: int = 0
    #
    # for index, digit in enumerate(reversed(str(business_code)[:-1])):
    #     weight_index: int = index % 3
    #     total += int(digit) * weights[weight_index]
    #
    # check_digit: int = -total % 10
    #
    # return business_code_check_digit == str(check_digit)
    return True


def is_date(inp: str) -> bool:
    """
    Validate that input is valid date(time), attempt to parse from ISO format and EE format

    :param inp: date string
    :return: True if date, else False
    """
    try:
        return bool(parse(inp))
    except ValueError:
        try:
            return bool(datetime.strptime(inp, '%d.%m.%Y'))
        except ValueError:
            return False
    except Exception as exc:  # noqa: broad-except
        return False


def compare_to(inp: Any, to: Any, equals: bool = False) -> bool:
    """
    Validate that inp can be compared to to (using a combination of equals and/or negate)

    :param inp: string to compare
    :param to: string to compare against
    :param equals: whether strings must equal or not
    :return: True if valid, else False
    """
    if equals:
        return str(inp) == str(to)
    else:
        return str(inp) != str(to)
