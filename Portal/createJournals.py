import csv
def read_impact_Factor():
      with open("C:\\Users\\Ritu\\PycharmProjects\\EWL-Using-Blockchain\\2018JournalImpactFactor.csv", 'r') as csv_file:

            csv_reader = csv.DictReader(csv_file)
            journals = {}
            for row in csv_reader:
                  # print(row)
                  title = row['Full Journal Title']
                  journals[title] = row['Journal\nImpact']

      return journals


