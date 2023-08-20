import uniTbrow.units as u
import uniTbrow.dimensions as d


def get_dimensions(expr):
    for symbol in expr.free_symbols:
        try:
            unit = u.library.lookup(symbol)
            expr = expr.subs(symbol, unit.dimension.dimension)
        except KeyError:
            continue
    return expr


class BaseUnitSystem:
    def __init__(self, dimension_unit_map):
        self.dimension_unit_map = dimension_unit_map

    def convert(self, expr):
        expr = u.to_base_units(expr)
        for symbol in expr.free_symbols:
            try:
                unit = u.library.lookup(symbol)
                to_unit = self.dimension_unit_map[unit.dimension]
                expr = expr.subs(symbol, unit.conversions[to_unit])
            except KeyError:
                continue
        return expr


si = BaseUnitSystem({
    d.mass: u.lookup("kg"),
})

cgs = BaseUnitSystem({
    d.length: u.lookup("cm"),
})
