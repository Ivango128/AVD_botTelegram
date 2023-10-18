from datetime import datetime


current_time = datetime.now()
formatted_date = current_time.strftime("%d.%m.%Y")
print(formatted_date)
