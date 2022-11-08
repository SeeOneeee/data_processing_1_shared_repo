
from datetime import datetime
import requests
import csv

def csv_converter(url):
    csvList = []

    listCount = 0
    # Start Date of the monkey pox data set
    startDate = datetime(2022, 4, 22).date()

    try:

        rData = requests.get(url)

        # Creating a temporary file and saving the requested data in it
        # The file will be deleted after the check.
        
        toExtractFilePath = "./data/to_extract_dataset_1.csv"

        with open(toExtractFilePath, 'wb') as fw:
            fw.write(rData.content)
        fw.close()


        fr = open(toExtractFilePath, 'r')
        #fr = open("./data/to_extract_dataset_1.csv")
        values = csv.reader(fr)
        listValues = list(values)

        for i in listValues:
            try:
                converted_value = datetime.strptime(i[0], "%d/%m/%Y").date()
                if converted_value >= startDate:
                    csvList.append(i)
                else:
                    pass

            except ValueError:
                continue
            """
            for innerValue in value:
                converted_value = convert(innerValue)
                print(converted_value)
                #csvList.append(converted_value)
            """

        fr.close()

        print(type(csvList[1][0]))
        csvListSort = csvList
        for i in csvList:

            convertedDate = datetime.strptime(i[0], "%d/%m/%Y").date()
            csvListSort[listCount][0] = convertedDate
            listCount += 1

        csvListSort = sorted(csvListSort)

        # clearing the csv list and list count
        csvList = []
        listCount = 0

        csvList.extend(csvListSort)

        for i in csvListSort:

            csvList[listCount][0] = i[0].strftime('%Y-%m-%d')
            listCount += 1

        print(csvList)

    # Writing csv files
    # https://www.geeksforgeeks.org/writing-csv-files-in-python/ , 07.11.2022

        with open("extracted_covid_data.csv", 'w', newline='') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(listValues[0])

            # writing the data rows
            csvwriter.writerows(csvList)

    except:
        pass


if __name__ == '__main__':
    url = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv"
    csv_converter(url)