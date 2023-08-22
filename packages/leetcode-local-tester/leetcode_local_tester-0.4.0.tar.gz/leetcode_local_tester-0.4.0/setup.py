# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leetcode_local_tester',
 'leetcode_local_tester.creator',
 'leetcode_local_tester.helper',
 'leetcode_local_tester.model',
 'leetcode_local_tester.parsers',
 'leetcode_local_tester.template.python3',
 'leetcode_local_tester.template.utils',
 'leetcode_local_tester.template.utils.python3']

package_data = \
{'': ['*'],
 'leetcode_local_tester': ['template/cpp/*'],
 'leetcode_local_tester.template.utils': ['cpp/*']}

install_requires = \
['alive-progress>=3.1.4,<4.0.0',
 'beautifulsoup4==4.9.1',
 'clang-format>=16.0.6,<17.0.0',
 'click==8.1.4',
 'dacite==1.8.0',
 'html5lib==1.1',
 'requests>=2.31.0,<3.0.0']

entry_points = \
{'console_scripts': ['leetcode-local-tester = leetcode_local_tester.main:cli']}

setup_kwargs = {
    'name': 'leetcode-local-tester',
    'version': '0.4.0',
    'description': '',
    'long_description': '# Leetcode-local-tester\n[![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)](https://github.com/goodstudyqaq/leetcode-local-tester/graphs/commit-activity)\n[![PyPI version](https://img.shields.io/pypi/v/leetcode-local-tester.svg)](https://pypi.python.org/pypi/leetcode-local-tester/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/leetcode-local-tester.svg)](https://pypi.python.org/pypi/leetcode-local-tester/)\n[![Downloads](https://static.pepy.tech/personalized-badge/leetcode-local-tester?period=month&units=international_system&left_color=grey&right_color=orange&left_text=downloads/month)](https://pepy.tech/project/leetcode-local-tester)\n[![Downloads](https://static.pepy.tech/personalized-badge/leetcode-local-tester?period=total&units=international_system&left_color=grey&right_color=orange&left_text=downloads)](https://pepy.tech/project/leetcode-local-tester)\n![GitHub Sponsors](https://img.shields.io/github/sponsors/goodstudyqaq)\n\n\nLeetcode test utils for local environment\n\n# Background\nBecause of Leetcode\'s special design for test cases, if you want to test your code locally, you need to write some boilerplate code to read the test cases from the file and parse them into the format that your code can understand, which is very annoying. Especially in a contest, you may not have enough time to write the boilerplate code. So I wrote this tool to help me generate the boilerplate code automatically. It will improve your efficiency in a contest.\n\nThe design is really like TopCoder\'s test cases, but TopCoder has a very good tool ([TZTester](https://community.topcoder.com/contest/classes/TZTester/TZTester.html)) to generate the boilerplate code for you, which is very convenient.\n\n# Usage\n\n## Install\n```bash\npip install leetcode-local-tester\n```\n\n## Command\n```bash\nleetcode-local-tester work --help\n\nOptions:\n  --kind TEXT          The question kind. Now support: `contest`, `problem`,\n                       `season`, and `contest` includes `weekly` and\n                       `biweekly`. Default is `problem`.\n  --detail TEXT        The detail of the question. If type is `contest` or\n                       `problem`, the detail is the url. Such as\n                       `https://leetcode.com/contest/weekly-contest-326/`,\n                       `https://leetcode.cn/problems/minimum-number-of-\n                       operations-to-reinitialize-a-permutation/`. If type is\n                       `season`, the detail is the season name. Such as\n                       `2020-fall-solo` or `2020-fall-team`.\n  --language TEXT      The language of the code. Now support: `cpp`,\n                       `python3`. Default is `python3`.\n  --location TEXT      The location of the code. Default is `./leetcode/`.\n  --help               Show this message and exit.\n```\n## Before you use\nBecause the utility needs to login to Leetcode to get some information, there are two ways to login. One is to use username and password. You need to set these value to environment variables: `LEETCODE_USERNAME` and `LEETCODE_PASSWORD`. The other is to use cookie. You need to set the cookie to environment variable: `LEETCODE_COOKIE`. You can read the article [How to get the cookie](https://betterprogramming.pub/work-on-leetcode-problems-in-vs-code-5fedf1a06ca1) to get the cookie.\n- Note: If you use `leetcode.com`. You cannot use username and password to login, because `leetcode.com` has recaptcha. So you need to use cookie to login.\n\n\n\n\n## Example\n```bash\nleetcode-local-tester work --kind contest --detail https://leetcode.com/contest/weekly-contest-326/ --language cpp --location ./leetcode/\n```\nAfter running the command, you will get the following files:\n\n\n![dir.jpg](https://s2.loli.net/2023/07/25/APhmjgsIa9G3BSw.jpg)\n\n`weekly-contest-326`: The folder of the contest. It contains all test cases and the code file.\n\n`utils`: The folder of the utils. It contains code that is used to parse the test cases. \n\n**Pay attention: `utils` folder is only generated once. After generated the first time, it will not be updated. So you can add your own code in it.**\n\nYou can write your code in `solution.h`. We take the first question in `weekly-contest-300` as an example.\nThe `solution.h` file is like this:\n\n```cpp\n/*\nCode generated by https://github.com/goodstudyqaq/leetcode-local-tester\n*/\n#if __has_include("../utils/cpp/help.hpp")\n#include "../utils/cpp/help.hpp"\n#elif __has_include("../../utils/cpp/help.hpp")\n#include "../../utils/cpp/help.hpp"\n#else\n#define debug(...) 42\n#endif\n\nclass Solution {\n   public:\n    string decodeMessage(string key, string message) {\n        int res[26];\n        memset(res, -1, sizeof(res));\n        int cnt = 0;\n        for (auto v : key) {\n            int cur = v - \'a\';\n            if (cur >= 0 && cur < 26) {\n                if (res[cur] != -1) continue;\n                res[cur] = cnt++;\n            }\n        }\n        string fin;\n        for (auto v : message) {\n            if (v == \' \')\n                fin += \' \';\n            else {\n                char cur = \'a\' + res[v - \'a\'];\n                fin += cur;\n            }\n        }\n        return fin;\n    }\n};\n```\n\nAfter you finish your own code, you can run `main.cpp` to test your code.\n    \n```bash\ng++ main.cpp -std=c++11 -o main && ./main\n\nCase 1 testing...\n[my_ans]: "this is a secret"\n[result]: "this is a secret"\nCase 1 passed!\nCase 2 testing...\n[my_ans]: "the five boxing wizards jump quickly"\n[result]: "the five boxing wizards jump quickly"\nCase 2 passed!\nThe number of test cases: 2\nThe number of test cases failed: 0\n```\n\nIf you get `Wrong answer`, you can snip the test case and paste it into `data` to debug your code.\n**Pay attention: `data`\'s format is Input + Output.**\n\nIn this example, the test case is:\n\n```text\n"the quick brown fox jumps over the lazy dog"\n"vkbs bs t suepuv"\n```\n\n# TODO\n- [x] Support `python` (completed)\n\n# License\nThis software is licensed under the MIT License. See the LICENSE file in the top distribution directory for the full license text.\n\nMaintaining the project is hard and time-consuming, and I\'ve put much ❤️ and effort into this.\n\nIf you\'ve appreciated my work, you can back me up with a donation! Thank you 😊\n\nIf there is any problem, please create an issue. I will reply to you as soon as possible.\n\n\n[<img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" width="217px" height="51x">](https://www.buymeacoffee.com/goodstudyqaq)\n\n',
    'author': 'shen',
    'author_email': 'goodstudyQAQ@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
