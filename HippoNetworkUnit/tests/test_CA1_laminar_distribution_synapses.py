import sciunit
import sciunit.scores
import HippoNetworkUnit.capabilities as cap

import quantities
import os

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#==============================================================================


class CA1_laminar_distribution_synapses_Test(sciunit.Test):
    """Tests a synapses distribution of different m-types (AA, BP, BS, CCKBC, Ivy, OLM, PC, PPA, SCA, Tri)
       across the layers of Hippocampus CA1 (SO, SP, SR, SLM)"""
    score_type = sciunit.scores.ZScore
    id = "/tests/12?version=15"

    def __init__(self, observation={}, name="CA1 laminar_distribution_synapses Test"):

        description = ("Tests the synapses distribution of different m-types across the Hippocampus CA1 layers")
        require_capabilities = (cap.Provides_CA1_laminar_distribution_synapses_info,)

        self.units = quantities.dimensionless
        self.figures = []
        observation = self.format_data(observation)
        sciunit.Test.__init__(self, observation, name)
        self.directory_output = './output/'

    #----------------------------------------------------------------------

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

        data_list_0 = list()
        for key0, list0 in data.items():  # key0: list of the m-types neurons (AA, BP, BS, CCKBC, Ivy, OLM, PC, PPA, SCA, Tri)
                                            # list0: list with just one dictionary containing  the m-type cell's
                                            # synapses fraction in each of the Hippocampus CA1 layers (SO, SP, SR, SLM)
                                            # and OUT (for prediction data only)
            data_list_1 = list()
            for dict1 in dict0.values():  # dict1: list of dictionaries {"mean": "X0"} (observation) or
                                            # {"value": "X"} (prediction)

                try:
                    synapses_fraction = float(dict1.values()[0])
                    assert(synapses_fraction <= 1.0)
                    data_list_1.extend([synapses_fraction])
                except:
                    raise sciunit.Error("Values not in appropriate format. Synapses fraction of an m-type cell"
                                        "must be dimensionless and not larger than 1.0")

            data_list_1.extend([0.0]) if "OUT" not in dict0.keys() # observation data
            data_list_1_q = quantities.Quantity(data_list_1, self.units)
            data_list_0.append(data_list_1_q)
 
        data_new_dict = dict.fromkeys(data.keys(), data_list_0)
        return data_new_dict

    # ----------------------------------------------------------------------

    def validate_observation(self, observation):
        print observation.values()

        for val in observation.values():  # lists with synapses fraction per Hippocampus CA1 layers (SO, SP, SR, SLM)
                                            # and OUT (=0.0 by default)
                                            # of each m-type cell (AA, BP, BS, CCKBC, Ivy, OLM, PC, PPA, SCA, Tri)'''
            try:
                # print val, type(val)
                assert type(val) is quantities.Quantity
            except:
                raise sciunit.ObservationError("Observation about synapses fraction in each CA1-layer must be of "
                                               "the form {'mean': XX}")

    #----------------------------------------------------------------------

    def generate_prediction(self, model, verbose=False):
        """Implementation of sciunit.Test.generate_prediction"""

        self.model_name = model.name
        prediction = model.get_CA1_laminar_distribution_synapses_info()
        prediction = self.format_data(prediction)
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation, prediction, verbose=True):
        """Implementation of sciunit.Test.score_prediction"""
        try:
            assert len(observation) == len(prediction)
        except Exception:
            raise sciunit.InvalidScoreError(("Difference in # of m-type cells. Cannot continue test"
                                            "for laminar distribution of synapses across CA1 layers"))

        print "observation = ", observation
        print "prediction = ", prediction


        ZScores_cell = dict()
        for key0 in observation.keys():
            ZScores_layer = list()
            for index in range(len(observation[key0])):
                ZScores_layer[index] = sciunit.scores.ZScore.compute(observation[key0][index], prediction[key0][index])
            ZScores_cell[key] = ZScores_layer[index]

        # self.score = morphounit.scores.CombineZScores.compute(zscores.values())
        self.score = ZScores_cell["PC"][0]

        # create output directory
        path_test_output = self.directory_output + 'CA1_laminar_distribution_synapses /' + self.model_name + '/'
        if not os.path.exists(path_test_output):
           os.makedirs(path_test_output)

        # save figure with Z-score data
        '''
            for key0 in observation.keys():
           score_lf[key0] = float(str(zscores[key0]).split()[2])
        '''
        # layers = range(len(observation))
        width = 0.35
        # plt.bar(layers, score_lf, width, color='blue')
        plt.figlegend(ax_score, ('Z-Score',), 'upper right')
        plt.ylabel("Score value")

        frame_bars = plt.gca()
        frame_bars.axes.get_xaxis().set_visible(False)

        fig_bars = plt.gcf()
        fig_bars.set_size_inches(8, 6)

        filename = \
        path_test_output + 'score_plot' + '.pdf'
        plt.savefig(filename, dpi=600,)
        self.figures.append(filename)

        score = ZScores_cell["PC"][0]
        return score

    #----------------------------------------------------------------------

    def bind_score(self, score, model, observation, prediction):
        score.related_data["figures"] = self.figures
        return score
