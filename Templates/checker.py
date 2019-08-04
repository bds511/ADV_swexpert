import sys
from io import StringIO

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout




def check():

    with Capturing() as output:
        import problem


    with open("output.txt" ,"r") as solution:
        if output == list(map(str.strip,solution.readlines())):
            print("정답입니다.")
        else:
            print("틀렸습니다.")