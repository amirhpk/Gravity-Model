The function's core algorithm involves an iterative process to balance the trip distribution based on the production and attraction potential of each zone, adjusted by the cost and deterrence factors. It iteratively calculates the balancing factors $A_i$ and $B_j$ for each zone and updates the OD matrix. The process continues until the change in the error percentage between iterations falls below the defined improvement_threshold, or the error percentage is less than the error_threshold.

Key features of the script include:
- Format and print functions for easy visualization of matrices.
- Normalization of the Origin and Destination matrices to ensure their sums are equal.
- Calculation of the OD matrix $T_{ij}$ using the updated balancing factors and deterrence matrix.
- Calculation of error percentage to monitor the convergence of the model.
- An iterative approach to update balancing factors and minimize error.

This script serves as a practical tool for applying the Gravity Model, enabling users to implement the algorithm with ease and flexibility while addressing the specific constraints associated with the transportation problem at hand.

### Deterrence Matrix Calculation

In the Gravity Model, deterrence functions play a crucial role in defining the impedance or reluctance to travel between zones. Various functional forms can be used to represent the deterrence effect based on travel cost (cij). Below are some common deterrence functions:

1. Exponential Function: This function models the deterrence effect as an exponentially decreasing function of the travel cost.
   
$$ f(c_{ij}) = \alpha \times \exp(-\beta \times c_{ij}) $$

2. Power Function: In this formulation, the deterrence decreases as a power function of the travel cost.

$$ f(c_{ij}) = \alpha \times c_{ij}^{-\beta} $$
   
3. Combined Function: This combined form uses both power and exponential components to model deterrence.

$$ f(c_{ij}) = \alpha \times c_{ij}^{\beta} \times \exp(-\gamma \times c_{ij}) $$
  
4. Lognormal Function: The lognormal function applies a squared logarithmic transformation to the travel cost.

$$ f(c_{ij}) = \alpha \times \exp(-\beta \times \ln^2(c_{ij} + 1)) $$
   
5. Top-Lognormal Function: This function modifies the lognormal form by adjusting the travel cost with a factor gamma.

$$ f(c_{ij}) = \alpha \times \exp(\beta \times \ln^2(c_{ij} / \gamma)) $$
