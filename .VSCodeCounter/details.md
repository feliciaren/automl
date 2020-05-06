# Details

Date : 2020-05-06 00:23:37

Directory d:\school\automl\automl\server

Total : 45 files,  2944 codes, 1218 comments, 743 blanks, all 4905 lines

[summary](results.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [server/__init__.py](/server/__init__.py) | Python | 10 | 3 | 1 | 14 |
| [server/cmd.py](/server/cmd.py) | Python | 43 | 1 | 17 | 61 |
| [server/early_stop/basic_early_stop.py](/server/early_stop/basic_early_stop.py) | Python | 14 | 8 | 4 | 26 |
| [server/early_stop/curve_functions.py](/server/early_stop/curve_functions.py) | Python | 75 | 176 | 30 | 281 |
| [server/early_stop/curve_model.py](/server/early_stop/curve_model.py) | Python | 153 | 168 | 16 | 337 |
| [server/early_stop/curve_stop.py](/server/early_stop/curve_stop.py) | Python | 26 | 0 | 13 | 39 |
| [server/early_stop/median_stop.py](/server/early_stop/median_stop.py) | Python | 20 | 0 | 10 | 30 |
| [server/feature_select/__init__.py](/server/feature_select/__init__.py) | Python | 1 | 0 | 0 | 1 |
| [server/feature_select/basic_select.py](/server/feature_select/basic_select.py) | Python | 19 | 16 | 4 | 39 |
| [server/feature_select/constants.py](/server/feature_select/constants.py) | Python | 53 | 27 | 21 | 101 |
| [server/feature_select/fginitialize.py](/server/feature_select/fginitialize.py) | Python | 381 | 131 | 112 | 624 |
| [server/feature_select/fgtrain.py](/server/feature_select/fgtrain.py) | Python | 154 | 32 | 43 | 229 |
| [server/feature_select/gbdtselector.py](/server/feature_select/gbdtselector.py) | Python | 53 | 53 | 17 | 123 |
| [server/feature_select/gradient_selector.py](/server/feature_select/gradient_selector.py) | Python | 346 | 238 | 48 | 632 |
| [server/feature_select/learnability.py](/server/feature_select/learnability.py) | Python | 304 | 152 | 74 | 530 |
| [server/feature_select/requirements.txt](/server/feature_select/requirements.txt) | pip requirements | 4 | 0 | 1 | 5 |
| [server/feature_select/syssettings.py](/server/feature_select/syssettings.py) | Python | 4 | 21 | 5 | 30 |
| [server/feature_select/utils.py](/server/feature_select/utils.py) | Python | 41 | 22 | 16 | 79 |
| [server/http_handler.py](/server/http_handler.py) | Python | 38 | 1 | 6 | 45 |
| [server/model/globals.py](/server/model/globals.py) | Python | 13 | 0 | 4 | 17 |
| [server/model/study.py](/server/model/study.py) | Python | 90 | 2 | 18 | 110 |
| [server/model/trials.py](/server/model/trials.py) | Python | 50 | 1 | 8 | 59 |
| [server/model/worker.py](/server/model/worker.py) | Python | 86 | 0 | 27 | 113 |
| [server/search/__init__.py](/server/search/__init__.py) | Python | 9 | 0 | 0 | 9 |
| [server/search/base_chocolate_algorithm.py](/server/search/base_chocolate_algorithm.py) | Python | 71 | 15 | 28 | 114 |
| [server/search/base_hyperopt_algorithm.py](/server/search/base_hyperopt_algorithm.py) | Python | 137 | 27 | 52 | 216 |
| [server/search/basic_search.py](/server/search/basic_search.py) | Python | 42 | 0 | 7 | 49 |
| [server/search/bayesian_optimization.py](/server/search/bayesian_optimization.py) | Python | 123 | 25 | 45 | 193 |
| [server/search/cmaes.py](/server/search/cmaes.py) | Python | 12 | 3 | 3 | 18 |
| [server/search/grid_search.py](/server/search/grid_search.py) | Python | 42 | 5 | 25 | 72 |
| [server/search/mocmaes.py](/server/search/mocmaes.py) | Python | 12 | 3 | 4 | 19 |
| [server/search/random_fuction.py](/server/search/random_fuction.py) | Python | 29 | 39 | 8 | 76 |
| [server/search/random_search.py](/server/search/random_search.py) | Python | 42 | 4 | 14 | 60 |
| [server/search/simulate_anneal.py](/server/search/simulate_anneal.py) | Python | 12 | 3 | 4 | 19 |
| [server/search/static.py](/server/search/static.py) | Python | 29 | 39 | 8 | 76 |
| [server/search/tpe.py](/server/search/tpe.py) | Python | 12 | 3 | 4 | 19 |
| [server/setup.py](/server/setup.py) | Python | 30 | 0 | 3 | 33 |
| [server/testtools/test_search/test_basic_search.py](/server/testtools/test_search/test_basic_search.py) | Python | 14 | 0 | 4 | 18 |
| [server/testtools/test_search/test_bayes_optimization.py](/server/testtools/test_search/test_bayes_optimization.py) | Python | 58 | 0 | 7 | 65 |
| [server/testtools/test_search/test_grid_search.py](/server/testtools/test_search/test_grid_search.py) | Python | 51 | 0 | 6 | 57 |
| [server/testtools/test_search/test_mocmaes.py](/server/testtools/test_search/test_mocmaes.py) | Python | 58 | 0 | 6 | 64 |
| [server/testtools/test_search/test_random_search.py](/server/testtools/test_search/test_random_search.py) | Python | 58 | 0 | 7 | 65 |
| [server/testtools/test_search/test_simulate_anneal.py](/server/testtools/test_search/test_simulate_anneal.py) | Python | 58 | 0 | 6 | 64 |
| [server/testtools/test_search/test_tpe.py](/server/testtools/test_search/test_tpe.py) | Python | 58 | 0 | 6 | 64 |
| [server/version.py](/server/version.py) | Python | 9 | 0 | 1 | 10 |

[summary](results.md)