import datetime

def generate_id():
    # Get the current date in the format YYYYMMDD
    date_part = datetime.datetime.now().strftime("%d%m%Y")

    # You may replace this with a database query to get the latest number
    # This is a placeholder, and you should adapt it based on your storage mechanism
    latest_number = 1

    # Generate the ID by combining the date and number
    generated_id = f"{date_part}-{latest_number:03d}"

    return generated_id

# Example usage:
id_result = generate_id()
print(id_result)
