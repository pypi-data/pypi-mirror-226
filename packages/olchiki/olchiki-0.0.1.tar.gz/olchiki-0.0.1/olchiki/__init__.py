# -*- coding: utf-8 -*-
import datetime

olchiki_number = ['᱐', '᱑','᱒', '᱓','᱔',
                 '᱕','᱖', '᱗', '᱘', '᱙']

english_number = ['0', '1', '2', '3', '4',
                  '5', '6', '7', '8', '9']

greg_equivalent_olchiki_months = ["ᱢᱟᱜᱽ", "ᱯᱷᱟ.ᱜᱩᱱ", "ᱪᱟ.ᱛ", "ᱵᱟ.ᱭᱥᱟ.ᱠ", "ᱡᱷᱮᱸᱴ",
                     "ᱟᱥᱟᱲ", "ᱥᱟᱱ", "ᱵᱷᱟᱫᱟᱨ", "ᱰᱟᱸᱥᱟᱭ", "ᱥᱚᱦᱨᱟᱭ", "ᱟᱸᱜᱷᱥᱲ", "ᱯᱩᱥ"]

python_olchiki_weekdays = ["ᱚᱛᱮ", "ᱵᱟᱞᱮ", "ᱥᱟ.ᱜᱩᱱ",
                       "ᱥᱟ.ᱨᱫᱤ", "ᱡᱟ.ᱨᱩᱢ", "ᱧᱩᱦᱩᱢ", "ᱥᱤᱸᱜᱮ"]

greg_equivalent_olchiki_seasons = ["ᱱᱤᱨᱚᱱ", "ᱫᱷᱚᱨᱚᱱ", "ᱡᱟ.ᱯᱩᱫ",
                      "ᱦᱟᱣᱮᱫ", "ᱦᱮᱢᱮᱟᱞ", "ᱨᱟᱵᱟᱝ"]

greg_equivalent_last_day_of_olchiki_months =  [13, 12, 14, 13, 14, 14,
                                              15, 15, 15, 15, 14, 14]

total_days_in_olchiki_months = [30, 30, 30, 30, 31, 31,
                               31, 31, 31, 30, 30, 30]

greg_equivalent_leap_year_index_in_olchiki_months = 2

def is_leap_year(passed_year):
    if passed_year % 400 == 0:
        return 1
    elif passed_year%4 == 0 and passed_year%100 != 0:
        return 1
    else:
        return 0

def get_olchiki_year(passed_date, passed_month, passed_year):
    if passed_month > 3:
        olchiki_year = passed_year - 593
    elif passed_month == 3 and passed_date > 13:
        olchiki_year = passed_year - 593
    else:
        olchiki_year = passed_year - 594
    return olchiki_year

def get_olchiki_weekday(passed_date, passed_month, passed_year):
    current_date_object = datetime.datetime(passed_year, passed_month, passed_date)
    olchiki_weekday = python_olchiki_weekdays[current_date_object.weekday()]
    return olchiki_weekday

def convert_english_digit_to_olchiki_digit(original):
    converted = ""
    for character in str(original):
        if character in english_number:
            converted+=olchiki_number[english_number.index(character)]
        else:
            converted+=character
    return converted

def get_date(passed_date=None, passed_month=None, passed_year=None):
    if passed_date == None and passed_month == None and passed_year == None:
        current_date_object = datetime.date.today()
        passed_year = current_date_object.year
        passed_month = current_date_object.month
        passed_date = current_date_object.day
    olchiki_weekday = get_olchiki_weekday(passed_date, passed_month, passed_year)
    passed_month = passed_month - 1
    olchiki_year = get_olchiki_year(passed_date, passed_month, passed_year)
    if passed_date <= greg_equivalent_last_day_of_olchiki_months[passed_month]:
        total_days_in_current_olchiki_month = total_days_in_olchiki_months[passed_month]
        if passed_month == greg_equivalent_leap_year_index_in_olchiki_months and is_leap_year(passed_year) == 1:
            total_days_in_current_olchiki_month += 1
        olchiki_date = total_days_in_current_olchiki_month + passed_date - greg_equivalent_last_day_of_olchiki_months[passed_month]
        olchiki_month_index = passed_month
        olchiki_month = greg_equivalent_olchiki_months[olchiki_month_index]
    else:
        olchiki_date = passed_date - greg_equivalent_last_day_of_olchiki_months[passed_month]
        olchiki_month_index = (passed_month+1)%12
        olchiki_month = greg_equivalent_olchiki_months[olchiki_month_index]

    olchiki_season = greg_equivalent_olchiki_seasons[olchiki_month_index // 2]

    olchiki_date_month_year_season = {
        "date": convert_english_digit_to_olchiki_digit(olchiki_date),
        "month": convert_english_digit_to_olchiki_digit(olchiki_month),
        "year": convert_english_digit_to_olchiki_digit(olchiki_year),
        "season": convert_english_digit_to_olchiki_digit(olchiki_season),
        "weekday": convert_english_digit_to_olchiki_digit(olchiki_weekday)
    }

    return olchiki_date_month_year_season
