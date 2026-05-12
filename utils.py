import re
from datetime import datetime

def parse_safe_number(value):
    if not isinstance(value, str):
        return value

    # Find the first number-looking pattern, e.g. "R$ 587.10", "$1,234.56", "12345"

    cleaned = re.sub(r'\n\[\d+\]', '', value)

    match = re.search(r'[\d.,]+', cleaned)
    if not match:
        return value

    num_str = match.group()
    num_str = num_str.replace(',', '')

    try:
        if num_str.isdigit():
            if len(num_str) < 10:
                return int(num_str)
            else:
                return num_str
        else:
            return round(float(num_str), 2)
    except ValueError:
        return value

# def test():
#     # Test cases for parse_safe_number
#     ret =  parse_safe_number('1,573\n[2]')
#     print(type(ret))
#     print(ret)
#     assert ret == str(1573)
#
#     print("All tests passed!")

# test()

def abbrev_to_state_name(abbrev):
    state_abbrev_map = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming',
        'DC': 'District of Columbia',
    }

    # Normalize input to uppercase, remove whitespace
    abbrev = abbrev.strip().upper()

    return state_abbrev_map.get(abbrev, "Unknown State")

def convert_to_full_date(short_date: str, year: int = 2025) -> str:
    # Parse the short format "6-18"
    month, day = map(int, short_date.split('-'))
    # Create a date object
    full_date = datetime(year, month, day)
    # Format as YYYY-MM-DD
    return full_date.strftime('%Y-%m-%d')

def chargeSum():
    sum = 0
    with open("card.txt", "r") as f:
        while True:
            line = f.readline()
            info = getRecord(line)
            if info:
                sum += info['target']
            if not line: break
    print(f"sum: {sum}")

def getRecord(record):
    # match record like "1234 +100" or "1234 -50"
    match = re.match(r'(\d{4})\s{0,}([+|-])\s{0,}((\d+\.\d+)|\d+)',record)
    if match:
        card = match.group(1)
        operation = match.group(2)
        amount = float(match.group(3))
        if operation == '-':
            amount = -amount
        return {'num':card, 'target': amount,'success': False}
    return None
