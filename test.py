class A:
    a: int
    b: int

    def __str__(self):
        return f"o.a = {self.a}, o.b = {self.b}"

    def __del__(self):
        print("End of objects life!")


def sample(o: A, l: list):
    x = A()
    x.a = l[-1].a + 1
    x.b = l[-1].b + 1
    l.append(x)


a = A()
a.a = 1
a.b = 2
l = [a]
for i in range(10):
    sample(a, l)

for i in l:
    print(i, id(i))
