import os
import csv

# Define the destination folder and filename
folder_path = "C:/Users/DELL/Desktop/ANPR"  
# Raw string to avoid escape characters
filename = "test1.csv"

# Combine the folder path and filename
file_path = os.path.join(folder_path, filename)

# Open the file in write mode and create a CSV writer object
with open(file_path, mode='w', newline='') as file:
    # Create a CSV writer object
    writer = csv.writer(file)

    # Write an empty row to the CSV file
    writer.writerow([])

print(f"Empty CSV file '{filename}' has been created in '{folder_path}'.")
