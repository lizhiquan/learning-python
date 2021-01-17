from city_model import City
from city_model import CityDatabase
from city_model import OverheadPassEvent
from city_model import CityOverheadTimes
import threading
import requests


class ISSDataRequest:
    """
    A wrapper for accessing the Open Notify API's iss-pass endpoint.
    This endpoint takes the location (latitude and longitude) and
    returns data about the number of times and the exact times that the
    ISS space station will be directly overhead that location.
    """

    # The url to the overhead pass endpoint form the Open notify API
    OPEN_NOTIFY_OVERHEAD_PASS_URL = \
        "http://api.open-notify.org/iss-pass.json?lat={0}&lon={1}"

    def __init__(self, session: requests.Session):
        self.session = session

    def get_overhead_pass(self, city: City) -> CityOverheadTimes:
        # TODO: Implement a get request that takes the location data
        # from a city and conducts a get request at the
        # OPEN_NOTIFY_OVERHEAD_PASS_URL endpoint.

        # Parse through the JSON Response to create a CityOverheadTimes
        # object and return it.
        url = self.OPEN_NOTIFY_OVERHEAD_PASS_URL.format(city.lat, city.lng)
        with self.session.get(url) as response:
            return CityOverheadTimes(city, *response.json()['response'])


class CityOverheadTimesList:

    def __init__(self):
        self.data = []
        self.lock = threading.Lock()

    def append(self, city_overhead_times: CityOverheadTimes):
        with self.lock:
            self.data.append(city_overhead_times)


class CityOverheadTimesRequestThread(threading.Thread):
    """
    This thread takes in a list of cities and executes a request to
    acquire the CityOverheadTimes for each city using the ISSDataRequest
    class. It then appends the CityOverheadTimes to a
    CityOverheadTimesList.
    """

    def __init__(self, cities: list,
                 city_overhead_times_list: CityOverheadTimesList):
        super().__init__()
        self.cities = cities
        self.city_overhead_times_list = city_overhead_times_list

    def run(self):
        with requests.session() as session:
            request = ISSDataRequest(session)
            for city in self.cities:
                city_overhead_times = request.get_overhead_pass(city)
                self.city_overhead_times_list.append(city_overhead_times)


def main():
    # Create 3 threads that split the cities from a city database amongst
    # themselves and execute ISSDataRequest for each city.
    # These threads should append the results to a list of
    # CityOverheadTimes objects using a lock to do so safely.
    db = CityDatabase('city_locations.xlsx')
    times_list = CityOverheadTimesList()
    t1 = CityOverheadTimesRequestThread(db.city_db, times_list)
    t2 = CityOverheadTimesRequestThread(db.city_db, times_list)
    t3 = CityOverheadTimesRequestThread(db.city_db, times_list)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    for times in times_list.data:
        print(times)


if __name__ == '__main__':
    main()


