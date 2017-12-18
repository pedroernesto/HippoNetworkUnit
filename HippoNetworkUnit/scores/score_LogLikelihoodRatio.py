import sciunit
import sciunit.utils as utils

import numpy as np
from scipy.stats import power_divergence

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

        num_obs = len(obs_values)
        Log_LikelihoodRatio_Result = power_divergence(obs_values, pred_values, ddof=num_obs - 1, lambda_='log-likelihood')

        utils.assert_dimensionless(Log_LikelihoodRatio_Result.statistic)
        utils.assert_dimensionless(Log_LikelihoodRatio_Result.pvalue)

        return Log_LikelihoodRatioScore(Log_LikelihoodRatio_Result)

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return 'Log-Likelihood-ratio score = %.5f' % self.score.statistic
