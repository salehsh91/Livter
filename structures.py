from object import *

class Structers:
    @classmethod
    def Tree(cls,world,centerx,centery):
        base_x = world.base_x
        base_y = world.base_y
        centery -= 4*BLOCK_SIZE
        def objc(x,y,z,name):
            x *= BLOCK_SIZE
            y *= BLOCK_SIZE
            return obj(centerx+x,centery+y,z,name=name,offset_x=base_x,offset_y=base_y)
        tree = [objc(0,0,1,"oak"),objc(0,0,2,"oak"),objc(0,0,3,"oak"),objc(0,0,4,"oak"),
                objc(-2,1,4,"leaves"),objc(-2,0,4,"leaves"),objc(-2,-1,4,"leaves"),
                objc(-1,1,4,"leaves"),objc(-1,0,4,"leaves"),objc(-1,-1,4,"leaves"),objc(-1,-2,4,"leaves"),objc(-1,2,4,"leaves"),
                objc(-1,1,5,"leaves"),objc(-1,0,5,"leaves"),objc(-1,-1,5,"leaves"),objc(-1,-2,5,"leaves"),objc(-1,2,5,"leaves"),
                objc(0,2,4,"leaves"),objc(0,1,4,"leaves"),objc(0,-1,4,"leaves"),objc(0,-2,4,"leaves"),
                objc(0,2,5,"leaves"),objc(0,1,5,"leaves"),objc(0,-1,5,"leaves"),objc(0,-2,5,"leaves"),objc(0,0,5,"leaves"),
                objc(1,1,4,"leaves"),objc(1,0,4,"leaves"),objc(1,-1,4,"leaves"),objc(1,-2,4,"leaves"),objc(1,2,4,"leaves"),
                objc(1,1,5,"leaves"),objc(1,0,5,"leaves"),objc(1,-1,5,"leaves"),objc(1,-2,5,"leaves"),objc(1,2,5,"leaves"),
                objc(2,1,4,"leaves"),objc(2,0,4,"leaves"),objc(2,-1,4,"leaves"),
                ]
        for i in tree:
            i.create()
