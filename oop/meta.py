class TestMetaClass(type):
    def __new__(cls, name, bases, attrs):
        new_attrs = dict()
        for k, v in attrs.items():
            if hasattr(v, "__call__"):
                new_attrs[k] = v
            else:
                new_attrs[f"_{k}"] = v
                new_attrs[f"get_{k}"] = lambda self: getattr(self, f"_{k}")
                new_attrs[f"set_{k}"] = lambda self, x: setattr(self, f"_{k}", x)
        return super(TestMetaClass, cls).__new__(cls, name, bases, new_attrs)


if __name__ == '__main__':
    class A(metaclass=TestMetaClass):
        a = 1
        b = 100


    obj = A()
    print(obj.get_a())
    obj.set_a(4)
    print(obj.get_a())

    print(obj.get_b())
    obj.set_b(4)
    print(obj.get_b())
