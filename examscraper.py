from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import re
import csv

# create csv file
with open('student_grades.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Mündlich', 'Schriftlich', 'Gesamt', 'Ergebnis'])

    # setup url and variables
    success_count = 0
    fail_count = 0
    not_rated_count = 0
    url = 'https://school-name/check?bogennummer=' # changed for the internet
    start_id = 0 # changed for the internet
    end_id = 1 # changed for the internet

    # loop through the students and poplulate the csv file
    for i in range(start_id, end_id + 1):
        
        full_url = url + str(i)
        result = requests.get(full_url)
        soup = BeautifulSoup(result.text, 'html.parser')
        tds = soup.find_all(re.compile('td'))
        points = re.findall('[^a-z]\d+\.*\d*', str(tds))
        schriftlich = []
        mündlich = []
        gesamt = []

        rating = soup.find_all(text=['Bestanden', 'Sehr Gut', 'Gut', 'Befriedigend', 'Ausreichend', 'Nicht Bestanden', 'X'])
        name = re.findall('[A-Za-z]*\s*[A-Za-z]*\s*[A-Za-z]*\s*,{1}\s*[A-Za-z]*\s*[A-Za-z]*\s*[A-Za-z]*', str(soup))[1]

        if not name:
            continue
        if not rating:
            not_rated_count += 1
            writer.writerow([name, 'X', 'X', 'X', 'nicht bewertet'])
            continue

        for i in range(0, len(points)):
            points[i] = points[i][1:]

        for i in range(0, len(points) - 3):
            if i % 2 == 0:
                mündlich.append(points[i])
            else:
                schriftlich.append(points[i])
            
        for i in range(len(points) - 3, len(points)):
            gesamt.append(points[i])

        if rating[2] in ['Nicht Bestanden', 'X']:
            fail_count += 1
            writer.writerow([name, gesamt[0], gesamt[1], gesamt[2], 'nicht bestanden'])

        elif rating[2] in ['Sehr Gut', 'Gut', 'Befriedigend', 'Ausreichend','Bestanden']:
            success_count += 1
            writer.writerow([name, gesamt[0], gesamt[1], gesamt[2], 'bestanden'])
            


    # bar chart
    x_axis = ['bestanden', 'nicht bestanden', 'nicht bewertet']
    y_axis = [success_count, fail_count, not_rated_count]

    plt.bar(x_axis, y_axis)
    plt.title('Ergebnisse')
    plt.ylabel('Anzahl')
    plt.show()
