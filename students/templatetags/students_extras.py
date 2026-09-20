from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key (supports string & int keys)"""
    if dictionary is None or not isinstance(dictionary, dict):
        return None
    if key in dictionary:
        return dictionary[key]
    str_key = str(key)
    if str_key in dictionary:
        return dictionary[str_key]
    return None


@register.filter
def concat_key(val1, val2):
    """Concatenate two values into a string key with an underscore: e.g. monday_1"""
    return f"{val1}_{val2}"


@register.filter
def stream_code(name):
    """Convert stream/division full name to compact short code"""
    if not name:
        return "GEN"
    name_clean = str(name).strip()
    name_upper = name_clean.upper()

    code_map = {
        'COMMERCE': 'COMM',
        'HUMANITIES': 'HUM',
        'SCIENCE': 'SCI',
        'B A ENGLISH': 'BA ENG',
        'BA ENGLISH': 'BA ENG',
        'B A SOCIOLOGY': 'BA SOC',
        'BA SOCIOLOGY': 'BA SOC',
        'B COM': 'B.COM',
        'B.COM': 'B.COM',
        'BCOM': 'B.COM',
        'B SC': 'B.SC',
        'BSC': 'B.SC',
        'BBA': 'BBA',
        'BCA': 'BCA',
        'PPTTC': 'PPTTC',
        'GENERAL': 'GEN',
    }
    if name_upper in code_map:
        return code_map[name_upper]

    # If short already (<= 6 chars), return uppercase
    if len(name_upper) <= 6:
        return name_upper

    # If starts with BA / B A / B COM etc.
    for prefix, code in [('B A ', 'BA '), ('BA ', 'BA '), ('B COM', 'B.COM'), ('B SC', 'B.SC')]:
        if name_upper.startswith(prefix):
            remainder = name_upper[len(prefix):].strip()
            return f"{code}{remainder[:4]}"

    # Acronym fallback for multi-word
    words = name_upper.split()
    if len(words) > 1:
        return ''.join(w[0] for w in words[:4])

    return name_upper[:4]


