# system modules
import warnings

# internal modules
from parmesan.symbols import *

# external modules

__doc__ = """

.. note::

    .. deprecated:: 2.0

        This module is deprecated. Use values from :mod:`parmesan.symbols` instead.

"""

warnings.warn(
    f"""
The parmesan.gas.constants module is deprecated. Use values from :mod:`parmesan.symbols` instead.
""".strip()
)

AVOGADRO_CONSTANT = N_A.quantity
BOLTZMANN_CONSTANT = k_B.quantity
GAS_CONSTANT_UNIVERSAL = R.quantity
MOLAR_MASS_WATER_VAPOUR = M_h2o.quantity
GAS_CONSTANT_WATER_VAPOUR = R_h2o.quantity
MOLAR_MASS_DRY_AIR = M_dry.quantity
GAS_CONSTANT_DRY_AIR = R_dry.quantity
MOLAR_MASS_CO2 = M_co2.quantity
GAS_CONSTANT_CO2 = R_co2.quantity
SPECIFIC_ISOBARIC_HEAT_CAPACITY_DRY_AIR = c_p_dryair.quantity
EARTH_ACCELERATION = earth_acceleration.quantity
VON_KARMAN_CONSTANT = von_karman_constant.value
