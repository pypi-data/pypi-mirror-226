from sympy import symbols as _symbols


class Dimension:
    def __init__(self, name, dimension=None):
        if dimension is None:
            self.name = name
            self.dimension = _symbols(name, positive=True, real=True)
        else:
            self.name = name
            self.dimension = dimension

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name + " = " + str(self.dimension)


# SI Base Dimensions
length = Dimension("length")
time = Dimension("time")
amount = Dimension("amount")
current = Dimension("current")
temperature = Dimension("temperature")
luminous_intensity = Dimension("luminous_intensity")
mass = Dimension("mass")


# Derived Dimensions
frequency = Dimension("frequency", time.dimension**-1)
angle = Dimension("angle", length.dimension/length.dimension)
solid_angle = Dimension("solid_angle", (length.dimension**2)/(length.dimension**2))
force = Dimension("force", mass.dimension*length.dimension/(time.dimension**2))
pressure = Dimension("pressure", force.dimension*length.dimension**-2)
energy = Dimension("energy", force.dimension*length.dimension)
power = Dimension("power", energy.dimension / time.dimension)
charge = Dimension("charge", time.dimension * current.dimension)
electric_potential = Dimension("electric_potential", power.dimension / current.dimension)
capacitance = Dimension("capacitance", charge.dimension / electric_potential.dimension)
resistance = Dimension("resistance", electric_potential.dimension / current.dimension)
conductance = Dimension("conductance", 1 / resistance.dimension)
magnetic_flux = Dimension("magnetic_flux", energy.dimension / current.dimension)
magnetic_induction = Dimension("magnetic_induction", magnetic_flux.dimension * length.dimension**-2)
electric_inductance = Dimension("electric_inductance", resistance.dimension * time.dimension)
luminous_flux = Dimension("luminous_flux", luminous_intensity.dimension * solid_angle.dimension)
illuminance = Dimension("illuminance", luminous_flux.dimension * length.dimension**-2)
volume = Dimension("volume", length.dimension**3)
velocity = Dimension("velocity", length.dimension / time.dimension)
area = Dimension("area", length.dimension**2)
