from datetime import datetime, timedelta

def parse_time_range(start,end):
    today = datetime.today().date()

    if start == "now":
        start = today
    elif start == "yesterday":
        start = today - timedelta(days=1)
    else:
        start = datetime.strptime(start, '%Y-%m-%d').date()

    if end == "now":
        end = today + timedelta(days=1)
    elif end == "yesterday":
        end = today
    else:
        end = datetime.strptime(end, '%Y-%m-%d').date()

    # open and write end date to file when exist overwrite it
    end_date = (end-timedelta(days=1)).strftime('%Y-%m-%d')

    with open('end_date.txt', 'w') as f:
        f.write(end_date)
    return start, end

def get_time_range(start,end):
    start_std,end_std = parse_time_range(start,end)
    print(f"time_range={start_std}_{end_std}")
    return f"time_range={start_std}_{end_std}"


def get_everyday_range(start,end):
    start,end = parse_time_range(start,end)
    print(start,end)
    range_list = []
    begin = start
    while begin < end:
        range_list.append(f"time_range={begin}_{begin + timedelta(days=1)}")
        begin += timedelta(days=1)

    print(range_list)
    return range_list

def get_start_day_from_time_range(time_range):
    range = time_range.replace('time_range=', '')
    start, end = range.split('_')
    return start


# range_list = get_everyday_range('date-to-yesterday-2025-5-24')
# print(range_list)

