from Main.Animation import Animation
import os

class ObjectType:
    """
    An ObjectType contains data that is common to all Entities of the same type.

    e.g. all ObjectTypes have the same Animations.
    """
    
    Height = 0
    Width = 0
    
    ObjectTypes = {}

    def addAnimation(self, name, animation):
        """
        Adds the name of an animation and the path to the file into a dictionary for later use.
        """
        self.width = max(self.width,animation.width)
        self.height = max(self.height,animation.height)
        self.animations[name] = animation

    def __init__(self, name, idle):
        """
        Defines a type of Object with a name and a default 'idle' animation.
        """
        
        ObjectType.ObjectTypes[name] = self
        self.name = name
        #Data
        #Animations
        self.animations = {}
        self.animations['idle'] = idle
        self.width = idle.width
        self.height = idle.height

    @staticmethod
    def initializeObjectTypes():
        """
         parses through all subdirectories under 'src\Main\ObjectType\' to create the ObjectTypes and add their respective
            animations contained in the anim.dat file
        
         anim.dat: comments start with a '#'.
            each non-commented line should start with the name of the animation.
            after the name, place a colon, then a relative path to the sprite image.
            separate multiple images with a ','.
        """
        
        print "Initializing Object Types"
        dir = os.path.dirname(__file__)
        for ObjectTypeName in os.listdir(dir):
            if (not os.path.isdir(os.path.join(dir, ObjectTypeName))):
                continue
            objectType = None

            animations = []
            keys = []

            animData = open(os.path.join(dir, os.path.join(ObjectTypeName, 'anim.dat'))).readlines()
            for line in animData:
                line.strip()
                if (line.startswith('#') or line == ''):
                    # commented lines start with a # sign
                    continue
                # keys are denoted first, and separated from the values via a ':'
                # multiple values are separated by ','
                animation = Animation()
                values = line.split(':')
                key = values.pop(0)
                if (key == 'idle'):
                    idle = animation

                else:
                    animations.append(animation)
                    keys.append(key)
                values = values.pop(0).split(',')
                for val in values:
                    val = val.strip()
                    animation.add(os.path.join(dir, os.path.join(ObjectTypeName, val)))
            objectType = ObjectType(ObjectTypeName,idle)
            for animation in animations:
                objectType.addAnimation(keys.pop(0), animation)
            
