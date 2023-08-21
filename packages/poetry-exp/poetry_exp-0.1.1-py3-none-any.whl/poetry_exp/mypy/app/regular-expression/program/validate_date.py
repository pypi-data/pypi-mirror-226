import re

DATE_PATTERN = '^(0?[1-9]|1[0-9]|2[0-9]|3[0-1])/(0?[1-9]|1[0-2])/(1[8-9][0-9]{2}|2[0-9]{3})$'
DATE_PATTERN2 = '^(0?[1-9]|1[0-9]|2[0-9]|3[0-1])-(0?[1-9]|1[0-2])-(1[8-9][0-9]{2}|2[0-9]{3})$'

days_dict = {
    1: 31,
    3: 31,
    4: 30,
    5: 31,
    6: 20,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}


def validate_date(date_str):
    match = re.match(DATE_PATTERN, date_str)
    if match:
        dd = match.group(1)
        mm = match.group(2)
        yy = match.group(3)

        # e.g 2016 is a leap year divisible by 4 but not by 100
        leap_year = True if ((int(yy) % 4 == 0 and int(yy) % 100 != 0) or int(yy) % 400 == 0) else False
        feb_days = 29 if leap_year else 28

        if int(mm) == 2:
            if int(dd) > feb_days:
                print 'Invalid Date: ', date_str
                return False
        else:
            if int(dd) > days_dict[int(mm)]:
                print 'Invalid Date: ', date_str
                return False

        print 'DD:{0} MM:{1} YY:{2}'.format(dd, mm, yy)
        return True

    else:
        print 'Invalid Date: ', date_str
        return False


if __name__ == '__main__':
    date_list = [
        '17/03/1989',
        '15/07/1989',
        '05/12/2015',
        '1/1/1989',
        '31/01/2012',
        '31/03/2013',
        '30/04/2015',
        '31/04/2013',
        '31/05/2019',
        '29/02/2000',
        '29/02/2016',
        '28/02/2001',
        '29/02/2001',
        '30/02/2000',
        '30/02/2001',
        '14/06.2012',
        '200/01/1989',
        '1/13/1800',
        '1/1/02'
    ]

    for date in date_list:
        validate_date(date)