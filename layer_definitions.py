import srim
from srim import Ion, Layer, Target, TRIM
from srim.output import Phonons, Ioniz
from srim.output import Results



p_ten = Layer(
		{
        'C': {
            'stoich': 2.0,
            'E_d': 28.0,
            'lattice': 3.0,
            'surface': 7.47
        },
        'H': {
            'stoich': 8.0,
            'E_d': 28.0,
            'lattice': 3.0,
            'surface': 7.41
        },
        'Ar': {
            'stoich': 90.0,
            'E_d': 5.0,
            'lattice': 1.0,
            'surface': 2.0
        }	        	        
        }, density=gas_density(gas_pressure), width=0.157e9,phase=1)








helium = Layer(
		{
        'C': {
            'stoich': 2.0,
            'E_d': 28.0,
            'lattice': 3.0,
            'surface': 7.47
        },
        'H': {
            'stoich': 8.0,
            'E_d': 28.0,
            'lattice': 3.0,
            'surface': 7.41
        },
        'Ar': {
            'stoich': 90.0,
            'E_d': 5.0,
            'lattice': 1.0,
            'surface': 2.0
        }	        	        
        }, density=gas_density(gas_pressure), width=0.157e9,phase=1)



methane = Layer(
		{
        'C': {
            'stoich': 2.0,
            'E_d': 28.0,
            'lattice': 3.0,
            'surface': 7.47
        },
        'H': {
            'stoich': 8.0,
            'E_d': 28.0,
            'lattice': 3.0,
            'surface': 7.41
        },
        'Ar': {
            'stoich': 90.0,
            'E_d': 5.0,
            'lattice': 1.0,
            'surface': 2.0
        }	        	        
        }, density=gas_density(gas_pressure), width=0.157e9,phase=1)