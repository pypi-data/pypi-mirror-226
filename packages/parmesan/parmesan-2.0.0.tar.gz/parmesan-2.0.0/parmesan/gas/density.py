# system modules
import logging
import warnings

# internal modules
from parmesan.gas import humidity, laws
from parmesan.gas import temperature as _temperature
from parmesan.errors import ParmesanWarning, ParmesanError
from parmesan.gas import humidity
from parmesan.gas.temperature import (
    virtual_temperature_from_absolute_humidity,
    virtual_temperature_from_mixing_ratio,
)
from parmesan.errors import ParmesanWarning
from parmesan.errors import ParmesanError
from parmesan import units
from parmesan import bounds
from parmesan import utils
from parmesan.utils.function import FunctionCollection
from parmesan.symbols import *

# external modules
import numpy as np
import pint
import sympy

logger = logging.getLogger(__name__)


density = FunctionCollection()
"""
Collection of functions to calculate density
"""


@density.register
@from_sympy(rearrange_from=laws.gas_law_meteorology.equation.subs(R_s, R_dry))
def density_dry_air():
    pass


@density.register
@from_sympy()
def density_humid_air_absolute_humidity():
    r"""
    Calculate the humid-air density :math:`\rho_\mathrm{air}` via the ideal gas
    law, using :any:`virtual_temperature_from_absolute_humidity` to include
    humidity effects in :any:`density_dry_air`.
    """
    return density_dry_air.equation.subs(
        T, _temperature.virtual_temperature_from_absolute_humidity.equation.rhs
    )


@density.register
@from_sympy()
def density_humid_air_from_mixing_ratio():
    r"""
    Calculate the humid-air density :math:`\rho_\mathrm{air}` via the ideal gas
    law, using :any:`virtual_temperature_from_mixing_ratio` to include
    humidity effects in :any:`density_dry_air`.
    """
    return density_dry_air.equation.subs(
        T, _temperature.virtual_temperature_from_mixing_ratio.equation.rhs
    )


__doc__ = rf"""
Equations
+++++++++

{formatted_list_of_equation_functions(locals().copy())}

API Documentation
+++++++++++++++++
"""
