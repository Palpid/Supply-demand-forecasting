import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from preprocess.preparedata import PrepareData
import numpy as np
from utility.runtype import RunType
from utility.datafilepath import g_singletonDataFilePath
from preprocess.splittrainvalidation import HoldoutSplitMethod
import xgboost as xgb
from evaluation.sklearnmape import mean_absolute_percentage_error_xgboost
from evaluation.sklearnmape import mean_absolute_percentage_error
from utility.modelframework import ModelFramework
from utility.xgbbasemodel import XGBoostGridSearch
from evaluation.sklearnmape import mean_absolute_percentage_error_xgboost_cv
from utility.xgbbasemodel import XGBoostBase


class DidiXGBoostModel(XGBoostBase, PrepareData, XGBoostGridSearch):
    def __init__(self):
        PrepareData.__init__(self)
        XGBoostGridSearch.__init__(self)
        XGBoostBase.__init__(self)
        self.do_cross_val = None
        
        return
    def set_xgb_parameters(self):
        early_stopping_rounds = 3
        self.xgb_params = {'max_depth':14, 'eta':0.02, 'silent':1, 'objective':'reg:linear' }
        self.xgb_learning_params = {
                                    'num_boost_round': 100,
                                    'callbacks':[xgb.callback.print_evaluation(show_stdv=True),xgb.callback.early_stop(early_stopping_rounds)],
                                    'feval':mean_absolute_percentage_error_xgboost_cv}
        if self.do_cross_val == False:
            self.xgb_learning_params['feval'] = mean_absolute_percentage_error_xgboost
        return
    def get_paramgrid_1(self):
        """
        This method must be overriden by derived class when its objective is not reg:linear
        """
        param_grid = {'max_depth':[6], 'eta':[0.1],  'min_child_weight':[1],'silent':[1], 
                 'objective':['reg:linear'],'colsample_bytree':[0.8],'subsample':[0.8]}
        return param_grid
     
    def get_paramgrid_2(self, param_grid):
        """
        This method must be overriden by derived class if it intends to fine tune parameters
        """
        self.ramdonized_search_enable = False
        self.randomized_search_n_iter = 3
        self.grid_search_display_result = True
 
#         param_grid['eta'] = [0.01]  #[54]    train-mape:-0.450673+0.00167039    test-mape:-0.45734+0.00530681
#         param_grid['max_depth'] = range(13,25) #[78]    train-mape:-0.406378+0.00244131    test-mape:-0.456578+0.0100904
        param_grid['max_depth'] = [3,4]
        param_grid['eta'] = [0.01,0.1] # 0.459426+0.00518875
#         param_grid['subsample'] = [0.5] #0.458935+0.00522205
#         param_grid['eta'] = [0.005] #0.457677+0.00526401
        return param_grid
     
    def get_learning_params(self):
        """e
        This method must be overriden by derived class if it intends to fine tune parameters
        """
        num_boost_round = 100
        early_stopping_rounds = 3
        

         
        kwargs = {'num_boost_round':num_boost_round, 'feval':mean_absolute_percentage_error_xgboost_cv,
                  'callbacks':[xgb.callback.print_evaluation(show_stdv=True),xgb.callback.early_stop(early_stopping_rounds)]}
        return kwargs

if __name__ == "__main__":   
    obj= DidiXGBoostModel()
    obj.run()