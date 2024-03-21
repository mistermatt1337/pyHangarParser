import datetime
import re
from collections import defaultdict
import csv
import matplotlib.pyplot as plt

# Define the regular expression pattern to extract dates and cost information
pattern = r'(\b[A-Za-z]{3}\s\d{1,2}\s\d{4}),.*value:\s\$(\d+\.\d+)'

# Create a dictionary to store the extracted data
data = defaultdict(float)

# Open the log file
with open('log.txt', 'r', encoding='utf-8') as file:
    # Read each line in the file
    for line in file:
        # Search for the pattern in each line
        match = re.search(pattern, line)
        if match:
            # Extract the date and cost information
            date = match.group(1)
            cost = float(match.group(2))
            # Update the data dictionary
            data[date] += cost

# Extract the dates and costs from the data dictionary
dates = list(data.keys())
costs = list(data.values())

# Sort the dates in ascending order
sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, '%b %d %Y'))

# Calculate the running total over time
running_total = []
current_total = 0
for date in sorted_dates:
    current_total += data[date]
    running_total.append(current_total)

# Prepare the data dictionary to sum costs by month
monthly_data = defaultdict(float)
for date, cost in data.items():
    # Extract the month and year from the date
    month_year = date.split()[0] + ' ' + date.split()[2]
    # Update the monthly data dictionary
    monthly_data[month_year] += cost

# Extract the months and costs from the monthly data dictionary
months = list(monthly_data.keys())
monthly_costs = list(monthly_data.values())

# Display the results as month and year
for month, cost in monthly_data.items():
    print(f"{month}: {cost}")

# Create a CSV file to store the monthly data dictionary
with open('monthly_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Month', 'Cost'])
    for month, cost in monthly_data.items():
        writer.writerow([month, cost])

# Create a histogram or timeline using matplotlib
plt.figure(figsize=(10, 6))
plt.plot(sorted_dates, running_total)
plt.xlabel('Date')
plt.ylabel('Running Total')
plt.title('Running Total Over Time')
plt.xticks(rotation=45)
plt.show()