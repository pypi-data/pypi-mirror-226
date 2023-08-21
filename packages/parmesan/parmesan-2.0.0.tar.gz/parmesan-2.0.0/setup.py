# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parmesan',
 'parmesan.gas',
 'parmesan.processing',
 'parmesan.radiation',
 'parmesan.utils',
 'tests']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.2,<4.0.0',
 'numpy>=1.13.3,<2.0.0',
 'pandas>=1,<2',
 'pint-pandas>=0.4',
 'pint>=0.22',
 'rich>=13.0',
 'scipy>=1.1,<2.0',
 'sympy>=1.12,<2.0']

setup_kwargs = {
    'name': 'parmesan',
    'version': '2.0.0',
    'description': 'Python Atmospheric Research Package for Meteorological Timeseries Analysis',
    'long_description': "# 🧀 PARMESAN\n\n**P**ython **A**tmospheric **R**esearch program for **ME**teorological **S**cientific **AN**alysis\n\n[![pipeline status](https://gitlab.com/tue-umphy/software/parmesan/badges/master/pipeline.svg)](https://gitlab.com/tue-umphy/software/parmesan/-/pipelines)\n[![coverage report](https://gitlab.com/tue-umphy/software/parmesan/badges/master/coverage.svg)](https://tue-umphy.gitlab.io/software/parmesan/coverage-report/)\n[![documentation](https://img.shields.io/badge/documentation-here%20on%20GitLab-brightgreen.svg)](https://tue-umphy.gitlab.io/software/parmesan)\n[![Downloads](https://static.pepy.tech/badge/parmesan)](https://pepy.tech/project/parmesan)\n\n## What can `PARMESAN` do?\n\nPARMESAN is targeted at meteorologists/scientists doing atmospheric measurements who want to analyse their obtained time series, calculate typical temperature, wind, humidity, atmospheric stability and turbulence parameters.\nPARMESAN provides basic building blocks for typical meteorological calculations and can be easily expanded as equations are based on symbolic mathematics that can be recombined and repurposed.\n\n#### 🔢 Physical Calculations\n\n- 📉 calculating [**power spectra** of timeseries](https://tue-umphy.gitlab.io/software/parmesan/notebooks/spectrum.html)\n- 📉 calculating [**structure functions** of timeseries](https://tue-umphy.gitlab.io/software/parmesan/notebooks/structure.html)\n- ⏱ calculating [**temporal cycles**](https://tue-umphy.gitlab.io/software/parmesan/api/parmesan.aggregate.html#parmesan.aggregate.temporal_cycle) (e.g. diurnal/daily cycles)\n- 🌫 calculating several [**humidity** measures](https://tue-umphy.gitlab.io/software/parmesan/api/parmesan.gas.humidity.html)\n- 🌡 calculating several [**temperature** measures](https://tue-umphy.gitlab.io/software/parmesan/api/parmesan.gas.temperature.html)\n- 📜 handling [**physical units** and checking **bounds**](https://tue-umphy.gitlab.io/software/parmesan/settings.html)\n- 🍃 [**wind** calculations](https://tue-umphy.gitlab.io/software/parmesan/api/parmesan.wind.html) calculations\n- 💨 [**turbulence parameters**](https://tue-umphy.gitlab.io/software/parmesan/api/parmesan.turbulence.html)\n- 🔢 based on reusable [SymPy](https://sympy.org) symbolic mathematics\n\n#### ❓ Why not `metpy`?\n\nWhile [`metpy`](https://unidata.github.io/MetPy) provides much functionality to handle spatial weather data, it is less focused on timeseries/turbulence analysis such as spectral analysis. See [here](https://tue-umphy.gitlab.io/software/parmesan#why-not-metpy) for a more detailed comparison.\n\n\n#### 🛠️ Inner Workings\n\nPARMESAN uses...\n\n- [SymPy](https://sympy.org) to do the math. PARMESAN derives meteorlogical equations with it and auto-generates Python functions and documentation based SymPy expressions.\n- [pint](pint.readthedocs.io/) to handle physical units.\n- [pint-pandas](https://github.com/hgrecco/pint-pandas) to enable handle units in [pandas](https://pandas.pydata.org/)-DataFrames.\n- [numpy](https://numpy.org) and [scipy](https://scipy.org/) for the numerics\n- [rich](https://rich.readthedocs.io/) for pretty terminal output like progress bars\n- [matplotlib](https://matplotlib.org/) for plotting\n\n## 📦 Installation\n\nTagged versions of `PARMESAN` are available [on PyPi](https://pypi.org/project/parmesan/).\nYou can install the latest tagged version of `PARMESAN` via\n\n```bash\n# make sure you have pip installed\n# Debian/Ubuntu:  sudo apt update && sudo apt install python3-pip\n# Manjaro/Arch:  sudo pacman -Syu python-pip\n\n# (optional) Then it's good practice to generate a virtual environment:\npython3 -m venv parmesan-venv\nsource parmesan-venv/bin/activate\n\n# Then install PARMESAN\npython3 -m pip install -U parmesan\n```\n\nTo install the latest development version of `PARMESAN` directly from GitLab, run\n\n```bash\n# make sure to have pip installed, see above\npython3 -m pip install -U git+https://gitlab.com/tue-umphy/software/parmesan\n```\n\nYou may also use [our workgroup Arch/Manjaro repository](https://gitlab.com/tue-umphy/workgroup-software/repository) and install the `python-parmesan` package with your favourite software installer, for example with `pacman`:\n\n```bash\nsudo pacman -Syu python-parmesan\n```\n\n## 📖 Documentation\n\nDocumentation can be found [here on GitLab](https://tue-umphy.gitlab.io/software/parmesan).\n\nIf you have a question or a problem with PARMESAN, you may [open an issue on GitLab](https://gitlab.com/tue-umphy/software/parmesan/-/issues/new).\n\n## ➕ Contributing to PARMESAN\n\nIf you'd like to contribute to PARMESAN, e.g. by adding new features or fixing bugs or just to run the test suite or generate the documentation locally, read the [`CONTRIBUTING.md`-file](https://gitlab.com/tue-umphy/software/parmesan/-/blob/master/CONTRIBUTING.md).\n",
    'author': 'Yann Büchau',
    'author_email': 'yann-georb.buechau@uni-tuebingen.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/tue-umphy/software/parmesan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
