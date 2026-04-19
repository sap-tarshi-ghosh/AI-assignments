import random
import math

# --- Problem Definition ---
# Define items as a list of dictionaries with weights and values
items = [
    {"weight": 10, "value": 60},
    {"weight": 20, "value": 100},
    {"weight": 30, "value": 120},
    {"weight": 15, "value": 75},
    {"weight": 25, "value": 90}
]
MAX_CAPACITY = 50

# --- Helper Functions ---
def calculate_fitness(solution):
    """
    Calculates the total value of the knapsack. 
    Applies a harsh penalty if the weight exceeds the maximum capacity.
    """
    total_weight = 0
    total_value = 0
    
    for i in range(len(solution)):
        if solution[i] == 1:
            total_weight += items[i]["weight"]
            total_value += items[i]["value"]
            
    # Penalty for exceeding capacity to guide the algorithm back to valid states
    if total_weight > MAX_CAPACITY:
        return -100 * (total_weight - MAX_CAPACITY) 
    
    return total_value

def get_neighbor(solution):
    """Generates a neighboring solution by flipping one random bit (item inclusion)."""
    neighbor = list(solution)
    flip_index = random.randint(0, len(solution) - 1)
    neighbor[flip_index] = 1 - neighbor[flip_index] # Flip 0 to 1, or 1 to 0
    return neighbor

# --- Simulated Annealing Algorithm ---
def simulated_annealing(items, capacity, initial_temp=1000.0, cooling_rate=0.95, min_temp=0.1):
    n = len(items)
    
    # 1. Start with a random initial solution (binary array)
    current_solution = [random.choice([0, 1]) for _ in range(n)]
    current_fitness = calculate_fitness(current_solution)
    
    # Track the best valid solution found so far
    best_solution = list(current_solution)
    best_fitness = current_fitness
    
    temp = initial_temp
    
    # 2. Main loop with cooling schedule
    while temp > min_temp:
        # Generate a neighbor
        neighbor_solution = get_neighbor(current_solution)
        neighbor_fitness = calculate_fitness(neighbor_solution)
        
        # Calculate change in fitness (we are MAXIMIZING value)
        delta_e = neighbor_fitness - current_fitness
        
        # 3. Acceptance Probability Logic
        if delta_e > 0:
            # If the neighbor is better, always accept it
            current_solution = neighbor_solution
            current_fitness = neighbor_fitness
            
            # Update global best if this is the highest valid score we've seen
            if current_fitness > best_fitness:
                best_solution = list(current_solution)
                best_fitness = current_fitness
        else:
            # If the neighbor is worse, accept it with a certain probability
            # Note: delta_e is negative here, so exp(negative / positive) is between 0 and 1
            acceptance_probability = math.exp(delta_e / temp)
            if random.random() < acceptance_probability:
                current_solution = neighbor_solution
                current_fitness = neighbor_fitness
                
        # 4. Apply Cooling Schedule
        temp *= cooling_rate
        
    return best_solution, best_fitness

# --- Execution ---
if __name__ == "__main__":
    best_combo, best_val = simulated_annealing(items, MAX_CAPACITY)
    
    print("--- Simulated Annealing: 0/1 Knapsack ---")
    print(f"Maximum Capacity: {MAX_CAPACITY}")
    print(f"Best Solution (Binary): {best_combo}")
    print(f"Total Value Achieved: {best_val}")
    
    # Print out the exact items picked
    final_weight = 0
    print("\nItems Selected:")
    for i in range(len(best_combo)):
        if best_combo[i] == 1:
            print(f"- Item {i+1} (Weight: {items[i]['weight']}, Value: {items[i]['value']})")
            final_weight += items[i]["weight"]
    print(f"Total Final Weight: {final_weight}")