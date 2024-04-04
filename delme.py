import datetime

def get_day_of_week(date_str):
    try:
        # Parse the input date string into a datetime object
        date_object = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        # Get the day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
        day_of_week = date_object.strftime('%A')
        return day_of_week
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD format."

# Example usage
date = '2023-07-11'
print(f"The day of the week for {date} is: {get_day_of_week(date)}")