import sciunit
import sciunit.utils as utils

import numpy as np
from scipy.stats import power_divergence
from collections import namedtuple

PearsonResult = namedtuple('PearsonResult', ('statistic_n', 'pvalue'))
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

        dof = len(obs_values)-1  # degrees of freedom for the Chi-squared distribution
        Pearson_Result = power_divergence(obs_values, pred_values, ddof=dof, lambda_='pearson')

        utils.assert_dimensionless(Pearson_Result.statistic)
        utils.assert_dimensionless(Pearson_Result.pvalue)

        # Obtaining a score value normalized respect to the mean and std of the Chi-squared distribution
	stat = Pearson_Result.statistic
        chisq_mean = dof
        chisq_std = np.sqrt(2*dof)
        stat_n = abs(stat-chisq_mean)/chisq_std

	Pearson_result = PearsonResult(stat_n, Pearson_Result.pvalue)
        return PearsonChiSquaredScore(Pearson_result)

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return 'Pearson''s chi-squared-score = %.5f' % self.score.statistic_n
