import math, pygame

class Star:
    """Class representing the stellar objects in the simulation. Acts as the
    data model class of the simulation."""
    
    def __init__(self, xpos, ypos, mass, radius, startingVelocity_x, startingVelocity_y):
        """Initialise a new stellar object, storing its position, mass, radius
        and starting velocity.

        Constructor: Star(float, float, int, int, float, float)
        
        """
        
        self.starMass = mass
        self.starRadius = radius
        self.xpos = xpos
        self.ypos = ypos

        self.vel_x = startingVelocity_x
        self.vel_y = startingVelocity_y

        self.acc = 0
        
    def grav_builder(self, dist_x, dist_y, sourceMass):
        """Given the x and y distance to another object, as well as that
        object's mass, return the components of the gravitational acceleration
        imparted by that mass.

        grav_builder(float, float, int) -> (float, float)
        
        """
        
        self.metres_x = 748000000*dist_x
        self.metres_y = 748000000*dist_y
        try:
            self.mod = math.pow((self.metres_x), 2) + math.pow((self.metres_y), 2)
        except OverflowError:
            return 0, 0
        self.radial = math.sqrt(self.mod)
        G = 0.0000000000667*2000000
        
        if self.radial > 0:
            self.acc = G*sourceMass*(1/(math.pow(self.radial, 2)))
        if self.metres_x != 0:
            self.acc_x = self.acc*(self.metres_x/self.radial)
        if self.metres_y != 0:
            self.acc_y = self.acc*(self.metres_y/self.radial)

        if self.metres_x != 0 and self.metres_y != 0:
            return self.acc_x, self.acc_y
        elif self.metres_x != 0:
            return self.acc_x, 0
        elif self.metres_y != 0:
            return 0, self.acc_y
        else:
            return 0, 0

    def move_stellar(self, change_x, change_y):
        """Given an object's intended x and y change in metres, move
        the object by the appropriate number of pixels.

        move_stellar(float, float) -> None
        
        """
        self.xpos += change_x/748000000 # converting to change in px.
        self.ypos += change_y/748000000

    def check_collide(self, stellar_object):
        """Check if the stellar object given is colliding with the
        stellar object this method is called on.

        check_collide(stellar_object) -> Boolean

        """

        dist_x = self.xpos - stellar_object.xpos
        dist_y = self.ypos - stellar_object.ypos

        try:
            radial = math.sqrt(dist_x**2+dist_y**2)
        except OverflowError:
            return False

        if radial < (self.starRadius+stellar_object.starRadius):
            return True
        else:
            return False

    def absorb(self, stellar_object):
        """Absorb the stellar object given, into the object this method
        is called on. Modify the momentum, mass and radius of the latter object
        accordingly.

        absorb(stellar_object) -> None
        
        """

        # Momentum
        self.vel_x = ((self.vel_x*self.starMass+
                      stellar_object.vel_x*stellar_object.starMass)/
                        (self.starMass+stellar_object.starMass))
        self.vel_y = ((self.vel_y*self.starMass+
                      stellar_object.vel_y*stellar_object.starMass)/
                        (self.starMass+stellar_object.starMass))

        # Mass & Radius
        self.change_mass(stellar_object.starMass)
        if self.starRadius < 25:
            self.change_radius(stellar_object.starRadius*0.25)
        else:
            self.change_radius(stellar_object.starRadius*0.05)

    def clone(self):
        """Return a copy of this stellar object.

        clone() -> stellar_object

        """

        return Star(self.xpos, self.ypos, self.starMass,
                        self.starRadius, self.vel_x, self.vel_y)
        

    def get_mass(self):
        """Return the mass of this object.

        get_mass() -> int

        """
        return self.starMass

    def change_mass(self, change):
        """Modify the mass of this object, by the given amount.

        change_mass(int) -> None

        """
        self.starMass += change

    def change_radius(self, change):
        """Modify the radius of this object, by the given amount.

        change_radius(float) -> None

        """
        self.starRadius += int(change)
        
