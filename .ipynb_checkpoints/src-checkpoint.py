from scipy.stats import binom, norm
import numpy as np
from scipy.stats import binom, norm
import numpy as np

def bayesian_3pt_percentage_with_credible_interval(historical_pct, current_attempts, current_made, prior_std=0.05, credible_level=0.95):
    """
    Calculate the Bayesian 3-point shooting percentage along with a credible interval.

    :param historical_pct: Player's historical 3-point shooting percentage.
    :param current_attempts: Number of 3-point attempts in the current season.
    :param current_made: Number of successful 3-point shots in the current season.
    :param prior_std: Standard deviation for the prior distribution (default 0.05).
    :param credible_level: Credible level for the interval (default 0.95).
    :return: Bayesian 3-point shooting percentage estimate and credible interval.
    """
    # Step 1: Establish a Prior Distribution
    prior_distribution = norm(historical_pct, prior_std)

    # Step 3: Choose a Likelihood Function
    likelihood = binom(current_attempts, current_made/current_attempts)

    # Step 4: Update the Prior with Current Data (Posterior Distribution)
    percentage_values = np.linspace(0, 1, 1000)  # Possible 3-point percentages
    posterior_probabilities = likelihood.pmf(current_made) * prior_distribution.pdf(percentage_values)

    # Check if the sum of posterior probabilities is very small or zero
    sum_posterior = np.sum(posterior_probabilities)
    if sum_posterior < 1e-8:
        raise ValueError("Sum of posterior probabilities is too small, check your prior_std or data.")

    # Normalize the posterior probabilities
    posterior_probabilities /= sum_posterior

    # Step 5: Calculate the Bayesian 3-Point Percentage
    bayesian_estimate = np.sum(percentage_values * posterior_probabilities)

    # Calculate the credible interval
    cumulative_probabilities = np.cumsum(posterior_probabilities)
    lower_bound_idx = np.where(cumulative_probabilities >= (1 - credible_level) / 2)[0][0]
    upper_bound_idx = np.where(cumulative_probabilities >= 1 - (1 - credible_level) / 2)[0][0]
    credible_interval = (percentage_values[lower_bound_idx], percentage_values[upper_bound_idx])

    return bayesian_estimate, credible_interval

