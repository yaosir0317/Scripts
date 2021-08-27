from unittest import TestCase, main as run_test_case


class ClassOnlyMethod(classmethod):
    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError("This method is available only on the class, not on instances.")
        return super().__get__(instance, cls)


class A(object):
    a = 123

    @classmethod
    def func(cls):
        return cls.a

    @ClassOnlyMethod
    def func_class(cls):
        return cls.a


class TestClassOnlyMethod(TestCase):
    def setUp(self):
        super().setUp()
        self.value = 123
        self.obj = A()
        self.A = A
        self.e = "This method is available only on the class, not on instances."

    def test_class_method(self):
        self.assertEqual(self.A.func(), self.value)
        self.assertEqual(self.obj.func(), self.value)

    def test_class_only_method(self):
        self.assertEqual(self.A.func_class(), self.value)
        self.assertRaises(AttributeError, lambda: self.obj.func_class())


if __name__ == '__main__':
    run_test_case()
