from __future__ import print_function
import googlemaps
from datetime import datetime
from bs4 import BeautifulSoup

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

class LocationService(object):

    def __init__(self,source,*args):
        apikey ="AIzaSyCljSfU86qvpoo6XplCgvRvON47rA_91vw"
        self.gmaps = googlemaps.Client(key=apikey)
        self.source =source
        self.addrList = list(*args)
        self.distances = {}
        self.durations = {}
        self.rev_dist = {}
        self.get_distances()

    def add_address(self,addr):
        self.addrList.append(addr)

    def get_distances(self):
        result = self.gmaps.distance_matrix(self.source,self.addrList)
        for i, addr in enumerate(result[DEST_ADDRS]):
            distance = result['rows'][0]['elements'][i]['distance']['text']
            duration = result['rows'][0]['elements'][i]['duration']['text']
            self.distances[(self.source,addr)] = distance
            self.durations[(self.source,addr)] = duration
            self.rev_dist[distance] = (self.source,addr)
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

    def get_directions(self, dest):
        now = datetime.now()
        if len(dest) == 1:
            dest = dest[0]
        directions = ParseDirections.get_text_directions(self.gmaps.directions(self.source,dest,departure_time=now))
        return "From " + self.source +":\n" + directions

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
    print("Nearest locations: \n\n")
    pp.pprint(ls.get_n_nearest(3))
    print("Directions: \n")
    print(ls.get_directions(addr2))

