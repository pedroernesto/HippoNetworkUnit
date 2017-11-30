import sciunit
import sciunit.utils as utils

import numpy as np

class FreemanTukey(sciunit.Score):
    """
    A Freeman-Tukey score. A float giving the Freeman-Tukey statistic for
    a goodness-of-fit test in the case of small counts (frequencies)
    """
    
    _allowed_types = (float,)

    _description = ('A Freeman-Tukey score. A float giving the Freeman-Tukey statistic'
                    'for a goodness-of-fit test in the case of small counts (frequencies)')

    @classmethod
    def compute(cls, observation, prediction):
        """
        Computes a Freeman-Tukey score from an observation and a prediction.
        """

        obs_values = observation[~np.isnan(observation)]
        pred_values = prediction[~np.isnan(prediction)]

	    value = 4*sum( ( numpy.sqrt(obs_values) - numpy.sqrt(pred_values) )**2 )
        value = utils.assert_dimensionless(value)
        return FreemanTukey(value)

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return 'FreemanTukey-statistic = %.5f' % self.score
