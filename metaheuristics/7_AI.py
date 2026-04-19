import numpy as np
import random

# --- Problem Setup ---
np.random.seed(42)
random.seed(42)

NUM_CUSTOMERS = 15
VEHICLE_CAPACITY = 50

# Generate coordinates. Index 0 is the Depot.
locations = np.random.rand(NUM_CUSTOMERS + 1, 2) * 100

# Generate demands (Depot has 0 demand)
demands = np.random.randint(5, 20, size=NUM_CUSTOMERS + 1)
demands[0] = 0 

# Create Distance Matrix
num_nodes = len(locations)
distances = np.zeros((num_nodes, num_nodes))
for i in range(num_nodes):
    for j in range(num_nodes):
        # Add a tiny value to prevent division by zero later
        distances[i][j] = np.linalg.norm(locations[i] - locations[j]) + 1e-6 

# --- ACO Parameters ---
NUM_ANTS = 20
MAX_ITERATIONS = 100
ALPHA = 1.0       # Pheromone importance
BETA = 2.0        # Visibility (distance) importance
EVAPORATION = 0.1 # Pheromone evaporation rate
Q = 100.0         # Pheromone deposit multiplier

# Initialize Pheromone Matrix
pheromones = np.ones((num_nodes, num_nodes))

# --- Helper Functions ---
def construct_ant_tour():
    """Simulates one ant building a valid VRP route."""
    tour = []       # The final list of visited nodes (includes depot returns)
    unvisited = set(range(1, num_nodes))
    
    current_node = 0 # Start at Depot
    current_load = 0
    
    while unvisited:
        # Filter unvisited nodes that the vehicle can still carry
        valid_next_nodes = [node for node in unvisited if current_load + demands[node] <= VEHICLE_CAPACITY]
        
        if not valid_next_nodes:
            # Capacity reached: Return to Depot, reset load, and continue
            tour.append(0)
            current_node = 0
            current_load = 0
            continue
            
        # Calculate transition probabilities for valid nodes
        probabilities = []
        for next_node in valid_next_nodes:
            tau = pheromones[current_node][next_node] ** ALPHA
            eta = (1.0 / distances[current_node][next_node]) ** BETA
            probabilities.append(tau * eta)
            
        # Normalize to create a probability distribution
        prob_sum = sum(probabilities)
        probabilities = [p / prob_sum for p in probabilities]
        
        # Select the next node based on probabilities (Roulette Wheel Selection)
        chosen_node = random.choices(valid_next_nodes, weights=probabilities)[0]
        
        # Move to chosen node
        tour.append(chosen_node)
        unvisited.remove(chosen_node)
        current_node = chosen_node
        current_load += demands[chosen_node]
        
    # Return to depot at the very end
    if tour[-1] != 0:
        tour.append(0)
        
    return tour

def calculate_tour_distance(tour):
    """Calculates the total distance of a route."""
    dist = distances[0][tour[0]] # Distance from depot to first node
    for i in range(len(tour) - 1):
        dist += distances[tour[i]][tour[i+1]]
    return dist

# --- Main ACO Algorithm ---
def run_vrp_aco():
    global pheromones
    best_overall_tour = None
    best_overall_distance = float('inf')
    
    for iteration in range(MAX_ITERATIONS):
        all_tours = []
        all_distances = []
        
        # 1. All ants construct their tours
        for _ in range(NUM_ANTS):
            tour = construct_ant_tour()
            distance = calculate_tour_distance(tour)
            all_tours.append(tour)
            all_distances.append(distance)
            
            # Track global best
            if distance < best_overall_distance:
                best_overall_distance = distance
                best_overall_tour = tour
                
        # 2. Global Pheromone Evaporation
        pheromones *= (1.0 - EVAPORATION)
        
        # 3. Pheromone Deposit (Better routes get more pheromones)
        for tour, distance in zip(all_tours, all_distances):
            deposit_amount = Q / distance
            # Add pheromones to the edges used in this tour
            prev_node = 0
            for node in tour:
                pheromones[prev_node][node] += deposit_amount
                pheromones[node][prev_node] += deposit_amount # Assuming symmetric paths
                prev_node = node
                
        if (iteration + 1) % 20 == 0:
            print(f"Iteration {iteration + 1}/{MAX_ITERATIONS} - Best Distance: {best_overall_distance:.2f}")
            
    return best_overall_tour, best_overall_distance

# --- Execution ---
if __name__ == "__main__":
    print("--- ACO: Vehicle Routing Problem ---")
    print(f"Total Customers: {NUM_CUSTOMERS}")
    print(f"Vehicle Capacity: {VEHICLE_CAPACITY}\n")
    
    best_route, min_distance = run_vrp_aco()
    
    print("\n--- Optimization Complete ---")
    print(f"Minimum Distance Achieved: {min_distance:.2f}")
    
    # Format the route nicely
    formatted_route = "Depot"
    for node in best_route:
        if node == 0:
            formatted_route += " -> [Depot] -> "
        else:
            formatted_route += f"C{node}(d:{demands[node]}) -> "
    print(f"\nOptimal Route:\n{formatted_route.strip(' -> ')}")