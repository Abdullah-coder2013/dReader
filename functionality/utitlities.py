import hashlib
from datetime import datetime
def dateEncoder(date, mode):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    if mode == "date":
        try:
        # Convert named date to YYYY MM DD
            fdate = date.replace(",", "")
            fdate = fdate.split(" ")
            month = months.index(fdate[0])+1
            day = fdate[1][:-2]
            if len(day) == 1:
                day = f"0{day}"
            elif len(str(month)) == 1:
                month = f"0{month}"
            year = fdate[2]
            return f"{year}-{month}-{day}"
        except:
            return date
    else:
        try:
            fdate = date.split("-")
            year = fdate[0]
            month = fdate[1]
            day = fdate[2]
            
            # Convert month to name
            
            month = months[int(month) - 1]
            
            # Convert day to name
            if day[-1] == "1":
                day = f"{day}st"
            elif day[-1] == "2":
                day = f"{day}nd"
            elif day[-1] == "3":
                day = f"{day}rd"
            else:
                day = f"{day}th"
            
            return f"{month} {day}, {year}"
        except:
            return date

def hashgen(password):
    salt = "2e78f89c6"
    passwordtohash = password + salt
    return hashlib.sha256(passwordtohash.encode()).hexdigest()

def reformat_date(date_str):
    date_str = date_str.replace(".", "")
    try:
        date_obj = datetime.strptime(date_str, '%B %d, %Y')
    except ValueError:
        date_obj = datetime.strptime(date_str, '%b %d, %Y')
    return date_obj.strftime('%Y-%m-%d')