import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# --- 1. Problem Setup & Data Loading ---
data = load_breast_cancer()
X = data.data
y = data.target

# Split data to evaluate feature subsets fairly
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

NUM_FEATURES = X.shape[1]
NUM_PARTICLES = 30
MAX_ITERATIONS = 50

# BPSO Parameters
W = 0.9      # Inertia weight (preserves previous velocity)
C1 = 2.0     # Cognitive coefficient (explores personal best)
C2 = 2.0     # Social coefficient (explores global best)
V_MAX = 6.0  # Maximum velocity to prevent sigmoid saturation

# --- 2. Helper Functions ---
def calculate_fitness(particle_position):
    """
    Evaluates the fitness of a binary feature mask.
    Fitness is the classification accuracy using only the selected features.
    """
    # Find indices where the particle has a '1' (feature selected)
    selected_features = np.where(particle_position == 1)[0]
    
    # If no features are selected, return a terrible fitness score
    if len(selected_features) == 0:
        return 0.0
    
    # Subset the training and testing data
    X_train_subset = X_train[:, selected_features]
    X_test_subset = X_test[:, selected_features]
    
    # Train and evaluate a simple classifier
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train_subset, y_train)
    predictions = clf.predict(X_test_subset)
    
    return accuracy_score(y_test, predictions)

def sigmoid(x):
    """Squashing function to map continuous velocities to probabilities."""
    return 1 / (1 + np.exp(-x))

# --- 3. Binary PSO Algorithm ---
def run_bpso():
    # Initialize particles: Random binary positions and zero starting velocities
    positions = np.random.randint(2, size=(NUM_PARTICLES, NUM_FEATURES))
    velocities = np.zeros((NUM_PARTICLES, NUM_FEATURES))
    
    # Track Personal Best (pbest) for each particle
    pbest_positions = np.copy(positions)
    pbest_scores = np.array([calculate_fitness(p) for p in positions])
    
    # Track Global Best (gbest) across the whole swarm
    gbest_index = np.argmax(pbest_scores)
    gbest_position = np.copy(pbest_positions[gbest_index])
    gbest_score = pbest_scores[gbest_index]
    
    # Main Loop
    for iteration in range(MAX_ITERATIONS):
        for i in range(NUM_PARTICLES):
            # 1. Update Velocity
            r1 = np.random.rand(NUM_FEATURES)
            r2 = np.random.rand(NUM_FEATURES)
            
            cognitive_velocity = C1 * r1 * (pbest_positions[i] - positions[i])
            social_velocity = C2 * r2 * (gbest_position - positions[i])
            velocities[i] = (W * velocities[i]) + cognitive_velocity + social_velocity
            
            # Clamp velocity to prevent extreme values in the sigmoid function
            velocities[i] = np.clip(velocities[i], -V_MAX, V_MAX)
            
            # 2. Update Position (Binary transformation)
            probabilities = sigmoid(velocities[i])
            random_thresholds = np.random.rand(NUM_FEATURES)
            
            # If probability > random number, select feature (1), else drop (0)
            positions[i] = (probabilities > random_thresholds).astype(int)
            
            # 3. Evaluate new fitness
            current_fitness = calculate_fitness(positions[i])
            
            # 4. Update Personal Best
            if current_fitness > pbest_scores[i]:
                pbest_scores[i] = current_fitness
                pbest_positions[i] = np.copy(positions[i])
                
                # 5. Update Global Best
                if current_fitness > gbest_score:
                    gbest_score = current_fitness
                    gbest_position = np.copy(positions[i])
        
        # Optional: Print progress every 10 iterations
        if (iteration + 1) % 10 == 0:
            print(f"Iteration {iteration + 1}/{MAX_ITERATIONS} - Best Accuracy: {gbest_score:.4f} "
                  f"with {np.sum(gbest_position)} features.")
            
    return gbest_position, gbest_score

# --- 4. Execution ---
if __name__ == "__main__":
    print("--- Starting Binary PSO for Feature Selection ---")
    
    # Baseline: Accuracy using ALL features
    baseline_clf = DecisionTreeClassifier(random_state=42)
    baseline_clf.fit(X_train, y_train)
    baseline_acc = accuracy_score(y_test, baseline_clf.predict(X_test))
    
    print(f"Baseline Accuracy (All {NUM_FEATURES} features): {baseline_acc:.4f}\n")
    
    # Run PSO
    best_features, best_accuracy = run_bpso()
    
    print("\n--- PSO Optimization Complete ---")
    print(f"Optimized Accuracy: {best_accuracy:.4f}")
    print(f"Number of Features Selected: {np.sum(best_features)} out of {NUM_FEATURES}")
    print(f"Feature Mask: {best_features}")