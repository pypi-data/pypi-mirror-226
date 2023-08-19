# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_robotframework']

package_data = \
{'': ['*']}

install_requires = \
['deepmerge>=1.1.0,<2.0.0', 'robotframework>=6.1.1,<7.0.0']

entry_points = \
{'pytest11': ['robotframework = pytest_robotframework.pytest_robotframework']}

setup_kwargs = {
    'name': 'pytest-robotframework',
    'version': '1.2.0',
    'description': 'a pytest plugin that can run both python and robotframework tests while generating robot reports for them',
    'long_description': '# pytest-robotframework\n\na pytest plugin that can run both python and robotframework tests while generating robot reports for them\n\n![](https://github.com/DetachHead/pytest-robotframework/assets/57028336/9caabc2e-450e-4db6-bb63-e149a38d49a2)\n\n## install\n\npytest should automatically find and activate the plugin once you install it.\n\n```\npoetry add pytest-robotframework --group=dev\n```\n\n## features\n\n### write robot tests in python\n\n```py\n# you can use both robot and pytest features\nfrom robot.api import logger\nfrom pytest import Cache\n\nfrom pytest_robotframework import keyword\n\n@keyword  # make this function show as a keyword in the robot log\ndef foo():\n    ...\n\n@mark.slow  # gets converted to robot tags\ndef test_foo(cache: Cache):\n    foo()\n```\n\n### run `.robot` tests\n\nto allow for gradual adoption, the plugin also runs regular robot tests as well:\n\n```robot\n*** Settings ***\ntest setup  setup\n\n*** Test Cases ***\nbar\n    [Tags]  asdf  key:value\n    no operation\n\n*** Keywords ***\nsetup\n    log  ran setup\n```\n\nwhich is roughly equivalent to the following python code:\n\n```py\n# conftest.py\nfrom robot.api import logger\nfrom pytest_robotframework import keyword\n\ndef pytest_runtet_setup():\n    foo()\n\n@keyword\ndef foo():\n    logger.info("ran setup")\n```\n\n```py\n# test_foo.py\nfrom pytest import mark\n\n@mark.asdf\n@mark.key("value")\ndef test_bar():\n    ...\n```\n\n### robot command line arguments\n\nspecify robot CLI arguments with the `--robotargs` argument:\n\n```\npytest --robotargs="-d results --listener foo.Foo"\n```\n\nhowever, arguments that have pytest equivalents should not be used. for example, instead of `pytest --robotargs="--include some_tag"` you should use `pytest -m some_tag`.\n\n### setup/teardown and other hooks\n\nto define a function that runs for each test at setup or teardown, create a `conftest.py` with a `pytest_runtest_setup` and/or `pytest_runtest_teardown` function:\n\n```py\n# ./tests/conftest.py\ndef pytest_runtest_setup():\n    log_in()\n```\n\n```py\n# ./tests/test_suite.py\ndef test_something():\n    """i am logged in now"""\n```\n\nthese hooks appear in the log the same way that the a `.robot` file\'s `Setup` and `Teardown` options in `*** Settings ***` would:\n\n![](https://github.com/DetachHead/pytest-robotframework/assets/57028336/d0b6ee6c-adcd-4f84-9880-9e602c2328f9)\n\nfor more information, see [writing hook functions](https://docs.pytest.org/en/7.1.x/how-to/writing_hook_functions.html). pretty much every pytest hook should work with this plugin\nbut i haven\'t tested them all. please raise an issue if you find one that\'s broken.\n\n### tags/markers\n\npytest markers are converted to tags in the robot log:\n\n```py\nfrom pytest import mark\n\n@mark.slow\ndef test_blazingly_fast_sorting_algorithm():\n    [1,2,3].sort()\n```\n\n![](https://github.com/DetachHead/pytest-robotframework/assets/57028336/f25ee4bd-2f10-42b4-bdef-18a22379bd0d)\n\nmarkers like `skip`, `skipif` and `parameterize` also work how you\'d expect:\n\n```py\nfrom pytest import mark\n\n@mark.parametrize("test_input,expected", [(1, 8), (6, 6)])\ndef test_eval(test_input: int, expected: int):\n    assert test_input == expected\n```\n\n![image](https://github.com/DetachHead/pytest-robotframework/assets/57028336/4361295b-5e44-4c9d-b2f3-839e3901b1eb)\n\n### robot suite variables\n\nto set suite-level robot variables, call the `set_variables` function at the top of the test suite:\n\n```py\nfrom robot.libraries.BuiltIn import BuiltIn\nfrom pytest_robotframework import set_variables\n\nset_variables(\n    {\n        "foo": "bar",\n        "baz": ["a", "b"],\n    }\n)\n\ndef test_variables():\n    assert BuiltIn().get_variable_value("$foo") == "bar"\n```\n\n`set_variables` is equivalent to the `*** Variables ***` section in a `.robot` file. all variables are prefixed with `$`. `@` and `&` are not required since `$` variables can store lists and dicts anyway\n',
    'author': 'DetachHead',
    'author_email': 'detachhead@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/detachhead/pytest-robotframework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
