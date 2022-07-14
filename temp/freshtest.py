class ClassA(object):
    def __init__(self):
        self.var1 = 1
        self.var2 = 2

    def methodA(self):
        self.var1 = self.var1 + self.var2
        return self.var1


class ClassB(ClassA):
    def __init__(self):
        super().__init__()
        print("var1",self.var1)
        print("var2",self.var2)


object1 = ClassB()
sum = object1.methodA()
print(sum)