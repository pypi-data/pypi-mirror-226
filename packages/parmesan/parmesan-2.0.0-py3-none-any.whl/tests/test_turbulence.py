# system modules
import unittest
from math import factorial as fac
import itertools

# internal modules
import parmesan
from parmesan.units import units
from parmesan import turbulence

# external modules
import pandas as pd
import numpy as np


class TKETest(unittest.TestCase):
    def test_tke_per_mass_no_variance(self):
        self.assertEqual(
            turbulence.turbulence_kinetic_energy_per_unit_mass(
                u=[0, 0, 0], v=[1, 1, 1], w=[2, 2, 2]
            ),
            0 * units("m² / s²"),
        )

    def test_tke_per_volume_no_variance(self):
        self.assertEqual(
            turbulence.turbulence_kinetic_energy_per_unit_volume(
                u=[0, 0, 0],
                v=[0, 0, 0],
                w=[0, 0, 0],
                density=units("1.2 kg / m³"),
            ),
            0 * units("J / m³"),
        )

    def test_turbulence_intensity(self):
        self.assertAlmostEqual(
            turbulence.turbulence_intensity(u=[1, 1, 1], v=[1, 1, 1]),
            0 * units("dimensionless"),
        )


class CovariancesTest(unittest.TestCase):
    def test_covariances_accessor(self):
        cols = "abcd"
        df = pd.DataFrame(
            {
                c: np.cumsum(np.random.uniform(-1, 1, (n := 1000)))
                for c in cols
            },
            index=pd.date_range(
                start="2023-01-01", freq=(samprate := "100ms"), periods=n
            ),
        )
        covariances = df.parmesan.covariances(covint := "1s")
        # TODO: for now, only the amount of columns is asserted.
        self.assertEqual(
            len(covariances.columns),
            fac(len(cols)) / (fac(2) * fac(len(cols) - 2)),
        )
