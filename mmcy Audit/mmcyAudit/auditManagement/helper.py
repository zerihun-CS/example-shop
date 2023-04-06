from PIL import Image
from datetime import datetime, timedelta
def is_image(file):
    try:
        img = Image.open(file)
        img.verify()
        return True
    except:
        return False
def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        

def date_range_append(date):
    date_list = []
    if date:
      start_date = date.start_date
      end_date = date.ending_date
    else:
      start_date = datetime.today()
      end_date = datetime.today() + timedelta(days=3)
    # date range from the admin
    for single_date in date_range(start_date, end_date):
      single_date.strftime("Y-m-d")
      date_list.append(single_date)
    
    return date_list