import random as rn

from art import Art

class SyracuseArt(Art):
    def __init__(self):
        super(SyracuseArt, self).__init__()

    def f(self, val, lst):
        lst.append(val)

        if val == 1:
            return
        elif val % 2 == 0:
            return self.f(val / 2, lst)
        else:
            return self.f(3 * val + 1, lst)

    def compute_syracuse(self, val, randmin=50000, randmax=200000000000):
        numbers = rn.sample(range(randmin, randmax), val)

        for n in numbers:
            # print(f'Computing for {number}')
            test = []
            self.f(n, test)
            test.reverse()
            self.all_curves.append(test)
