from datetime import datetime
SNAP_MAX_EXPIRE_HOURS_LIMIT = 2 * 24



def parse_json_datetime(date_time):
    iso_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.strptime(date_time, iso_format)


def calculate_hours_from_now(d):
    """
    Calculate the number of hours from the current date time
    :param d: Future date time in string format "2025-06-10T22:04:46.000Z"
    :return: Number of hours from current date
    """
    current_date = datetime.utcnow()
    delta = parse_json_datetime(d) - current_date
    print(delta.days)
    print(delta.seconds)
    total_hours = delta.total_seconds() / (60 * 60)  # hours
    return total_hours


TIME_FORMAT_MULTIPLIER = {
    'Hours': 1,
    'Days': 24,
    'Weeks': 24 * 7,
    'Months': 24 * 7 * 30,
    'Years': 24 * 7 * 30 * 365
}

def validate_snap_max_expire_limit(total_hours, unit='Days'):
    if total_hours > (SNAP_MAX_EXPIRE_HOURS_LIMIT):
        max_limit = str(SNAP_MAX_EXPIRE_HOURS_LIMIT / TIME_FORMAT_MULTIPLIER[unit]) + ' ' + unit
        #raise Exception("Maximum snapshot expire limit is {0}.".format(max_limit))
        print('Error: Maximum snapshot expire limit is {0}'.format(max_limit))


if __name__ == '__main__':
    current_date = datetime.utcnow()
    #print(current_date)  # 2020-06-23 09:27:07.263331
    # 2020-05-27T08:31:54.000Z
    #2025-06-10T22:04:46.000Z

    future_date = parse_json_datetime("2020-06-27T08:31:54.000Z")
    # print(future_date)
    # delta = future_date - current_date
    # print(delta)
    # print(delta.days)

    previous_date = "2020-06-10T22:04:46.000Z"
    future_date = "2025-06-10T22:04:46.000Z" # 2025-06-10T22:04:46.000Z

    #print(calculate_hours_from_now(future_date))
    print(calculate_hours_from_now("2025-06-23T11:04:46.000Z")/24)

    # validate_snap_max_expire_limit(calculate_hours_from_now("2020-06-28T22:04:46.000Z"))
    # validate_snap_max_expire_limit(calculate_hours_from_now("2026-06-10T22:04:46.000Z"), unit='Hours')
    # validate_snap_max_expire_limit(calculate_hours_from_now("2026-06-10T22:04:46.000Z"), unit='Weeks')
    # validate_snap_max_expire_limit(calculate_hours_from_now("2026-06-10T22:04:46.000Z"), unit='Months')
    # validate_snap_max_expire_limit(calculate_hours_from_now("2026-06-10T22:04:46.000Z"), unit='Years')
    #

