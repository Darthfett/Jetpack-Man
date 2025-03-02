class CollisionBlock:

    objects = set()
    
    def isInBlock(self,object):
        # Return whether self and objects' collisionRect overlap
        return False
        
    def __init__(self,position,size):
        self.position = position
        self.maxPosition = [position[0] + size[0],position[1] + size[1]]
        