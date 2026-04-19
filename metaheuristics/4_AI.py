import random
import math

# --- Problem Definition ---
# Represent assets with expected returns and risks (standard deviation)
assets = [
    {"name": "Tech Stock (High Risk/Return)", "return": 0.15, "risk": 0.22},
    {"name": "Index Fund (Med Risk/Return)",  "return": 0.10, "risk": 0.15},
    {"name": "Corporate Bond (Low Risk)",     "return": 0.06, "risk": 0.08},
    {"name": "Govt Bond (Very Low Risk)",     "return": 0.03, "risk": 0.02},
    {"name": "Emerging Market (High Risk)",   "return": 0.18, "risk": 0.28}
]

NUM_ASSETS = len(assets)
POPULATION_SIZE = 100
GENERATIONS = 150
MUTATION_RATE = 0.1

# --- Helper Functions ---
def normalize(chromosome):
    """Ensures all portfolio weights sum to exactly 1.0 (100% allocation)."""
    total = sum(chromosome)
    if total == 0: 
        return [1.0 / NUM_ASSETS] * NUM_ASSETS
    return [w / total for w in chromosome]

def calculate_fitness(chromosome):
    """
    Evaluates a portfolio balancing return and risk.
    Uses Expected Return / Portfolio Risk (similar to Sharpe Ratio).
    """
    normalized_weights = normalize(chromosome)
    
    # Calculate Expected Portfolio Return
    expected_return = sum(w * a["return"] for w, a in zip(normalized_weights, assets))
    
    # Calculate Simplified Portfolio Risk 
    # (Assuming zero correlation between assets for simplicity in this assignment)
    variance = sum((w * a["risk"])**2 for w, a in zip(normalized_weights, assets))
    portfolio_risk = math.sqrt(variance)
    
    # Fitness Function: Maximize return per unit of risk
    # Added tiny value (1e-6) to prevent division by zero
    return expected_return / (portfolio_risk + 1e-6)

# --- Genetic Algorithm Operators ---
def select_parent(population, fitness_scores):
    """Tournament Selection: Pick a few random individuals and return the best one."""
    tournament_size = 3
    best_index = random.randint(0, len(population) - 1)
    
    for _ in range(tournament_size - 1):
        contender_index = random.randint(0, len(population) - 1)
        if fitness_scores[contender_index] > fitness_scores[best_index]:
            best_index = contender_index
            
    return population[best_index]

def crossover(parent1, parent2):
    """Arithmetic Crossover: Averages the genes (weights) of two parents."""
    alpha = random.random() # Random blending factor between 0 and 1
    child1 = [alpha * p1 + (1 - alpha) * p2 for p1, p2 in zip(parent1, parent2)]
    child2 = [(1 - alpha) * p1 + alpha * p2 for p1, p2 in zip(parent1, parent2)]
    return child1, child2

def mutate(chromosome):
    """Mutation: Adds a random small adjustment to a random asset's weight."""
    mutated = list(chromosome)
    for i in range(len(mutated)):
        if random.random() < MUTATION_RATE:
            # Introduce a random shift between -10% and +10%
            shift = random.uniform(-0.1, 0.1)
            mutated[i] = max(0, mutated[i] + shift) # Keep weights non-negative
    return mutated

# --- Main Genetic Algorithm ---
def optimize_portfolio():
    # 1. Initialization
    # Create random initial population
    population = [[random.random() for _ in range(NUM_ASSETS)] for _ in range(POPULATION_SIZE)]
    population = [normalize(ind) for ind in population]
    
    best_overall_solution = None
    best_overall_fitness = -1

    # 2. Evolution Loop
    for generation in range(GENERATIONS):
        # Evaluate fitness
        fitness_scores = [calculate_fitness(ind) for ind in population]
        
        # Track the best solution
        max_fitness = max(fitness_scores)
        if max_fitness > best_overall_fitness:
            best_overall_fitness = max_fitness
            best_overall_solution = population[fitness_scores.index(max_fitness)]
            
        # Create next generation
        new_population = []
        
        # Elitism: Keep the best individual from the current generation
        new_population.append(population[fitness_scores.index(max_fitness)])
        
        # Fill the rest of the new population
        while len(new_population) < POPULATION_SIZE:
            # Selection
            parent1 = select_parent(population, fitness_scores)
            parent2 = select_parent(population, fitness_scores)
            
            # Crossover
            child1, child2 = crossover(parent1, parent2)
            
            # Mutation & Normalization
            new_population.append(normalize(mutate(child1)))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(normalize(mutate(child2)))
                
        population = new_population

    return normalize(best_overall_solution), best_overall_fitness

# --- Execution ---
if __name__ == "__main__":
    best_portfolio, best_score = optimize_portfolio()
    
    print("--- Genetic Algorithm: Portfolio Optimization ---")
    print(f"Best Fitness Score (Return/Risk Ratio): {best_score:.4f}\n")
    print("Optimal Asset Allocation:")
    
    total_return = 0
    total_variance = 0
    
    for w, asset in zip(best_portfolio, assets):
        allocation_pct = w * 100
        print(f"- {asset['name']:<30} : {allocation_pct:05.2f}%")
        total_return += w * asset["return"]
        total_variance += (w * asset["risk"])**2
        
    print("-" * 40)
    print(f"Expected Portfolio Return: {total_return * 100:.2f}%")
    print(f"Expected Portfolio Risk:   {math.sqrt(total_variance) * 100:.2f}%")