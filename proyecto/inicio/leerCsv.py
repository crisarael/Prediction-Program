import csv

with open('UploadedFiles/Titanic.csv', newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        print(row)
