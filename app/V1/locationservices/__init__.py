from __future__ import print_function
import googlemaps
from datetime import datetime
from bs4 import BeautifulSoup
import os
import usaddress as uaddr

# API_KEY = os.environ.get('GOOGLE_API_KEY')
API_KEY = "AIzaSyCljSfU86qvpoo6XplCgvRvON47rA_91vw"
DEST_ADDRS = "destination_addresses"
ORIG_ADDRS = "origin_addresses"

class ParseDirections(object):
    @staticmethod
    def get_HTML_directions(directions):
        html = []
        for step in directions[0]["legs"][0]["steps"]:
           html.append(step["html_instructions"] )
        return html

    @staticmethod
    def get_text_directions(directions):
        htmlList = ParseDirections.get_HTML_directions(directions)
        soup = BeautifulSoup("\n".join(htmlList),"lxml")
        return soup.text

# TODO use AddresMapper to decompose address into
# city, state, zip... etc
class AddressMapper(object):
    def __init__(self):
        """ Address Mapper and parser that returns orderedDict
            with keys: [fulladdress, city, state, zip] to access data
        """
        self.fulladdrmapping = {
           'Recipient': 'recipient',
           'AddressNumber': 'fulladdress',
           'AddressNumberPrefix': 'fulladdress',
           'AddressNumberSuffix': 'fulladdress',
           'StreetName': 'fulladdress',
           'StreetNamePreDirectional': 'fulladdress',
           'StreetNamePreModifier': 'fulladdress',
           'StreetNamePreType': 'fulladdress',
           'StreetNamePostDirectional': 'fulladdress',
           'StreetNamePostModifier': 'fulladdress',
           'StreetNamePostType': 'fulladdress',
           'CornerOf': 'fulladdress',
           'IntersectionSeparator': 'fulladdress',
           'LandmarkName': 'fulladdress',
           'USPSBoxGroupID': 'fulladdress',
           'USPSBoxGroupType': 'fulladdress',
           'USPSBoxID': 'fulladdress',
           'USPSBoxType': 'fulladdress',
           'BuildingName': 'address2',
           'OccupancyType': 'address2',
           'OccupancyIdentifier': 'address2',
           'SubaddressIdentifier': 'address2',
           'SubaddressType': 'address2',
           'PlaceName': 'city',
           'StateName': 'state',
           'ZipCode': 'zipcode',
        }
        self.uaddr = uaddr

    def parse(self, addr, mapping='fulladdress'):
        if mapping == 'fulladdress':
            return self.uaddr.tag(addr, tag_mapping=self.fulladdrmapping)[0]
        elif mapping == 'default':
            return self.uaddr.tag(addr)[0]

def eval_dist(dist):
    return float(dist.split(" ")[0])

def format_addr(addr):
    addr = addr.split(",")[:-1]
    return ",".join(addr)

def parse_addr(addr):
    pass

class LocationService(object):

    def __init__(self,source,*args):
        print("API_KEY:", API_KEY)
        self.addrmapper = AddressMapper()
        self.gmaps = googlemaps.Client(key=API_KEY)
        self.source = self.addrmapper.parse(source)
        print(self.source)
        self.addrList = list(*args)
        self.distances = {}
        self.durations = {}
        #reverse distance hashmap
        self.rev_dist = {}
        self.geo_addrList = []
        self.get_distances()

    def add_address(self,addr):
        self.addrList.append(addr)

    def get_distances(self):
        result = self.gmaps.distance_matrix(self.source.get('fulladdress'),self.addrList,units="imperial")
        for i, addr in enumerate(result[DEST_ADDRS]):
            addr = format_addr(addr)
            distance = result['rows'][0]['elements'][i]['distance']['text']
            duration = result['rows'][0]['elements'][i]['duration']['text']
            self.distances[(self.source.get('fulladdress'),self.addrList[i])] = distance
            self.durations[(self.source.get('fulladdress'),self.addrList[i])] = duration
            self.rev_dist[distance] = (self.source.get('fulladdress'),self.addrList[i])
        return self.distances

    def get_n_nearest(self,n):
        sorted_by_dist = sorted(self.rev_dist.keys())
        nearest = []
        for i in range(n):
            nearest.append((self.rev_dist[sorted_by_dist[i]], sorted_by_dist[i]))
        return nearest

    def get_n_nearest_addr(self,n):
        nearest = self.get_n_nearest(n)
        nearest_addr = []
        for addr,dist in nearest:
            nearest_addr.append(addr[1])
        return nearest_addr

    def get_addr_by_radius(self, radius=10):
        results = []
        addrs = self.get_distances()
        li = [dest for _,dest in addrs.keys()]
        # print("len(addrs):",len(addrs))
        for i,((source,dest), dist) in enumerate(addrs.items()):
            if eval_dist(dist) <=float(radius):
                temp = {}
                temp[(source,dest)] = eval_dist(dist)
                temp["destination"] = self.addrmapper.parse(dest)
                results.append(temp) 
        return results

    def get_directions(self, dest):
        now = datetime.now()
        if len(dest) == 1:
            dest = dest[0]
        directions = ParseDirections.get_text_directions(self.gmaps.directions(self.source.get('fulladdress'),dest,departure_time=now))
        return "From " + self.source +":\n" + directions

    def get_places(self, search_term):
        place_results = self.gmaps.places(query=search_term)
        for res in place_results['results']:
            pp.pprint("Name: "+ str(res['name']))
            pp.pprint("Location: "+ str(res['geometry']['location']))
            pp.pprint("Rating: "+ str(res['rating']))
            print("\n\n\n")
        pp.pprint(place_results['results'][0])


if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter()
    source = "950 w. linden st., Riverside, CA"
    addr1 = "1959 s. Fern, Ontario, CA"
    addr2 = "3734 live oak creek way, Ontario, CA"
    addr3 = "1600 Amphitheatre Parkway, Mountain View, CA"
    addr4 = "3737 live oak creek way, Ontario, CA"
    addr5 = "900 University Ave, Riverside, CA"
    addr6 = "1133 W Blaine St, Riverside, CA"
    ls = LocationService(source,[addr1,addr2,addr3, addr4, addr5,addr6])
    pp.pprint(ls.get_distances())
    """
    print("Nearest locations: \n\n")
    pp.pprint(ls.get_n_nearest(3))
    print("Directions: \n")
    print(ls.get_directions(addr2))
    """
    print("\n\n")
    pp.pprint(ls.get_addr_by_radius(radius=17))
    # ls.get_places("mexican in riverside, ca")

