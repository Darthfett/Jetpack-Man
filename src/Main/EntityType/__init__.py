from Main.Animation import Animation
import os

class EntityType:
    EntityTypes = {}

    def addAnimation(self, name, animation):
        self.animations[name] = animation

    def __init__(self, name, idle):
        EntityType.EntityTypes[name] = self
        #Data
        #Animations
        self.animations = {}
        self.animations['idle'] = idle

    @staticmethod
    def initializeEntityTypes():
        print "Initializing Entity Types"

        # parsing through all subdirectories under 'Megaman Remake\src\Main\EntityType\' to create the EntityTypes and add their respective
        #    animations contained in the anim.dat file
        #
        # anim.dat: comments start with a '#'.
        #    each non-commented line should start with the name of the animation.
        #    after the name, place a colon, then a relative path to the sprite image.
        #    separate multiple images with a ','.
        dir = os.path.abspath(os.path.join(os.getcwd(), 'EntityType'))
        #dir = os.getcwd()
        print os.getcwd()
        print dir
        print os.listdir(dir)
        os.chdir(dir)
        dir = os.getcwd()
        for entityTypeName in os.listdir(dir):
            print entityTypeName, os.path.isdir(entityTypeName)
            if (not os.path.isdir(entityTypeName)):
                continue
            entityType = None

            animations = []
            keys = []

            animData = open(os.path.join(dir, os.path.join(entityTypeName, 'anim.dat'))).readlines()
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
                    print 'entity type definition:', entityTypeName
                    entityType = EntityType(entityTypeName, animation)
                else:
                    animations.append(animation)
                    keys.append(key)
                    values = values.pop(0).split(',')
                    #print 'values:'
                    for val in values:
                        val = val.strip()
                        #print val
                        animation.add(os.path.join(entityTypeName, val))
            for animation in animations:
                    entityType.addAnimation(keys.pop(0), animation)
