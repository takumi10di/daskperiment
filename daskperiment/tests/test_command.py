import subprocess
import shutil
import sys

import pandas as pd
import pandas.testing as tm

import daskperiment


class TestCommand(object):

    def test_simple_experiment_no_params(self):
        file = 'scripts/simple_experiment.py'

        p = subprocess.Popen([sys.executable, file], stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        assert p.returncode == 1

        # cleanup
        e = daskperiment.Experiment('simple_experiment_pj')
        e._delete_cache()

    def test_simple_experiment(self):
        e = daskperiment.Experiment('simple_experiment_pj')
        assert e._trial_id == 0

        file = 'scripts/simple_experiment.py'

        p = subprocess.Popen([sys.executable, file, 'a=1', 'b=2'],
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        assert p.returncode == 0

        e = daskperiment.Experiment('simple_experiment_pj')
        assert e._trial_id == 1

        hist = e.get_history()
        exp = pd.DataFrame({'a': [1], 'b': [2], 'Result': [4]},
                           index=pd.Index([1], name='Trial ID'))
        tm.assert_frame_equal(exp[['a', 'b', 'Result']], exp)

        p = subprocess.Popen([sys.executable, file, 'a=3', 'b=5'],
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        assert p.returncode == 0

        e = daskperiment.Experiment('simple_experiment_pj')
        hist = e.get_history()
        exp = pd.DataFrame({'a': [1, 3], 'b': [2, 5], 'Result': [4, 9]},
                           index=pd.Index([1, 2], name='Trial ID'))
        tm.assert_frame_equal(hist[['a', 'b', 'Result']], exp)

        # cleanup
        e = daskperiment.Experiment('simple_experiment_pj')
        e._delete_cache()
