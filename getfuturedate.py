from datetime import date
import datetime
from dateutil.relativedelta import relativedelta



def main():
    today = date.today()
    threemonths = datetime.datetime.now() + relativedelta(months=3)
    print("Today's date is ", today)
    print("3 months from today ", threemonths.strftime("%Y-%m-%d"))


if __name__ == "__main__":
    main()


