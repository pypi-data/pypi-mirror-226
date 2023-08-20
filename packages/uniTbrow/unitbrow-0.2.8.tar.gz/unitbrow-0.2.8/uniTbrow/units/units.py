from sympy import symbols as _symbols, pi as _pi
from uniTbrow import dimensions

_metric_prefixes = [
    ("Q", ["quetta"], 10**30),
    ("R", ["ronna"], 10**27),
    ("Y", ["yotta"], 10**24),
    ("Z", ["zetta"], 10**21),
    ("E", ["exa"], 10**18),
    ("P", ["peta"], 10**15),
    ("T", ["tera"], 10**12),
    ("G", ["giga"], 10**9),
    ("M", ["mega"], 10**6),
    ("k", ["kilo"], 10**3),
    ("h", ["hecto"], 10**2),
    ("da", ["deka"], 10**1),
    ("d", ["deci"], 10**-1),
    ("c", ["centi"], 10**-2),
    ("m", ["milli"], 10**-3),
    ("μ", ["micro", "u"], 10**-6),
    ("n", ["nano"], 10**-9),
    ("p", ["pico"], 10**-12),
    ("f", ["femto"], 10**-15),
    ("a", ["atto"], 10**-18),
    ("z", ["zepto"], 10**-21),
    ("y", ["yocto"], 10**-24),
    ("r", ["ronto"], 10**-27),
    ("q", ["quecto"], 10**-30)
]


class Unit:
    def __init__(self, dimension: dimensions.Dimension, abbr_symbol: str, alternates=None, base=None, metric=True):
        if alternates is None:
            alternates = []
        assert base is True or (base is not None), "Need to provide a conversion to a base unit"
        self.dimension: dimensions.Dimension = dimension
        self.symbol = _symbols(abbr_symbol, positive=True, real=True)
        self.alternates: list = alternates
        self.conversions: dict = dict()
        self.metric: bool = metric
        self.base = base

    # add_conversion defines the factor used to convert from other_unit to this unit
    def add_conversion(self, other_unit, expr):
        assert other_unit.dimension == self.dimension, "Dimension mismatch between " +\
                                                       self.dimension.dimension +\
                                                       " and " + other_unit.dimension.dimension
        self.conversions[other_unit] = expr

    def generate_metric_prefixes(self):
        if not self.metric:
            return []
        metric_units = []
        for abbr, alts, factor in _metric_prefixes:
            alternates = []
            for alt_prefix in alts:
                for suffix in self.alternates:
                    alternates.append(str(alt_prefix+suffix))

            new_unit = Unit(self.dimension, abbr+str(self.symbol), alternates=[], metric=False, base=factor*self.symbol)
            new_unit.add_conversion(self, factor*self.symbol)
            self.add_conversion(new_unit, (1/factor)*new_unit.symbol)
            metric_units.append(new_unit)

        return metric_units

    def __repr__(self):
        return str(self.symbol)+"["+str(self.dimension.dimension)+"]"

    def __str__(self):
        string_to_return = str(self.symbol)
        string_to_return += "[" + str(self.dimension.dimension) + "]"
        if len(self.alternates) >= 1:
            string_to_return += "\t" + str(len(self.alternates)) + " alternate spellings"
            string_to_return += " (e.g. " + str(self.alternates[0]) + ")"
        return string_to_return

    def __pow__(self, power, modulo=None):
        return pow(self.symbol, power, modulo)

    def __mul__(self, other):
        return self.symbol * other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.symbol / other

    def __rtruediv__(self, other):
        return other / self.symbol


class UnitLibrary:
    def __init__(self):
        self.unit_dictionary = dict()
        self.reverse_unit_dictionary = dict()

    def lookup(self, unit_to_lookup):
        """
        lookup searches for a unit either by symbol or string representation. String representation can
        handle variants of a unit (e.g. μm, um, micrometer, micrometre would all return the correct micrometer Unit)

        Throws a KeyError if the unit being searched for does not exist

        :param unit_to_lookup: Either a `str` or `Symbol` to lookup.
        :return: The `Unit` representation of the unit to lookup
        """
        if isinstance(unit_to_lookup, str):
            return self.reverse_unit_dictionary[self.unit_dictionary[unit_to_lookup]]
        return self.reverse_unit_dictionary[unit_to_lookup]

    def add(self, unit_to_add: Unit):
        self.unit_dictionary[str(unit_to_add.symbol)] = unit_to_add.symbol
        self.reverse_unit_dictionary[unit_to_add.symbol] = unit_to_add
        for alternate in unit_to_add.alternates:
            self.unit_dictionary[alternate] = unit_to_add.symbol

    def add_all(self, unit_list: list[Unit]):
        for u in unit_list:
            self.add(u)


# Base Units
metre = meter = Unit(dimensions.length, "m", ["meter", "metre", "meters", "metres"], base=True)
second = Unit(dimensions.time, "s", ["second", "seconds", "sec", "secs"], base=True)
mole = Unit(dimensions.amount, "mole", ["mol", "moles"], base=True)
ampere = Unit(dimensions.current, "A", ["ampere", "amps", "amperes", "amp"], base=True)
kelvin = Unit(dimensions.temperature, "K", ["kelvin"], base=True)
candela = Unit(dimensions.luminous_intensity, "cd", ["candela"], base=True)
gram = Unit(dimensions.mass, "g", ["gram", "grams"], base=True)

# Derived Units

hertz = Unit(dimensions.frequency, "Hz", ["hertz"], base=(1 / second.symbol))

radian = Unit(dimensions.angle, "rad", ["radians", "radian"], base=1)

steradian = Unit(dimensions.solid_angle, "sr", ["steradians", "steradian"], base=1)

newton = Unit(dimensions.force, "N", ["newtons", "newton"], base=(1000 * gram.symbol * metre.symbol / (second.symbol ** 2)))

pascal = Unit(dimensions.pressure, "Pa", ["pascals", "pascal"], base=(1000 * gram.symbol * metre.symbol ** -1 * second.symbol ** -2))

joule = Unit(dimensions.energy, "J", ["joule", "joules"], base=(1000 * gram.symbol * metre.symbol ** 2 * second.symbol ** -2))

watt = Unit(dimensions.power, "W", ["watt", "watts"], base=(1000 * gram.symbol * metre.symbol ** 2 * second.symbol ** -3))

coulomb = Unit(dimensions.charge, "C", ["coulombs", "coulomb"], base=(second.symbol * ampere.symbol))

volt = Unit(dimensions.electric_potential, "V", ["volts", "volt"], base=(1000 * gram.symbol * metre.symbol ** 2 * second.symbol ** -3 * ampere.symbol ** -1))

farad = Unit(dimensions.capacitance, "F", ["farads", "farad"], base=((1000 * gram.symbol) ** -1 * metre.symbol ** -2 * second.symbol ** 4 * ampere.symbol ** 2))

ohm = Unit(dimensions.resistance, "Ω", ["ohms", "ohm"], base=(1000 * gram.symbol * metre.symbol ** 2 * second.symbol ** -3 * ampere.symbol ** -2))

siemens = Unit(dimensions.conductance, "S", ["siemens", "siemen", "mho", "mhos"], base=((1000 * gram.symbol) ** -1 * metre.symbol ** -2 * second.symbol ** 3 * ampere.symbol ** 2))

weber = Unit(dimensions.magnetic_flux, "Wb", ["weber", "webers"], base=(1000 * gram.symbol * metre.symbol ** 2 * second.symbol ** -2 * ampere.symbol ** -1))

tesla = Unit(dimensions.magnetic_induction, "T", ["tesla", "teslas"], base=(1000 * gram.symbol * second.symbol ** -2 * ampere.symbol ** -1))

henry = Unit(dimensions.electric_inductance, "H", ["henry", "henrys"], base=(1000 * gram.symbol * metre.symbol ** 2 * second.symbol ** -2 * ampere.symbol ** -2))

# Astronomical Units
mass_sun = Unit(dimensions.mass, "M_⊙", ["solar_mass", "solar_masses", "M_sun"], metric=False, base=(1.98847 * 10 ** 33 * gram.symbol))
parsec = Unit(dimensions.length, "pc", ["parsec", "parsecs"], base=(3.0856775814913 * 10 ** 16 * metre.symbol))
astronomical_unit = Unit(dimensions.length, "AU", ["au", "astronomical_units", "astronomical_unit"], metric=False, base=(1.495978707 * 10 ** 11 * metre.symbol))
lightyear = Unit(dimensions.length, "ly", ["lightyear", "lyr", "lyrs", "lightyears", "light_year", "light_years"], base=(9460730472580800 * metre.symbol))
solar_luminosity = Unit(dimensions.power, "L_⊙", ["L_sun", "solar_luminosity", "solar_luminosities"], metric=False, base=(3.828 * 10 ** 26 * watt.base))

# Additional length units
fermi = Unit(dimensions.length, "fermi", ["fermis"], base=(10 ** -15 * metre.symbol))
angstrom = Unit(dimensions.length, "Å", ["angstrom", "angstroms"], metric=False, base=(100 * 10 ** -12 * metre.symbol))
micron = Unit(dimensions.length, "micron", ["microns"], metric=False, base=(10 ** -6 * metre.symbol))
yard = Unit(dimensions.length, "yd", ["yards", "yds", "yard"], metric=False, base=(0.9144 * metre.symbol))
foot = Unit(dimensions.length, "ft", ["feet", "foot"], metric=False, base=(yard.base / 3))
inch = Unit(dimensions.length, "in", ["inch", "inches"], metric=False, base=(foot.base / 12))
mile = Unit(dimensions.length, "mile", ["miles"], metric=False, base=(foot.base * 5280))
fathom = Unit(dimensions.length, "fathom", ["fathoms"], metric=False, base=(6 * foot.base))
nautical_mile = Unit(dimensions.length, "nmi", ["NM", "M", "nautical_mile", "nautical_miles"], metric=False, base=(1852 * metre.symbol))
furlong = Unit(dimensions.length, "furlong", ["furlongs"], metric=False, base=(220 * yard.base))

# Additional time units
minute = Unit(dimensions.time, "min", ["mins", "minutes", "minute"], metric=False, base=(60 * second.symbol))
hour = Unit(dimensions.time, "hr", ["hrs", "hours", "hour"], metric=False, base=(3600 * second.symbol))
day = Unit(dimensions.time, "day", ["days"], metric=False, base=(86400 * second.symbol))
week = Unit(dimensions.time, "week", ["weeks"], metric=False, base=(7 * 86400 * second.symbol))
year = Unit(dimensions.time, "yr", ["year", "years", "yrs"], base=(86400 * 365.25 * second.symbol))

# Additional temperature units
# TODO celsius = Unit(dimensions.temperature, "°C", ["degrees_celsius", "°celsius", "celsius"], base=(1 + 273.15 * kelvin.symbol))
# TODO fahrenheit = Unit(dimensions.temperature, "°F", ["degrees_fahrenheit", "°fahrenheit", "fahrenheit"], base=(1))
rankine = Unit(dimensions.temperature, "°R", ["rankine", "degrees_rankine", "°rankine"], base=((5 / 9) * kelvin.symbol))

# Additional luminosity units
lumen = Unit(dimensions.luminous_flux, "lm", ["lumen", "lumens"], base=(candela.symbol * steradian.symbol))

lux = Unit(dimensions.illuminance, "lx", ["lux"], metric=False, base=(candela.symbol * steradian.symbol * metre.symbol ** -2))
foot_candle = Unit(dimensions.illuminance, "fc", ["foot_candle", "ft_c"], metric=False, base=(lumen.base * foot.base ** -2))
phot = Unit(dimensions.illuminance, "ph", ["phot", "phots"], metric=False, base=(10000 * lux.base))

# Additional mass units
tonne = Unit(dimensions.mass, "t", ["tonne", "tonnes", "metric_ton", "metric_tons"], metric=False, base=(1000000 * gram.symbol))
dalton = Unit(dimensions.mass, "Da", ["u", "dalton", "daltons"], base=(1.6604390666050 * 10 ** -24 * gram.symbol))
slug = Unit(dimensions.mass, "sl", ["slug", "slugs"], metric=False, base=(14593.90 * gram.symbol))
pound = Unit(dimensions.mass, "lb", ["lbs", "pound", "pounds"], metric=False, base=(453.59237 * gram.symbol))
ounce = Unit(dimensions.mass, "oz", ["ounce", "ounces"], metric=False, base=(pound.base / 16))
ton = Unit(dimensions.mass, "tons", ["ton", "short_ton", "short_tons"], metric=False, base=(2000 * pound.base))
long_ton = Unit(dimensions.mass, "long_tons", ["long_ton", "imperial_ton", "imperial_tons", "displacement_ton", "displacement_tons"], metric=False, base=(2240 * pound.base))
carat = Unit(dimensions.mass, "ct", ["carat", "carats"], base=(0.2 * gram.symbol))
imperial_carat = Unit(dimensions.mass, "imp_ct", ["imp_carat", "imp_carats", "imperial_carat", "imperial_carats"], metric=False, base=(0.00705 * ounce.base))

# Additional force units
pound_force = Unit(dimensions.force, "lbf", ["pound_force, pound_of_force"], metric=False, base=(4.4482216152605 * newton.base))
dyne = Unit(dimensions.force, "dyn", ["dyne", "dynes"], metric=False, base=(10 ** -5 * newton.base))
poundal = Unit(dimensions.force, "pdl", ["poundal"], metric=False, base=(pound.base * foot.base * second.symbol ** -2))

# Additional energy units
erg = Unit(dimensions.energy, "erg", ["ergs"], metric=False, base=(10 ** -7 * joule.base))
calorie = Unit(dimensions.energy, "cal", ["calorie", "calories"], base=(4.184 * joule.base))
electron_volt = Unit(dimensions.energy, "eV", ["electronvolt", "electronvolts", "electron_volt", "electron_volts"], base=(1.602176634 * 10 ** -19 * joule.base))

# Additional power units
metric_horsepower = Unit(dimensions.power, "hp", ["hp_M", "horsepower", "metric_horsepower"], base=(735.49875 * watt.base))
mechanical_horsepower = Unit(dimensions.power, "hp_I", ["mechanical_horsepower", "imperial_horsepower"], metric=False, base=(550 * foot.base * pound_force.base / second.symbol))
electical_horsepower = Unit(dimensions.power, "hp_E", ["electrical_horsepower"], metric=False, base=(746 * watt.base))
boiler_horsepower = Unit(dimensions.power, "hp_S", ["boiler_horsepower"], metric=False, base=(9812.5 * watt.base))

# Additional pressure units
bar = Unit(dimensions.pressure, "bar", ["bars"], base=(100000 * pascal.base))
standard_atmosphere = Unit(dimensions.pressure, "atm", ["atmosphere", "atmospheres", "standard_atmosphere", "standard_atmospheres"], metric=False, base=(101325 * pascal.base))
millimetre_mercury = millimeter_mercury = Unit(dimensions.pressure, "mmHg", ["mm_Hg"], metric=False, base=(133.322 * pascal.base))
inch_mercury = Unit(dimensions.pressure, "inHg", ["in_Hg"], metric=False, base=(3386.389 * pascal.base))
torr = Unit(dimensions.pressure, "Torr", ["torr"], metric=False, base=((101325 / 760) * pascal.base))

# Additional angular measurements
degree = Unit(dimensions.angle, "°", ["deg", "degree", "degrees", "arcdegree", "arcdegrees", "degree_of_arc", "degrees_of_arc", "arc_degree", "arc_degrees"], metric=False, base=((_pi / 180) * radian.base))
turn = Unit(dimensions.angle, "tr", ["pla", "turn", "turns"], metric=False, base=(2 * _pi * radian.base))
gradian = Unit(dimensions.angle, "gon", ["ᵍ", "grad", "grade", "grads", "grades"], metric=False, base=((_pi / 200) * radian.base))
square_degree = Unit(dimensions.solid_angle, "square_deg", ["sq_deg", "square_degree", "square_degrees"], metric=False, base=((_pi / 180) ** 2 * steradian.base))
arcminute = Unit(dimensions.angle, "arcmin", ["arc_minute", "arc_minutes", "arcminute", "arcminutes", "minute_arc", "minutes_arc"], metric=False, base=(degree.base / 60))
arcsecond = Unit(dimensions.angle, "as", ["arcsec", "asec", "arc_second", "arc_seconds", "arcsecond", "arcseconds", "second_of_arc", "seconds_of_arc"], base=(arcminute.base / 60))


# Additional volume units
litre = liter = Unit(dimensions.volume, "L", ["l", "ℓ", "liter", "litre", "liters", "litres"], base=(10 ** -3 * metre.symbol))
us_gallon = Unit(dimensions.volume, "US_gal", ["US_gallon", "US_gallons"], metric=False, base=(231 * inch.base ** 3))
us_dry_gallon = Unit(dimensions.volume, "US_dry_gal", ["US_dry_gallon", "US_dry_gallons"], metric=False, base=(268.8025 * inch.base ** 3))
imperial_gallon = Unit(dimensions.volume, "imp_gal", ["imperial_gallon", "imp_gallon", "imperial_gallons", "imp_gallons"], metric=False, base=(4.54609 * litre.base))
us_quart = Unit(dimensions.volume, "US_qt", ["US_quart", "US_quarts"], metric=False, base=(us_gallon.base / 4))
us_dry_quart = Unit(dimensions.volume, "US_dry_qt", ["US_dry_quarts", "US_dry_quart"], metric=False, base=(us_dry_gallon.base / 4))
imperial_quart = Unit(dimensions.volume, "imp_qt", ["imperial_quart", "imp_quart", "imperial_quarts", "imp_quarts"], metric=False, base=(imperial_gallon.base / 4))
# TODO cup https://en.wikipedia.org/wiki/Cup_(unit)
# TODO tablespoon https://en.wikipedia.org/wiki/Tablespoon
# TODO teaspoon https://en.wikipedia.org/wiki/Teaspoon
us_fluid_ounce = Unit(dimensions.volume, "US_fl_oz", ["US_fluid_ounce", "US_fluid_ounces"], metric=False, base=(us_gallon.base / 128))
imperial_fluid_ounce = Unit(dimensions.volume, "imp_fl_oz", ["imp_fluid_ounce", "imp_fluid_ounces", "imperial_fluid_ounce", "imperial_fluid_ounces"], metric=False, base=(imperial_gallon.base / 160))
us_peck = Unit(dimensions.volume, "US_peck", ["US_pecks"], metric=False, base=(2 * us_gallon.base))
imperial_peck = Unit(dimensions.volume, "imp_peck", ["imp_pecks", "imperial_peck", "imperial_pecks"], metric=False, base=(2 * imperial_gallon.base))
us_bushel = Unit(dimensions.volume, "US_bushel", ["US_bushels", "US_bu", "US_bsh"], metric=False, base=(8 * us_gallon.base))
imperial_bushel = Unit(dimensions.volume, "imp_bushel", ["imp_bushels", "imperial_bushel", "imperial_bushels", "imp_bu", "imp_bsh"], metric=False, base=(8 * imperial_gallon.base))

# Additional velocity units
mile_per_hour = Unit(dimensions.velocity, "mph", ["miles_per_hour", "mile_per_hour"], metric=False, base=(mile.base / hour.base))
knot = Unit(dimensions.velocity, "kt", ["knots", "kn", "knot"], metric=False, base=(1852 * metre.symbol / hour.base))

# Additional area units
acre = Unit(dimensions.area, "acre", ["ac", "acres"], metric=False, base=(4840 * yard.base ** 2))
hectare = Unit(dimensions.area, "ha", ["hectare", "hectares"], metric=False, base=(10 ** 4 * metre.symbol ** 2))

_units = [
    # Base Units
    metre, second, mole, ampere, kelvin, candela, gram,

    # Derived Units
    hertz, radian, steradian, newton, pascal, joule, watt, coulomb, volt, farad, ohm, siemens, weber, tesla, henry,

    # Astronomical Units
    mass_sun, parsec, astronomical_unit, lightyear, solar_luminosity,

    # Additional length units
    fermi, angstrom, micron, yard, foot, inch, mile, fathom, nautical_mile, furlong,

    # Additional time units
    minute, hour, day, week, year,

    # Additional temperature units
    rankine,  # TODO celsius, fahrenheit

    # Additional luminosity units
    lumen, lux, foot_candle, phot,

    # Additional mass units
    tonne, dalton, slug, pound, ounce, ton, long_ton, carat, imperial_carat,

    # Additional force units
    pound_force, dyne, poundal,

    # Additional energy units
    erg, calorie, electron_volt,

    # Additional power units
    metric_horsepower, mechanical_horsepower, electical_horsepower, boiler_horsepower,

    # Additional pressure units
    bar, standard_atmosphere, millimetre_mercury, inch_mercury, torr,

    # Additional angle units
    degree, turn, gradian, square_degree, arcminute, arcsecond,

    # Additional volume units
    litre, us_gallon, us_dry_gallon, imperial_gallon, us_quart, us_dry_quart, imperial_quart, us_fluid_ounce,
    imperial_fluid_ounce, us_peck, imperial_peck, us_bushel, imperial_bushel,

    # Additional velocity units
    mile_per_hour, knot,

    # Additional area units
    acre, hectare,
]


for unit in list(_units):
    for prefix in unit.generate_metric_prefixes():
        _units.append(prefix)

library = UnitLibrary()
library.add_all(_units)


def lookup(unit_to_lookup):
    return library.lookup(unit_to_lookup)


def to_base_units(expr):
    changes = -1
    while changes != 0:
        changes = 0
        for symbol in expr.free_symbols:
            try:
                _unit = library.lookup(symbol)
                if _unit.base is True:
                    continue
                changes += 1
                expr = expr.subs(symbol, _unit.base)
            except KeyError:
                continue
    return expr
