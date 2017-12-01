import sciunit
import sciunit.utils as utils

import numpy as np
import scipy
from collections import namedtuple

FreemanTukeyResult = namedtuple('FreemanTukeyResult', ('statistic', 'pvalue'))
class FreemanTukey(sciunit.Score):
    """
    A Freeman-Tukey score.A float giving the result of a Freeman-Tukey goodness-of-fit test..
    It is useful in the case of small counts (frequencies)
    """
    
    _allowed_types = (float,)

    _description = ('A Freeman-Tukey score. A float giving the result of a Freeman-Tukey goodness-of-fit test.'
                    'It is useful in the case of small counts (frequencies)')

    @classmethod
    def compute(cls, observation, prediction):
        """
        Computes a Freeman-Tukey score from an observation and a prediction.
        """

        obs_values = observation[~np.isnan(observation)]
        pred_values = prediction[~np.isnan(prediction)]

        num_obs = len(obs_values)
        stat = 4*sum((np.sqrt(obs_values) - np.sqrt(pred_values))**2)
        pval = scipy.stats.distributions.chi2.sf(stat, num_obs - 1)

        stat = utils.assert_dimensionless(stat)
        pval = utils.assert_dimensionless(pval)
        FreemanTukey_Result = FreemanTukeyResult(stat, pval)

        return FreemanTukey(FreemanTukey_Result.statistic)

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return 'FreemanTukey-score = %.5f' % self.score
