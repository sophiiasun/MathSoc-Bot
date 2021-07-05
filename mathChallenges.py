# =======================================================================================
# CREDITS: CEMC University of Waterloo, American Mathematics Competitions
# =======================================================================================

import random

class Challenges:
    def __init__(self):
        self.geometry = [ # problem, image, credits, solution
            ['In the diagram, *PQRS* is a quadrilateral. What is its perimeter?', 'https://i.ibb.co/L1JnPDL/Screen-Shot-2021-05-27-at-1-47-28-PM.png', '13', 'CEMC Euclid 2021—Q3(a)'],
            ['In the diagram, *A* has coordinates (0, 8). Also, the midpoint of *AB* is *M*(3, 9) and the midpoint of *BC* is *N*(7, 6). What is the slope of *AC*?', 'https://i.ibb.co/Q8sMGSP/Screen-Shot-2021-05-27-at-2-27-24-PM.png', '-3/4', 'CEMC Euclid 2021—Q3(b)'],
            ['Rectangle ABCD has *AB* = 4 and *BC* = 6. The semi-circles with diameters *AE* and *FC* each have radius *r*, have centres *S* and *T*, and touch at a single point *P*, as shown. What is the value of *r*?', 'https://i.ibb.co/JBn6rRz/Screen-Shot-2021-05-28-at-11-06-53-AM.png', '13/6', 'CEMC Euclid 2020—Q6(a)'],
            ['In the diagram, △*ABE* is right-angled at *A*, △*BCD* is right-angled at *C*, ∠*ABC* = 135◦, and *AB* = *AE* = 7√2. If *DC* = 4*x*, *DB* = 8*x* and *DE* = 8*x* − 6 for some real number *x*, determine all possible values of *x*', 'https://i.ibb.co/rFB7bZj/Screen-Shot-2021-05-28-at-11-10-25-AM.png', '10', 'CEMC Euclid 2020—Q6(b)'],
            ['A regular pentagon covers part of another regular polygon, as shown. This regular polygon has *n* sides, five of which are completely or partially visible. In the diagram, the sum of the measures of the angles marked *a*◦ and *b*◦ is 88◦. Determine the value of *n*. (The side lengths of a regular polygon are all equal, as are the measures of its interior angles.)', 'https://i.ibb.co/ZmQCZqL/Screen-Shot-2021-05-29-at-9-08-13-PM.png', '9', 'CEMC Euclid 2019—Q6(a)'],
            ['Three identical rectangles *PQRS*, *WTUV* and *XWVY* are arranged, as shown, so that *RS* lies along *TX*. The perimeter of each of the three rectangles is 21 cm. What is the perimeter of the whole shape?', 'https://i.ibb.co/j8vdBWn/Screen-Shot-2021-05-29-at-9-46-59-PM.png', '42', 'CEMC Euclid 2017—Q3(b)']
        ]
        self.algebra = [
            ['Determine all values of *x* for which (refer to diagram below~)', 'https://i.ibb.co/ykn59ZW/Screen-Shot-2021-05-27-at-2-29-26-PM.png', '-1/2, 1/2', 'CEMC Euclid 2021-Q1(c)'],
            ['What is the vale of the real number *x*? Refer to diagram below.', 'https://i.ibb.co/xJhfCwM/Screen-Shot-2021-05-27-at-2-30-53-PM.png', '58/3', 'CEMC Euclid 2021-Q4(a)'],
            ['Suppose that *n* is a positive integer and that the value of the expression in the image below is an integer. Determine all possible values of *n*.', 'https://i.ibb.co/dP9S192/Screen-Shot-2021-05-28-at-11-14-00-AM.png', '1, 3, 5, 15', 'CEMC Euclid 2020—Q2(c)'],
            ['Linh is driving at 60 km/h on a long straight highway parallel to a train track. Every 10 minutes, she is passed by a train travelling in the same direction as she is. These trains depart from the station behind her every 3 minutes and all travel at the same constant speed. What is the constant speed of the trains, in km/h?', '', '600/7', 'CEMC Euclid 2017—Q7(1)']
        ]
        self.number_theory = [
            ['Five distinct integers are to be chosen from the set {1, 2, 3, 4, 5, 6, 7, 8} and placed in some order in the top row of boxes in the diagram. Each box that is not in the top row then contains the product of the integers in the two boxes connected to it in the row directly above. Determine the number of ways in which the integers can be chosen and placed in the top row so that the integer in the bottom box is 9 953 280 000.', 'https://i.ibb.co/wN3RGPM/Screen-Shot-2021-05-29-at-9-29-03-PM.png', '8', 'CEMC Euclid 2021—Q8(a)']
        ]
        self.all = [self.geometry, self.algebra, self.number_theory]

    def getCategory(self, choice):
        # choice = choice.lower()
        if choice == 'random':
            return -1
        if choice == 'geometry':
            return 0
        if choice == 'number theory':
            return 1
        return 2

    def getChallenge(self, choice): # -1 --> rand, 0 --> geo, etc.
        category = self.getCategory(choice)
        if category == -1:
            category = random.randint(0, 2)
        problem = random.randint(0, len(self.all[category])-1)
        return self.all[category][problem]