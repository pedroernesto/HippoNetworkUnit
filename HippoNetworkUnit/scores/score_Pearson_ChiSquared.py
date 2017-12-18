import sciunit
import sciunit.utils as utils

import numpy as np
from scipy.stats import power_divergence

class PearsonChiSquaredScore(sciunit.Score):
    """
    A Pearson score. A float giving the result of
    a Pearson's chi-squared goodness-of-fit test
    """
    
    _allowed_types = (float,)

    _description = ('A Pearson score. A float giving the result'
                    'of a Pearson''s chi-squared goodness-of-fit test')

    @classmethod
    def compute(cls, observation, prediction):
        """
        Computes a Pearson's chi-squared score from an observation and a prediction.
        """

        obs_values = observation[~np.isnan(observation)]
        pred_values = prediction[~np.isnan(prediction)]

        num_obs = len(obs_values)
        Pearson_Result = power_divergence(obs_values, pred_values, ddof=num_obs - 1, lambda_='pearson')

        utils.assert_dimensionless(Pearson_Result.statistic)
        utils.assert_dimensionless(Pearson_Result.pvalue)

        return PearsonChiSquaredScore(Pearson_Result)

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return 'Pearson''s chi-squared-score = %.5f' % self.score.statistic
