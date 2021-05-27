# =====================================================
# CREDITS: CEMC University of Waterloo
# =====================================================

import random

class Challenges:
    def __init__(self):
        self.geometry = [
            ['In the diagram, P QRS is a quadrilateral. What is its perimeter?', 'https://i.ibb.co/L1JnPDL/Screen-Shot-2021-05-27-at-1-47-28-PM.png']
        ]
        self.algebra = []
        self.all = [self.geometry, self.algebra]

    def getChallenge(self):
        # category = random.randint(0, len(all)-1)
        # problem = random.randint(0, len(all[category])-1)
        # return all[category][problem]
        return self.geometry[0]