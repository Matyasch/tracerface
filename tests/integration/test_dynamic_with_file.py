from pathlib import Path
import subprocess
import time

from pytest import fixture

from tests.integration.asserts import assert_results
from viewmodel.trace_setup import Setup
from viewmodel.viewmodel import ViewModel


@fixture
def config():
    return '''
{application}:
  - func1:
    - '%s'
    - '%s'
  - func2:
    - '%d'
  - func3
'''


def test_dynamic_model_with_config_file(tmp_path, config):
    test_application_path = Path.cwd().joinpath('tests/integration/resources/test_application')
    test_config_file_content = config.format(application=test_application_path)
    test_config_file = tmp_path.joinpath('test_config_file')
    test_config_file.write_text(test_config_file_content)

    viewmodel = ViewModel(Setup())

    viewmodel.trace_with_config_file(str(test_config_file)) # start monitoring
    time.sleep(5) # BCC trace needs a bit of time to setup
    subprocess.run(str(test_application_path)) # run monitored application
    viewmodel.trace_btn_turned_off() # stop monitoring

    assert_results(viewmodel.get_nodes(), viewmodel.get_edges())
