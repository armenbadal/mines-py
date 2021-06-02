
class W:
    counter = 0

    def __init__(self):
        self.number = W.counter
        W.counter += 1
    
    def __str__(self):
        return 'W-{0}'.format(self.number)


m0 = [W() for n in range(10)]
for m in m0:
    print(m)

