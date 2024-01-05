import requests
import json
import csv

searchUrl = 'https://www.qantas.com/hotels/api/ui/locations/London,%20England,%20United%20Kingdom/availability?checkIn=2024-01-11&checkOut=2024-01-12&adults=2&children=0&infants=0&sortBy=popularity&propertyTypes=&facilities=&subRegions=&limit=25&payWith=cash&page=1'
searchHeaders = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'If-None-Match': 'W/\"f652-bWEFIFvuZ6kD/U/Sc9QSmmsxOio\"',
    'Qh-Meta': '{"qhUserId":"b1f7b756-0320-48d6-940f-37c31c77c688"}',
    'Referer': 'https://www.qantas.com/hotels/search/list?adults=2&checkIn=2024-01-11&checkOut=2024-01-12&children=0&infants=0&location=London%2C+England%2C+United+Kingdom&sortBy=popularity&page=1&payWith=cash'
    }
s = requests.get(searchUrl, headers=searchHeaders, verify=False)

#getting a list of hotels from the response
hotels = json.loads(s.text)
hotelsList = hotels["results"]

# getting a list of hotel ids and names
hotelIdList = []
for i in range(len(hotelsList)):
    hotelDict = {}
    hotelDict["name"] = hotelsList[i]["property"]["name"]
    hotelDict["id"] = hotelsList[i]["property"]["id"]
    hotelIdList.append(hotelDict)

#headers for request to pull list of romm types/offers
headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'If-None-Match': 'W/\"f652-bWEFIFvuZ6kD/U/Sc9QSmmsxOio\"',
    'Qh-Meta': '{"qhUserId":"b1f7b756-0320-48d6-940f-37c31c77c688"}',
    'Referer': 'https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-01-11&checkOut=2024-01-12&children=0&infants=0&location=London%2C+England%2C+United+Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity'
}

# create .csv file
csv_file = open('C:\\Users\SBotalov\Desktop\hotel_rates.csv', 'w', newline='') 
writer = csv.writer(csv_file, dialect='excel')
writer.writerow(["Hotel_id", "Hotel name", "Room name", "Rate Name", "Number of Guests", "Cancellation Policy", "Price", "Top Deal?", "Currency"]) # write headers to .csv file

for k in hotelIdList:
    hotelId = k["id"]
    hotelName = k["name"]

    url = 'https://www.qantas.com/hotels/api/ui/properties/' + hotelId + '/availability?checkIn=2024-01-11&checkOut=2024-01-12&adults=2&children=0&infants=0&payWith=cash' #url concatenation for every hotel_id
    r = requests.get(url, headers=headers, verify=False)  
    
    roomTypes = json.loads(r.text) #response json
    roomTypesList = roomTypes["roomTypes"] # list of room types and offers

    #getting rate data 
    for i in range(len(roomTypesList)):
        roomName = roomTypesList[i]["name"]
        numberOfGuests = roomTypesList[i]["maxOccupantCount"]
        offers = roomTypesList[i]["offers"] # list of offers for particular room type
        for j in range(len(offers)): 
            rateName = offers[j]["name"]
            price = offers[j]["charges"]["total"]["amount"]
            currency = offers[j]["charges"]["total"]["currency"]
            cancellationPolicy = offers[j]["cancellationPolicy"]["description"]
            if offers[j]["promotion"]:
                topDeal = True
            else:
                topDeal = False
            #writing the rate down to .csv
            writer.writerow([hotelId, hotelName, roomName, rateName, numberOfGuests, cancellationPolicy, price, topDeal, currency]) 
        
csv_file.close()