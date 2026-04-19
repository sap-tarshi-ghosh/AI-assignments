import random
import math

# --- Problem Setup ---
NUM_DEMAND_POINTS = 40
NUM_CANDIDATE_LOCATIONS = 15
NUM_FACILITIES_TO_OPEN = 3

# Generate random coordinates (x, y) on a 100x100 grid
random.seed(42) # Fixed seed for reproducible results
demand_points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(NUM_DEMAND_POINTS)]
candidate_locations = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(NUM_CANDIDATE_LOCATIONS)]

# --- Helper Functions ---
def distance(p1, p2):
    """Calculates Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_total_cost(open_facility_indices):
    """
    Calculates total transportation cost.
    Cost = Sum of distances from each demand point to its nearest open facility.
    """
    total_cost = 0
    for dp in demand_points:
        # Find distance to the closest open facility
        min_dist = min([distance(dp, candidate_locations[i]) for i in open_facility_indices])
        total_cost += min_dist
    return total_cost

def get_neighbor(current_open_indices):
    """
    Generates a neighboring solution by swapping one currently 
    open facility with one currently closed facility.
    """
    neighbor = list(current_open_indices)
    
    # 1. Pick a random open facility to close
    idx_to_remove = random.choice(neighbor)
    neighbor.remove(idx_to_remove)
    
    # 2. Pick a random closed facility to open
    closed_indices = [i for i in range(NUM_CANDIDATE_LOCATIONS) if i not in current_open_indices]
    idx_to_add = random.choice(closed_indices)
    neighbor.append(idx_to_add)
    
    return neighbor

# --- Simulated Annealing Algorithm ---
def simulated_annealing(initial_temp=1000.0, cooling_rate=0.99, min_temp=0.1):
    # 1. Initial State: Randomly pick 'k' facilities to open
    current_solution = random.sample(range(NUM_CANDIDATE_LOCATIONS), NUM_FACILITIES_TO_OPEN)
    current_cost = calculate_total_cost(current_solution)
    
    # Track the best configuration found
    best_solution = list(current_solution)
    best_cost = current_cost
    
    temp = initial_temp
    
    # 2. Main Annealing Loop
    while temp > min_temp:
        # Generate a neighbor (swap one facility)
        neighbor_solution = get_neighbor(current_solution)
        neighbor_cost = calculate_total_cost(neighbor_solution)
        
        # Calculate change in cost (We are MINIMIZING, so lower is better)
        delta_e = neighbor_cost - current_cost
        
        # 3. Acceptance Probability Logic
        if delta_e < 0:
            # If neighbor is better (lower cost), accept unconditionally
            current_solution = neighbor_solution
            current_cost = neighbor_cost
            
            # Update global best if necessary
            if current_cost < best_cost:
                best_solution = list(current_solution)
                best_cost = current_cost
        else:
            # If neighbor is worse, accept with a probability based on temperature
            # delta_e is positive here. e^(-positive / positive) = value between 0 and 1
            acceptance_probability = math.exp(-delta_e / temp)
            if random.random() < acceptance_probability:
                current_solution = neighbor_solution
                current_cost = neighbor_cost
                
        # 4. Cooling
        temp *= cooling_rate
        
    return best_solution, best_cost

# --- Execution ---
if __name__ == "__main__":
    best_facilities, best_cost = simulated_annealing()
    
    print("--- Simulated Annealing: Facility Location Problem ---")
    print(f"Total Demand Points: {NUM_DEMAND_POINTS}")
    print(f"Total Candidate Facilities: {NUM_CANDIDATE_LOCATIONS}")
    print(f"Facilities Opened: {NUM_FACILITIES_TO_OPEN}\n")
    
    print(f"Optimal Facility Indices: {best_facilities}")
    print(f"Minimum Total Transportation Cost: {best_cost:.2f}\n")
    
    print("Selected Facility Coordinates:")
    for idx in best_facilities:
        x, y = candidate_locations[idx]
        print(f"- Facility {idx:02d}: (X: {x:.2f}, Y: {y:.2f})")