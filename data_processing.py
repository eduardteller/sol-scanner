import time
from datetime import datetime


def adjust_to_ten_digits(number: float) -> float:
    # Extract the integer part without sign
    integer_part = str(abs(int(number)))
    num_digits = len(integer_part)

    # Adjust the integer part to have exactly 10 digits
    if num_digits < 10:
        while num_digits < 10:
            number *= 10
            integer_part = str(abs(int(number)))
            num_digits = len(integer_part)
    elif num_digits > 10:
        while num_digits > 10:
            number /= 10
            integer_part = str(abs(int(number)))
            num_digits = len(integer_part)

    return number


def format_time(pair_time: int | float) -> str:
    timestamp1 = time.time()
    timestamp2 = adjust_to_ten_digits(pair_time)

    # Convert to datetime objects
    datetime1 = datetime.fromtimestamp(timestamp1)
    datetime2 = datetime.fromtimestamp(timestamp2)

    time_diff = datetime1 - datetime2

    # Extract total seconds
    total_seconds = int(time_diff.total_seconds())

    # Calculate days, hours, minutes, and seconds
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Check for years and months first
    if days >= 365:
        years = days // 365
        formatted_time_diff = f"{years}Y"
    elif days >= 30:
        months = days // 30
        formatted_time_diff = f"{months}Mo"
    elif days > 0:
        formatted_time_diff = f"{days}D"
    elif hours > 0:
        formatted_time_diff = f"{hours}H"
    elif minutes > 0:
        formatted_time_diff = f"{minutes}M"
    else:
        formatted_time_diff = f"{seconds}S"

    return formatted_time_diff


def format_values(value: float | int) -> str:
    if value > 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value > 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value > 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return f"{value}"
