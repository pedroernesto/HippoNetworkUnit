import sciunit
import sciunit.utils as utils

import numpy as np
from scipy.stats import power_divergence
from collections import namedtuple

Log_LikelihoodRatioResult = namedtuple('Log_LikelihoodRatioResult', ('statistic_n', 'pvalue'))
class Log_LikelihoodRatioScore(sciunit.Score):
    """
    A Log-Likelihood Ratio score. A float giving the result of
    a Log-Likelihood goodness-of-fit test. Also known as the G-test
    """
    
    _allowed_types = (float,)

    _description = ('A Log-Likelihood Ratio score. A float giving the result of'
                    'a Log-Likelihood goodness-of-fit test. Also known as the G-test')

    @classmethod
    def compute(cls, observation, prediction):
        """
        Computes a Log-Likelihood Ratio score from an observation and a prediction.
        """

        obs_values = observation[~np.isnan(observation)]
        pred_values = prediction[~np.isnan(prediction)]

        dof = len(obs_values)-1  # degrees of freedom for the Chi-squared distribution
        Log_LikelihoodRatio_Result = power_divergence(obs_values, pred_values, ddof=dof, lambda_='log-likelihood')

        utils.assert_dimensionless(Log_LikelihoodRatio_Result.statistic)
        utils.assert_dimensionless(Log_LikelihoodRatio_Result.pvalue)

        # Obtaining a score value normalized respect to the mean and std of the Chi-squared distribution
	stat = Log_LikelihoodRatio_Result.statistic
        chisq_mean = dof
        chisq_std = np.sqrt(2*dof)
        stat_n = abs(stat-chisq_mean)/chisq_std

	Log_LikelihoodRatio_result = Log_LikelihoodRatioResult(stat_n, Log_LikelihoodRatio_Result.pvalue)
        return Log_LikelihoodRatioScore(Log_LikelihoodRatio_result)

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return 'Log-Likelihood-ratio score = %.5f' % self.score.statistic_n
