import heapq
import math

# Define the A* node class
class Node:
    def __init__(self, position, g_cost, h_cost):
        self.position = position  # Coordinates (lat, long)
        self.g_cost = g_cost  # Cost from start to this node
        self.h_cost = h_cost  # Heuristic cost from this node to goal
        self.f_cost = g_cost + h_cost  # Total cost
        self.parent = None  # To trace the path

    def __lt__(self, other):
        return self.f_cost < other.f_cost

# Heuristic function (using Euclidean distance here)
def heuristic(node_a, node_b):
    return math.sqrt((node_a[0] - node_b[0]) ** 2 + (node_a[1] - node_b[1]) ** 2)

# Define the Ship class to store vessel data
class Ship:
    def __init__(self, speed_knots, fuel_capacity_liters, fuel_consumption_per_km, cargo_capacity):
        self.speed_knots = speed_knots  # Ship speed in knots (nautical miles per hour)
        self.fuel_capacity_liters = fuel_capacity_liters  # Total fuel capacity
        self.fuel_consumption_per_km = fuel_consumption_per_km  # Fuel consumption in liters per kilometer
        self.cargo_capacity = cargo_capacity  # Maximum cargo capacity in tons
        self.remaining_fuel = fuel_capacity_liters  # Start with full tank
    
    def calculate_travel_time(self, distance_km):
        """Calculate travel time based on speed (in km/h)."""
        speed_kmh = self.speed_knots * 1.852  # Convert knots to km/h
        time_hours = distance_km / speed_kmh
        return time_hours
    
    def calculate_fuel_required(self, distance_km):
        """Calculate fuel required for a given distance."""
        fuel_needed = distance_km * self.fuel_consumption_per_km
        return fuel_needed
    
    def update_fuel(self, distance_km):
        """Update remaining fuel after traveling a given distance."""
        fuel_needed = self.calculate_fuel_required(distance_km)
        if fuel_needed <= self.remaining_fuel:
            self.remaining_fuel -= fuel_needed
        else:
            print("Not enough fuel for the journey!")
            return False
        return True

# Define a function to model traffic conditions
def get_traffic_factor():
    """Simulate traffic conditions affecting travel time."""
    traffic_conditions = {
        'low': 1.0,    # No traffic, normal speed
        'moderate': 1.2,  # Some traffic, 20% slower
        'heavy': 1.5   # Heavy traffic, 50% slower
    }
    # You can add logic to dynamically change traffic based on time, etc.
    current_traffic = 'moderate'  # Can be dynamic or input from the user
    return traffic_conditions[current_traffic]

# A* algorithm
def a_star(start, goal, ship, graph):
    open_list = []  # Priority queue (min-heap)
    closed_list = set()  # Explored nodes

    # Start node with g_cost=0, heuristic distance to the goal
    start_node = Node(start, 0, heuristic(start, goal))
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        # If we reach the goal, reconstruct the path
        if current_node.position == goal:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Reverse the path to go from start to goal

        closed_list.add(current_node.position)

        # Explore neighbors
        neighbors = graph[current_node.position]  # Adjacent nodes

        for neighbor_position, distance in neighbors:
            if neighbor_position in closed_list:
                continue

            # Calculate g_cost (cost from start to neighbor)
            travel_time = ship.calculate_travel_time(distance)  # Time to travel this distance
            fuel_needed = ship.calculate_fuel_required(distance)  # Fuel required for this distance
            traffic_factor = get_traffic_factor()  # Traffic impact
            total_cost = travel_time * traffic_factor + fuel_needed  # Weighted cost

            g_cost = current_node.g_cost + total_cost
            h_cost = heuristic(neighbor_position, goal)
            f_cost = g_cost + h_cost

            # Create neighbor node
            neighbor_node = Node(neighbor_position, g_cost, h_cost)
            neighbor_node.parent = current_node

            # Add to the open list if it's a better path
            heapq.heappush(open_list, neighbor_node)

    return None  # No path found

# Example graph with distances between points (simple grid with distances)
graph = {
    (0, 0): [((0, 1), 10), ((1, 0), 20)],
    (0, 1): [((0, 0), 10), ((1, 1), 15)],
    (1, 0): [((0, 0), 20), ((1, 1), 10)],
    (1, 1): [((0, 1), 15), ((1, 0), 10)]
}

# Get user input for ship details
speed_knots = float(input("Enter ship speed in knots: "))
fuel_capacity_liters = float(input("Enter fuel capacity in liters: "))
fuel_consumption_per_km = float(input("Enter fuel consumption per km (liters): "))
cargo_capacity = float(input("Enter cargo capacity in tons: "))

# Initialize the ship with user inputs
user_ship = Ship(
    speed_knots=speed_knots,
    fuel_capacity_liters=fuel_capacity_liters,
    fuel_consumption_per_km=fuel_consumption_per_km,
    cargo_capacity=cargo_capacity
)

# Define start and goal positions
start_position = (0, 0)
goal_position = (1, 1)

# Run the A* algorithm
path = a_star(start_position, goal_position, user_ship, graph)

if path:
    print("Optimal path:", path)
else:
    print("No valid path found due to fuel or other constraints.")
