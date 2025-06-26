from flight import Flight

def comp_1 (a,b):
    if a<b:
        return True
    else:
        return False
    
class Heap:
    
    def __init__(self, tot_data, comparison_function=comp_1, init_array=None):
        if init_array is None:
            init_array = []
        self._comparator = comparison_function
        self._data = init_array[:]
        self._positions = [-1] * tot_data  
    
    def insert(self, element):
        self._data.append(element)
        idx = len(self._data) - 1
        self._positions[element[1]] = idx
        self._upheap(idx)
    
    def decrease_key(self, element_id, new_value):
        idx = self._positions[element_id]
        self._data[idx] = (new_value, element_id)
        self._upheap(idx)
    
    def extract(self):
        if self.is_empty():
            raise Exception
        last = len(self._data) - 1
        self._swap(0, last)
        element = self._data.pop()
        self._positions[element[1]] = -1
        if not self.is_empty():
            self._downheap(0)
        return element
    
    def top(self):
        if self.is_empty():
            raise Exception
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0
    
    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, j):
        return 2 * j + 1

    def _right(self, j):
        return 2 * j + 2

    def _has_left(self, j):
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]
        self._positions[self._data[i][1]] = i
        self._positions[self._data[j][1]] = j

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._comparator(self._data[j], self._data[parent]):
            self._swap(j, parent)
            self._upheap(parent)

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._comparator(self._data[right], self._data[left]):
                    small_child = right
            if self._comparator(self._data[small_child], self._data[j]):
                self._swap(j, small_child)
                self._downheap(small_child)

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.flights = flights[:]
        if len(flights) > 0 :
            self.num_cities = max(max([flight.end_city for flight in self.flights]) + 1, max([flight.start_city for flight in self.flights]) + 1)
        else : 
            self.num_cities = 0

        self.adjacency_list = [[] for _ in range(self.num_cities)]
        
        for flight in self.flights:
            self.adjacency_list[flight.start_city].append((flight.end_city, flight))
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        level = [start_city]
        tree_parents = [[(-1, -1, -1)] for _ in range(len(self.adjacency_list))]
        check = 0
        count = 0
        if start_city == end_city:
            return []
        else:

            while(len(level) > 0):
                next_level = []
                count += 1
                for level_city in level:
                    for city11, flight11 in self.adjacency_list[level_city]:
                        if flight11.departure_time >= t1 and flight11.arrival_time <= t2:
                            if tree_parents[city11][0][0] == -1:
                                if level_city == start_city:
                                    tree_parents[city11][0] = (level_city, 1, flight11)
                                else:
                                    for j in tree_parents[level_city]:
                                        if flight11.departure_time >= j[2].arrival_time + 20:
                                            tree_parents[city11][0] = (level_city, j[1] + 1, flight11)
                                            break

                                    if tree_parents[city11][0][0] == -1:
                                        continue
                            else:
                                f = -1
                                if level_city != start_city:
                                    for j in tree_parents[level_city]:
                                        if flight11.departure_time >= j[2].arrival_time + 20:
                                            f = 1
                                            break
                                    if f == -1:
                                        continue
                                if tree_parents[city11][-1][2].arrival_time > flight11.arrival_time:
                                    if tree_parents[city11][-1][1] == count:
                                        tree_parents[city11][-1] = (level_city, count, flight11)
                                    else:
                                        tree_parents[city11].append((level_city, count, flight11))
                                else:
                                    continue
                            if city11 == end_city:
                                check = 1
                            next_level.append(city11)               
                if check == 1:
                    break
                level = next_level
            
            if tree_parents[end_city][0][0] == -1:
                return []
                
            
            city_no, counter, flightt = tree_parents[end_city][0]
            path = []
            path.append(flightt)
            
            flag = -1
            while(city_no != start_city):
                for next_city_no, next_counter, next_flightt in tree_parents[city_no]:
                    if next_flightt.arrival_time + 20 <= flightt.departure_time:
                        flag = 1
                        city_no, counter, flightt = next_city_no, next_counter, next_flightt
                        path.append(flightt)
                        break
                if flag == -1:
                    path = []
                    break
            path = path[::-1]
            return path
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        if start_city==end_city:
            return []

        else:
            valid_flights = [flight for flight in self.flights if flight.departure_time >= t1 and flight.arrival_time <= t2]
            graph = self.build_graph(valid_flights, self.num_cities)
            
            min_cost_overall = float('inf')
            best_path_overall = []

            for idx, flight in enumerate(valid_flights):
                if flight.start_city == start_city:
                    min_cost, path = self.dijkstra_for_cheap(idx, valid_flights, graph, end_city)

                    if min_cost < min_cost_overall:
                        min_cost_overall = min_cost
                        best_path_overall = path

            return [valid_flights[idx] for idx in best_path_overall] if best_path_overall else []
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        if start_city==end_city:
            return []

        else:
            valid_flights = [flight for flight in self.flights if flight.departure_time >= t1 and flight.arrival_time <= t2]
            graph = self.build_graph(valid_flights, self.num_cities)
            
            min_cost_overall = (float('inf'),float('inf'))
            best_path_overall = []

            for idx, flight in enumerate(valid_flights):
                if flight.start_city == start_city:
                    min_cost, path = self.dijkstra_for_least_flight_cheap(idx, valid_flights, graph, end_city)

                    if min_cost < min_cost_overall:
                        min_cost_overall = min_cost
                        best_path_overall = path

            return [valid_flights[idx] for idx in best_path_overall] if best_path_overall else []

    def build_graph(self, valid_flights, num_cities):
        depart_city_flights = [[] for _ in range(num_cities)]
        for i, flight in enumerate(valid_flights):
            depart_city_flights[flight.start_city].append((i, flight))
        
        graph = [[] for _ in range(len(valid_flights))]
        
        for i, flighta in enumerate(valid_flights):
            end_city = flighta.end_city
            for j, flightb in depart_city_flights[end_city]:
                if flightb.departure_time >= flighta.arrival_time + 20:
                    graph[i].append((j, flighta.fare)) 

        return graph

    def dijkstra_for_cheap(self, start_flight_index, valid_flights, graph, end_city):
        num_flights = len(valid_flights)
        min_costs = [float('inf')] * num_flights
        min_costs[start_flight_index] = valid_flights[start_flight_index].fare
        children = [[] for _ in range(num_flights)]
        
        heap = Heap(num_flights,comp_1)
        for i in range(num_flights):
            if i == start_flight_index:
                fare = valid_flights[start_flight_index].fare
            else:
                fare = float('inf')
            heap.insert((fare, i))

        while not heap.is_empty():
            fare_total, flight_idx = heap.extract()
            current_flight = valid_flights[flight_idx]

            if fare_total > min_costs[flight_idx]:
                continue

            if current_flight.end_city == end_city:  
                path = []
                current = flight_idx
                while current != start_flight_index:
                    path.append(current)
                    current = children[current][0] if children[current] else start_flight_index
                path.append(start_flight_index)
                listt = path[::-1]          
                return fare_total, listt

            for neighbor_idx, fare in graph[flight_idx]:
                next_flight = valid_flights[neighbor_idx]
                new_fare = fare_total + next_flight.fare

                if new_fare < min_costs[neighbor_idx]:
                    min_costs[neighbor_idx] = new_fare
                    heap.decrease_key(neighbor_idx, new_fare)
                    children[neighbor_idx] = [flight_idx]

        return float('inf'), []
    
    def dijkstra_for_least_flight_cheap(self, start_flight_index, valid_flights, graph, end_city):
        num_flights = len(valid_flights)
        min_costs = [(float('inf'), float('inf'))] * num_flights
        min_costs[start_flight_index] = (1,valid_flights[start_flight_index].fare)
        children = [[] for _ in range(num_flights)]
        
        heap = Heap(num_flights,comp_1)
        for i in range(num_flights):
            if i == start_flight_index:
                fare = (1, valid_flights[start_flight_index].fare)
            else:
                fare = (float('inf'), float('inf'))
            heap.insert((fare, i))

        while not heap.is_empty():
            fare_total, flight_idx = heap.extract()
            current_flight = valid_flights[flight_idx]

            if fare_total > min_costs[flight_idx]:
                continue

            if current_flight.end_city == end_city:              
                path = []
                current = flight_idx
                while current != start_flight_index:
                    path.append(current)
                    current = children[current][0] if children[current] else start_flight_index
                path.append(start_flight_index)
                listt = path[::-1]          
                return fare_total, listt


            for neighbor_idx, fare in graph[flight_idx]:
                next_flight = valid_flights[neighbor_idx]
                new_fare = (fare_total[0] + 1, fare_total[1] + valid_flights[neighbor_idx].fare)

                if new_fare < min_costs[neighbor_idx]:
                    min_costs[neighbor_idx] = new_fare
                    heap.decrease_key(neighbor_idx, new_fare)
                    children[neighbor_idx] = [flight_idx]

        return (float('inf'), float('inf')), []