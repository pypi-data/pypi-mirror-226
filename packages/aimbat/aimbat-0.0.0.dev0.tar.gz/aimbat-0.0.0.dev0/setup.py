# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aimbat', 'aimbat.commands', 'aimbat.lib']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0', 'prettytable>=3.8.0,<4.0.0', 'pysmo>=1.0.0-dev0,<2.0.0']

entry_points = \
{'console_scripts': ['aimbat = aimbat.cli:cli']}

setup_kwargs = {
    'name': 'aimbat',
    'version': '0.0.0.dev0',
    'description': 'AIMBAT: Automated and Interactive Measurement of Body-wave Arrival Times.',
    'long_description': '# AIMBAT\n\n[![Test Status](https://github.com/pysmo/aimbat/actions/workflows/run-tests.yml/badge.svg)](https://github.com/pysmo/pysmo/actions/workflows/run-tests.yml)\n[![Build Status](https://github.com/pysmo/aimbat/actions/workflows/build.yml/badge.svg)](https://github.com/pysmo/pysmo/actions/workflows/build.yml)\n[![Documentation Status](https://readthedocs.org/projects/aimbat/badge/?version=latest)](https://aimbat.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/pysmo/aimbat/branch/master/graph/badge.svg?token=ZsHTBN4rxF)](https://codecov.io/gh/pysmo/aimbat)\n[![PyPI](https://img.shields.io/pypi/v/aimbat)](https://pypi.org/project/aimbat/)\n\nAIMBAT (Automated and Interactive Measurement of Body wave Arrival Times) is an\nopen-source software package for efficiently measuring teleseismic body wave arrival\ntimes for large seismic arrays [[1]](#1). It is based on a widely used method called\nMCCC (Multi-Channel Cross-Correlation) [[2]](#2). The package is automated in the sense\nof initially aligning seismograms for MCCC, which is achieved by an ICCS (Iterative Cross\nCorrelation and Stack) algorithm. Meanwhile, a GUI (graphical user interface) is built to\nperform seismogram quality control interactively. Therefore, user processing time is\nreduced while valuable input from a user\'s expertise is retained. As a byproduct, SAC\n[[3]](#3) plotting and phase picking functionalities are replicated and enhanced.\n\nModules and scripts included in the AIMBAT package were developed using\n[Python](http://www.python.org/) and its open-source modules on the Mac OS X platform\nsince 2009. The original MCCC [[2]](#2) code was transcribed into Python.\nThe GUI of AIMBAT was inspired and initiated at the\n[2009 EarthScope USArray Data Processing and Analysis Short Course](https://www.iris.edu/hq/es_course/content/2009.html).\nAIMBAT runs on Mac OS X, Linux/Unix and Windows thanks to the platform-independent\nfeature of Python.\n\nFor more information visit the\n[project website](http://www.earth.northwestern.edu/~xlou/aimbat.html) or the\n[pysmo repositories](https://github.com/pysmo).\n\n\n## Authors\' Contacts\n\n* [Xiaoting Lou](http://geophysics.earth.northwestern.edu/people/xlou/aimbat.html) Email: xlou at u.northwestern.edu\n\n* [Suzan van der Lee](http://geophysics.earth.northwestern.edu/seismology/suzan/) Email: suzan at northwestern.edu\n\n* [Simon Lloyd](https://www.slloyd.net/) Email: simon at slloyd.net\n\n## Contributors\n\n* Lay Kuan Loh\n\n## References\n\n<a id="1">[1]</a>\nXiaoting Lou, Suzan van der Lee, and Simon Lloyd (2013),\nAIMBAT: A Python/Matplotlib Tool for Measuring Teleseismic Arrival Times.\n*Seismol. Res. Lett.*, 84(1), 85-93, doi:10.1785/0220120033.\n\n<a id="2">[2]</a>\nVanDecar, J. C., and R. S. Crosson (1990),\nDetermination of teleseismic relative phase arrival times using multi-channel\ncross-correlation and\nleast squares.\n*Bulletin of the Seismological Society of America*, 80(1), 150–169.\n\n<a id="3">[3]</a>\nGoldstein, P., D. Dodge, M. Firpo, and L. Minner (2003),\nSAC2000: Signal processing and analysis tools for seismologists and engineers,\n*International Geophysics*, 81, 1613–1614.\n',
    'author': 'Xiaoting Lou',
    'author_email': 'xlou@u.northwestern.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
