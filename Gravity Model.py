import numpy as np
import pandas as pd

# Define the cost matrix: This represents the cost or difficulty of travel between zones.
# Each row corresponds to an origin zone, and each column corresponds to a destination zone.
# A value of 0 indicates no direct connection between the zones.
cost_matrix = np.array([
    [0, 0, 50, 0, 0],
    [0, 0, 60, 0, 0],
    [0, 0, 0, 30, 0],
    [20, 0, 80, 0, 20],
    [0, 70, 90, 10, 0]
], dtype=float)

# Define the supply and demand for trips between zones:
# origin_supply: Number of trips originating from each zone.
# destination_demand: Number of trips attracted to each zone.
origin_supply = np.array([80, 150, 100, 160, 180], dtype=float)
destination_demand = np.array([100, 90, 320, 80, 300], dtype=float)

# Ensure balance between total trips supplied (origin_supply) and total trips attracted (destination_demand).
# If there is an imbalance, scale the destination_demand to match the total origin_supply.
total_supply = origin_supply.sum()
total_demand = destination_demand.sum()
if total_supply != total_demand:
    # Calculate the ratio to adjust the demand values proportionally.
    scaling_factor = total_supply / total_demand
    destination_demand = destination_demand * scaling_factor

# Parameters for the deterrence function:
# coefficient_a: This scales the deterrence value and determines its magnitude.
# coefficient_b: This determines how strongly the deterrence decreases as the cost increases.
coefficient_a = 0.05
coefficient_b = 0.2

# Define the deterrence function:
# This function calculates the deterrence value for a given cost. Deterrence represents how unattractive
# a destination becomes as the travel cost increases. The formula uses a log-normal distribution.
def deterrence_func(matrix):
    return coefficient_a * np.exp(-coefficient_b * np.power(np.log(matrix + 1), 2))

# Implement the gravity model algorithm:
# This algorithm calculates the distribution of trips between zones based on the cost matrix,
# the origin supply, and the destination demand. It iteratively balances the matrix until
# the row and column sums match the supply and demand constraints.
def gravity_model(matrix, supply, demand, missing_value_substitute, max_steps=1000, error_limit=1e-3):
    num_zones = len(supply)  # Number of zones (rows/columns in the cost matrix).
    trip_distribution = np.zeros((num_zones, num_zones), dtype=float)  # Initialize trip matrix with zeros.
    balance_coeff = np.ones(num_zones, dtype=float)  # Initialize balancing coefficients for destinations.
    deterrence = np.vectorize(deterrence_func)(matrix)  # Apply deterrence function to cost matrix.

    # Handle missing connections by substituting their deterrence values with a small number or zero.
    deterrence[matrix == 0] = missing_value_substitute

    for count in range(max_steps):  # Iterate to refine the trip distribution matrix.
        # Calculate scaling factors for origins to ensure supply constraints are met.
        scaling_factors = 1 / (np.dot(deterrence, balance_coeff * demand) + 1e-9)

        # Update the trip distribution matrix based on the scaling factors, demand, and deterrence.
        for src in range(num_zones):
            for dest in range(num_zones):
                trip_distribution[src, dest] = (
                    scaling_factors[src]
                    * supply[src]
                    * balance_coeff[dest]
                    * demand[dest]
                    * deterrence[src, dest]
                )

        # Update balancing coefficients for destinations to ensure demand constraints are met.
        updated_balance_coeff = 1 / (np.dot(deterrence.T, scaling_factors * supply) + 1e-9)

        # Calculate the total error as the sum of the mismatches in row and column totals.
        total_error = (
            np.sum(np.abs(supply - trip_distribution.sum(axis=1)))  # Row-wise mismatch
            + np.sum(np.abs(demand - trip_distribution.sum(axis=0)))  # Column-wise mismatch
        ) / supply.sum()

        # Check if the total error is below the specified threshold for convergence.
        if total_error < error_limit:
            print(f"Successfully reached convergence after {count + 1} iterations.")
            break

        # Update the balance coefficients for the next iteration.
        balance_coeff = updated_balance_coeff

    else:
        # If the maximum number of iterations is reached, print a warning message.
        print("The process didn't converge within the allowed iteration count.")

    # Print the final trip distribution matrix, formatted with appropriate labels for readability.
    labels = ["A", "B", "C", "D", "E"]  # Labels for zones.
    result_df = pd.DataFrame(trip_distribution, index=labels, columns=labels)
    print("\nResulting Trip Distribution Matrix:")
    print(result_df.round(4))  # Round to 4 decimal places for clarity.
    print("Computed Error Value =", total_error)  # Print the final computed error.

# Execute the gravity model with different substitutes for missing connections:
# First run: Use 0 as the deterrence value for missing connections.
gravity_model(cost_matrix, origin_supply, destination_demand, missing_value_substitute=0)

# Second run: Use a very small value (1e-6) as the deterrence value for missing connections.
gravity_model(cost_matrix, origin_supply, destination_demand, missing_value_substitute=1e-6)
# No Convergence in the First Run
#In the first execution, the model failed to achieve an error lower than the threshold within the allowed number of iterations.
#This was due to the lack of connections between some zones, which prevented the algorithm from generating a proper trip distribution.
#The computed error value (Computed Error Value = 0.4212) confirms this issue and indicates that the problem cannot be solved with the initial parameters.
# Adjusting Deterrence for Unconnected Routes
#In the second execution, the deterrence value for unconnected routes (epsilon) was adjusted to a small value such as 10−6.
#This adjustment allowed the model to reach an error below the threshold, successfully converging after 19 iterations. However, in the final trip matrix, positive values appeared for routes without any direct connection, which invalidates the solution.
# No Valid Solution for the Problem
#The results demonstrate that with the current setup, the problem lacks a valid solution.
#Even with adjustments to the deterrence parameters, the presence of unconnected routes results in a final solution that cannot accurately reflect the true distribution of trips. 
#Assigning positive values to non-existent routes violates the logic of the model.
