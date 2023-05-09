from flight_data import FlightData
from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
from pprint import pprint

ORIGIN_CITY_IATA = "KTW"

flight_search = FlightSearch()
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()


if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    try:
        if flight.price < destination["lowestPrice"]:
            message = f"{flight.price} PLN to fly from {flight.origin_city}-{flight.origin_airport}" \
                      f" to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date}" \
                      f" to {flight.return_date}."
            print(message)

    except AttributeError:
        pass
