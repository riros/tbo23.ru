"""Auto-generated file, do not edit by hand. LU metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_LU = PhoneMetadata(id='LU', country_code=352, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[24-9]\\d{3,10}|3(?:[0-46-9]\\d{2,9}|5[013-9]\\d{1,8})', possible_length=(4, 5, 6, 7, 8, 9, 10, 11)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:2[2-9]\\d{2,9}|(?:[3457]\\d{2}|8(?:0[2-9]|[13-9]\\d)|9(?:0[89]|[2-579]\\d))\\d{1,8})', example_number='27123456', possible_length=(4, 5, 6, 7, 8, 9, 10, 11)),
    mobile=PhoneNumberDesc(national_number_pattern='6[25-79][18]\\d{6}', example_number='628123456', possible_length=(9,)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{5}', example_number='80012345', possible_length=(8,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='90[015]\\d{5}', example_number='90012345', possible_length=(8,)),
    shared_cost=PhoneNumberDesc(national_number_pattern='801\\d{5}', example_number='80112345', possible_length=(8,)),
    personal_number=PhoneNumberDesc(national_number_pattern='70\\d{6}', example_number='70123456', possible_length=(8,)),
    voip=PhoneNumberDesc(national_number_pattern='20(?:1\\d{5}|[2-689]\\d{1,7})', example_number='20201234', possible_length=(4, 5, 6, 7, 8, 9, 10)),
    national_prefix_for_parsing='(15(?:0[06]|1[12]|35|4[04]|55|6[26]|77|88|99)\\d)',
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{3})', format='\\1 \\2', leading_digits_pattern=['[2-5]|7[1-9]|[89](?:[1-9]|0[2-9])'], domestic_carrier_code_formatting_rule='$CC \\1'),
        NumberFormat(pattern='(\\d{2})(\\d{2})(\\d{2})', format='\\1 \\2 \\3', leading_digits_pattern=['[2-5]|7[1-9]|[89](?:[1-9]|0[2-9])'], domestic_carrier_code_formatting_rule='$CC \\1'),
        NumberFormat(pattern='(\\d{2})(\\d{2})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['20'], domestic_carrier_code_formatting_rule='$CC \\1'),
        NumberFormat(pattern='(\\d{2})(\\d{2})(\\d{2})(\\d{1,2})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['2(?:[0367]|4[3-8])'], domestic_carrier_code_formatting_rule='$CC \\1'),
        NumberFormat(pattern='(\\d{2})(\\d{2})(\\d{2})(\\d{3})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['20'], domestic_carrier_code_formatting_rule='$CC \\1'),
        NumberFormat(pattern='(\\d{2})(\\d{2})(\\d{2})(\\d{2})(\\d{1,2})', format='\\1 \\2 \\3 \\4 \\5', leading_digits_pattern=['2(?:[0367]|4[3-8])'], domestic_carrier_code_formatting_rule='$CC \\1'),
        NumberFormat(pattern='(\\d{2})(\\d{2})(\\d{2})(\\d{1,4})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['2(?:[12589]|4[12])|[3-5]|7[1-9]|8(?:[1-9]|0[2-9])|9(?:[1-9]|0[2-46-9])'], domestic_carrier_code_formatting_rule='$CC \\1'),
        NumberFormat(pattern='(\\d{3})(\\d{2})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['70|80[01]|90[015]'], domestic_carrier_code_formatting_rule='$CC \\1'),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['6'], domestic_carrier_code_formatting_rule='$CC \\1')],
    mobile_number_portable_region=True)