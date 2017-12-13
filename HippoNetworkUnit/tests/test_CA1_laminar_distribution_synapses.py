import sciunit

import sciunit.scores
import HippoNetworkUnit.scores as hpn_scores
import HippoNetworkUnit.capabilities as hpn_cap

import quantities
import os

# For data manipulation
import pandas as pd

# For plotting
# Force matplotlib to not use any Xwindows backend.
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns

# score_str = 'KLdivScore'
score_str = 'FreemanTukeyScore'

# ==============================================================================

class CA1_laminar_distribution_synapses_Test(sciunit.Test):
    """Tests a synapses distribution of different m-types (AA, BP, BS, CCKBC, Ivy, OLM, PC, PPA, SCA, Tri)
       across the layers of Hippocampus CA1 (SO, SP, SR, SLM)"""

    score_type = eval('hpn_scores.' + score_str)
    id = "/tests/12?version=15"

    def __init__(self, observation={}, name="CA1 laminar_distribution_synapses Test"):

        description = ("Tests the synapses distribution of different m-types across the Hippocampus CA1 layers")
        require_capabilities = (hpn_cap.Provides_CA1_laminar_distribution_synapses_info,)

        self.units = quantities.dimensionless
        self.figures = []
        observation = self.format_data(observation)
        sciunit.Test.__init__(self, observation, name)
        self.directory_output = './output/'

    # ----------------------------------------------------------------------

    def format_data(self, data):
        """
        This accepts data input in the form:
        ***** (observation) *****
        {   "AA":{
                "SO": {"mean": "X0"},
                "SP": {"mean": "X1"},
                "SR": {"mean": "X2"},
                "SLM":{"mean": "X3"}
            },
            "BP": {...},
            "BS": {...},
            "CCKBC":{...},
            "Ivy":{...},
            "OLM":{...},
            "PC":{...},
            "PPA":{...},
            "SCA":{...},
            "Tri":{...}
        }

        ***** (prediction) *****
        {   "AA":{
                "SO": {"value": "X0"},
                "SP": {"value": "X1"},
                "SR": {"value": "X2"},
                "SLM":{"value": "X3"},
                "OUT":{"value": "X4"}
            },
            "BP": {...},
            "BS": {...},
            "CCKBC":{...},
            "Ivy":{...},
            "OLM":{...},
            "PC":{...},
            "PPA":{...},
            "SCA":{...},
            "Tri":{...}
        }

        Returns a new dictionary of the form 
        { "AA":[X0, X1, X2, X3, X4], "BP":[...] , "BS":[...], "CCKBC":[...], "Ivy":[...], "OLM":[...],
        "PC":[...], "PPA":[...], "SCA":[...], "Tri":[...] }
        """

        data_new_dict = dict()
        for key0, dict0 in data.items():  # dict0: a dictionary containing the synapses fraction in each of the
                                    # Hippocampus CA1 layers (SO, SP, SR, SLM) and OUT (for prediction data only)
                                    # for each m-type cell (AA, BP, BS, CCKBC, Ivy, OLM, PC, PPA, SCA, Tri)
            data_list_1 = list()
            for dict1 in dict0.values():  # dict1: a dictionary of the form
                                        # {"mean": "X0"} (observation) or {"value": "X"} (prediction)
                try:
                    synapses_fraction = float(dict1.values()[0])
                    assert(synapses_fraction <= 1.0)
                    data_list_1.extend([synapses_fraction])
                except:
                    raise sciunit.Error("Values not in appropriate format. Synapses fraction of an m-type cell"
                                        "must be dimensionless and not larger than 1.0")

            if "OUT" not in dict0.keys(): data_list_1.extend([0.0])  # observation data
            data_list_1_q = quantities.Quantity(data_list_1, self.units)
            data_new_dict[key0] = data_list_1_q

        return data_new_dict

    # ----------------------------------------------------------------------

    def validate_observation(self, observation):

        for val in observation.values():  # val0: a list with synapses fraction in each of the
                                            # Hippocampus CA1 layers (SO, SP, SR, SLM) and OUT (=0.0 by default)
                                            # for each m-type cell (AA, BP, BS, CCKBC, Ivy, OLM, PC, PPA, SCA, Tri)
            try:
                assert type(val) is quantities.Quantity
            except:
                raise sciunit.ObservationError("Observation about synapses fraction in each CA1-layer"
                                               "must be of the form {'mean': XX}")

    # ----------------------------------------------------------------------

    def generate_prediction(self, model, verbose=False):
        """Implementation of sciunit.Test.generate_prediction"""

        self.model_name = model.name
        prediction = model.get_CA1_laminar_distribution_synapses_info()
        prediction = self.format_data(prediction)

        return prediction

    # ----------------------------------------------------------------------

    def compute_score(self, observation, prediction, verbose=True):
        """Implementation of sciunit.Test.score_prediction"""
        try:
            assert len(observation) == len(prediction)
        except Exception:
            raise sciunit.InvalidScoreError(("Difference in # of m-type cells. Cannot continue test"
                                            "for laminar distribution of synapses across CA1 layers"))

        # print "observation = ", observation, "\n"
        # print "prediction = ", prediction, "\n"

        # Computing the score
        zscores_cell = dict()
        for key0 in observation.keys():  # m-type cell (AA, BP, BS, CCKBC, Ivy, OLM, PC, PPA, SCA, Tri)
            zscores_cell[key0] = eval('hpn_scores.' + score_str + '.compute(observation[key0], prediction[key0])')

        # create output directory
        path_test_output = self.directory_output + 'CA1_laminar_distribution_synapses /' + self.model_name + '/'
        if not os.path.exists(path_test_output):
            os.makedirs(path_test_output)

        # save figure with score data
        zscores_cell_float = dict.fromkeys(zscores_cell.keys(), [])
        for key0 in zscores_cell.keys():
            zscores_cell_float[key0] = zscores_cell[key0].score

        zscores_cell_DF = pd.DataFrame(zscores_cell_float, index=[score_str[:-5] + '-score'])
        print zscores_cell_DF

        axis_obj = sns.barplot(data=zscores_cell_DF)
        axis_obj.set(xlabel="Cell",ylabel=score_str[:-5] + "-score value")
        filename = path_test_output + score_str + '_plot' + '.pdf'
        plt.savefig(filename, dpi=600,)
        self.figures.append(filename)

        # self.score = morphounit.scores.CombineZScores.compute(zscores.values())
        self.score = zscores_cell["PC"]
        return self.score

    # ----------------------------------------------------------------------

    def bind_score(self, score, model, observation, prediction):
        score.related_data["figures"] = self.figures
        return score
