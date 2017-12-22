import sciunit
import sciunit.utils as utils

import numpy as np
import scipy
from collections import namedtuple

FreemanTukeyResult = namedtuple('FreemanTukeyResult', ('statistic_n', 'pvalue'))
class FreemanTukey2Score(sciunit.Score):
    """
    A Freeman-Tukey score.A float giving the result of a Freeman-Tukey goodness-of-fit test.
    It is useful in the case of small counts (frequencies)
    """
    
    _allowed_types = (tuple,)

    _description = ('A Freeman-Tukey score. A float giving the result of a Freeman-Tukey goodness-of-fit test.'
                    'It is useful in the case of small counts (frequencies)')

    @classmethod
    def compute(cls, observation, prediction):
        """
        Computes a Freeman-Tukey score from an observation and a prediction.
        """

        obs_values = observation[~np.isnan(observation)]
        pred_values = prediction[~np.isnan(prediction)]

        dof = len(obs_values)-1  # degrees of freedom for the Chi-squared distribution
        stat = sum((np.sqrt(pred_values) + np.sqrt(pred_values+1) - np.sqrt(4*obs_values+1))**2)
        pval = scipy.stats.distributions.chi2.sf(stat, dof)

        stat = utils.assert_dimensionless(stat)
        pval = utils.assert_dimensionless(pval)

        # Obtaining a score value normalized respect to the mean and std of the Chi-squared distribution
        chisq_mean = dof
        chisq_std = np.sqrt(2*dof)
        stat_n = abs(stat-chisq_mean)/chisq_std
        FreemanTukey_Result = FreemanTukeyResult(stat_n, pval)

        return FreemanTukey2Score(FreemanTukey_Result)

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return '%.5f' % self.score.statistic_n
