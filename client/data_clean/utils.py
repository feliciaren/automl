'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-12 15:30:05
@LastEditors: feliciaren
@LastEditTime: 2020-05-12 20:24:30
'''
from client.data_clean.config import *

import datetime
import random
import re


class Utils(object):

    @staticmethod
    def is_all_digits(x):
        return x.isdigit()

    @staticmethod
    def check_type(x):
        if x == 'None' or x == 'nan' or x == "":
            return NAN
        elif Utils.is_all_digits(x):
            return INTEGRAL
        else:
            try:
                float(x)
                return DOUBLE
            except ValueError:
                return STRING

    @staticmethod
    def random_generate_date(start_year, end_year):
        start_time = datetime.datetime.now().replace(year=start_year)
        diff_day = random.random() * (end_year - start_year + 1) * 365
        end_time = start_time + datetime.timedelta(days=diff_day)
        return end_time.date()

    @staticmethod
    def random_generate_timestamp(start_year, end_year):
        start_time = datetime.datetime.now().replace(year=start_year)
        diff_day = random.random() * (end_year - start_year + 1) * 365
        end_time = start_time + datetime.timedelta(days=diff_day)
        return end_time

    @staticmethod
    def numerical_string_to_double(label):
        if label is None:
            return float('NaN')
        if type(label) in [int, float]:
            return float(label)
        elif type(label) == str:
            if label not in ["", "None", "NULL", "null", "none", "NaN", "Nan", "nan"]:
                return float(label)
            else:
                return float("NaN")
        else:
            raise Exception("can not support ", label, " type")

    @staticmethod
    def boolean_to_double(label):
        if label is None:
            return 2.0
        if type(label) == bool:
            return 1.0 if label else 0.0
        elif type(label) == float:
            return label
        else:
            raise Exception("can not support ", label, " type")

    @staticmethod
    def is_long_or_int(label):
        if type(label) == float:
            return True if (label - int(label)) < 1e-10 else False
        else:
            raise Exception("The value type is error")

    @staticmethod
    def string_missing_value_completion(input_str):
        if input_str is None or input_str == "" or input_str == "NULL":
            return "None"
        else:
            return input_str

    @staticmethod
    def to_str(input_str):
        if input_str is None:
            return ""
        elif type(input_str) in [datetime.datetime, datetime.date]:
            return input_str.strftime("%Y-%m-%d %H:%M:%S")
        elif type(input_str) == str:
            return input_str
        else:
            return str(input_str)

    @staticmethod
    def date_to_age(birthday):
        now = datetime.datetime.now()
        if birthday is None:
            return float("NaN")
        else:
            if type(birthday) in [datetime.datetime, datetime.date]:
                inner_age = now.year - birthday.year
                if (now.month - birthday.month) < 0:
                    inner_age -= 1.0
                else:
                    inner_age -= 0.0
            elif type(birthday) == str:
                birth_date = datetime.datetime.strptime(birthday, "%Y-%m-%d")
                inner_age = now.year - birth_date.year
                if (now.month - birth_date.month) < 0:
                    inner_age -= 1.0
                else:
                    inner_age -= 0.0
            else:
                raise Exception("only support Date and String type")
            return inner_age
            
def re_title(title):
    rstr = r"[\=\(\)\,\/\\\:\*\.\?\"\<\>\|\' ']"  # '= ( ) ， / \ : * ? " < > |  '   还有空格
    new_title = re.sub(rstr, "_", title)
    return new_title



