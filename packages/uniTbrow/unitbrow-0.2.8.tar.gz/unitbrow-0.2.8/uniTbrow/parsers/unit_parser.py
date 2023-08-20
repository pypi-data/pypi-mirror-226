from sympy import parse_expr as p
from sympy.parsing.sympy_parser import T
from uniTbrow.units.units import library


def parse_units(unit_string, transformations=T[:], unit_library=library):
    return p(unit_string, transformations=transformations, local_dict=unit_library.unit_dictionary)
