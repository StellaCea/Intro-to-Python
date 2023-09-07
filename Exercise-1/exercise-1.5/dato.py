class Date(object):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
    
    def get_date(self):
        output = str(self.day) + "/" + str(self.month) + "/" + str(self.year)
        return output
    
    def is_leap_year(self):
        return self.year % 4 == 0
    
    def is_valid_date(self):
        if not(type(self.day) == int and type(self.month) == int and type(self.year) == int):
            return False
        # Make sure the year isn't negative
        if self.year < 0:
            return False
        # Check if the month is between 1 and 12
        if self.month < 1 or self.month > 12:
            return False
        #Verify if the day is valid for a given month. Store last days of each month in a dictionary: key:month, value:number of days
        last_days = {
            1: 31,
            2: 29 if self.is_leap_year() else 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }
        #Verify if the day is valid for a given month
        if self.day < 1 or self.day > last_days.get(self.month):
            return False

        return True
    
# Initialize a few Date objects
date1 = Date(29, 2, 2000)
date2 = Date(29, 2, 2001)
date3 = Date("abc", "ghi", "thr")

print(str(date1.get_date()) + ": " + str(date1.is_valid_date()))
print(str(date2.get_date()) + ": " + str(date2.is_valid_date()))
print(str(date3.get_date()) + ": " + str(date3.is_valid_date()))