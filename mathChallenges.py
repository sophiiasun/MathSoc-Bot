# =====================================================
# CREDITS: CEMC University of Waterloo
# =====================================================

import random

class Challenges:
    def __init__(self):
        self.geometry = [
            ['In the diagram, PQRS is a quadrilateral. What is its perimeter?', 'https://i.ibb.co/L1JnPDL/Screen-Shot-2021-05-27-at-1-47-28-PM.png'],
            ['In the diagram, A has coordinates (0, 8). Also, the midpoint of AB is M(3, 9) and the midpoint of BC is N(7, 6). What is the slope of AC?', 'https://i.ibb.co/Q8sMGSP/Screen-Shot-2021-05-27-at-2-27-24-PM.png']
            ['Rectangle ABCD has *AB* = 4 and *BC* = 6. The semi-circles with diameters *AE* and *FC* each have radius *r*, have centres *S* and *T*, and touch at a single point *P*, as shown. What is the value of *r*?', 'https://i.ibb.co/JBn6rRz/Screen-Shot-2021-05-28-at-11-06-53-AM.png']
            ['In the diagram, △*ABE* is right-angled at *A*, △*BCD* is right-angled at *C*, ∠*ABC* = 135◦, and *AB* = *AE* = 7√2. If *DC* = 4*x*, *DB* = 8*x* and *DE* = 8*x* − 6 for some real number *x*, determine all possible values of *x*', 'https://i.ibb.co/rFB7bZj/Screen-Shot-2021-05-28-at-11-10-25-AM.png']    
        ]
        self.algebra = [
            ['Determine all values of *x* for which (refer to diagram below~)', 'https://i.ibb.co/ykn59ZW/Screen-Shot-2021-05-27-at-2-29-26-PM.png'],
            ['What is the vale of the real number *x*? Refer to diagram below.', 'https://i.ibb.co/xJhfCwM/Screen-Shot-2021-05-27-at-2-30-53-PM.png'],
            [' Suppose that *n* is a positive integer and that the value of the expression in the image below is an integer. Determine all possible values of *n*.', ]
        ]
        self.all = [self.geometry, self.algebra]

    def getCategory(self, choice):
        # choice = choice.lower()
        if choice == 'random':
            return -1
        if choice == 'geometry':
            return 0
        return 1

    def getChallenge(self, choice = 'rand'): # -1 --> rand, 0 --> geo, etc.
        category = self.getCategory(choice)
        problem = random.randint(0, len(self.all[category])-1)
        return self.all[category][problem]