import datetime

# Replace the date with your desired starting date
start_date = datetime.date(2023, 3, 1)  # Year, month, and day

# Calculate the ending date (two weeks later)
end_date = start_date + datetime.timedelta(weeks=2)

# Generate a list of days within the two-week range
date_range = []
current_date = start_date
while current_date <= end_date:
    date_range.append(current_date)
    current_date += datetime.timedelta(days=1)

# Print the start date, end date, and the list of days
print("Start Date:", start_date)
print("End Date:", end_date)
print("Days in the Two Weeks:")
for day in date_range:
    print(day)