from abc import ABC, abstractmethod
import dill


class A(ABC):

    @abstractmethod
    def test(self, a):
        """Abstract method"""


class B(A):

    def test(self, a):
        return a + 1


if __name__ == '__main__':
    test_obj = B()
    with open('test_save.pkl', 'wb') as f:
        dill.dump(test_obj, f)
