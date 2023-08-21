import datetime
import dateutil

ISO_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fz'

def convert_date_time_str_to_obj(date_time_str):
    return datetime.datetime.strptime(
        date_time_str, ISO_DATETIME_FORMAT)


def convert_iso_date_str_to_obj(date_time_str):
    return dateutil.parser.parse(date_time_str)


def convert_utc_date_to_iso(utc_date_obj):
    """ convert to ISO8601 format.

    :param utc_date_obj: datetime.datetime object
    """
    if not isinstance(utc_date_obj, datetime.datetime):
        raise TypeError("utc_date_obj should be a datetime.datetime object")

    if utc_date_obj.tzname() == 'UTC':
        # remove the tz info as python converts it to +00:00 but we need Z
        # at end
        utc_date_obj = utc_date_obj.replace(tzinfo=None)

    formatted_info = utc_date_obj.isoformat(timespec='milliseconds')

    # datetime.datetime.isoformat returns a string in ISO format without Z
    if not utc_date_obj.tzinfo:
        return formatted_info + 'Z'

    return formatted_info


if __name__ == '__main__':
    iso_formatted_date_str = '2020-10-01T11:12:16.944Z'
    date_time_obj = convert_date_time_str_to_obj(iso_formatted_date_str)
    print(date_time_obj) # 2020-10-01 11:12:16.944000

    date_time_obj = convert_utc_date_to_iso(date_time_obj)
    print(date_time_obj) # 2020-10-01T11:12:16.944Z

    iso_date_str = '2022-01-21T09:06:03.348+00:00'

    #print(f'IN seconds: {date_time_obj.timestamp()}')
