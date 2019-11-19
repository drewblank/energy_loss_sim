import srim
from srim import Ion, Layer, Target, TRIM
from srim.output import Phonons, Ioniz
from srim.output import Results




def setlayer(layer_label, gas_pressure, length):

	pressure = 133.322*gas_pressure
	R = 8.3144598*10**6
	T = 273

	if (layer_label == 'p_ten'):

		molar_mass = 16.04
		gas_density = molar_mass*pressure/(R*T)
		
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
		        }, density=gas_density, width=length,phase=1)
	
		return p_ten



	if (layer_label == 'helium'):

		molar_mass = 4.002602
		gas_density = molar_mass*pressure/(R*T)


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
	        }, density=gas_density, width=length,phase=1)
		return helium





	if (layer_label == 'methane'):

		molar_mass = 16.04
		gas_density = molar_mass*pressure/(R*T)

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
	        }, density=gas_density, width=length,phase=1)

		return methane

