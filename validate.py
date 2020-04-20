import datetime

class validate:

    def __init__(self, valinput,valformat):
        self.valinput = valinput
        self.valformat = valformat

    def validate_date(self):
        try:
            datetime.datetime.strptime(self.valinput, self.valformat)
            return True
        except ValueError:
            #raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            return False



