def calculate_delivery_times(packages, start_time, speed=18):
    # Convert start_time (string) to hours and minutes
    hours, minutes = map(int, start_time.split(":"))

    # Convert hours and minutes to total minutes
    current_time_in_minutes = hours * 60 + minutes

    delivery_times = []

    for package, distance in packages:

        # Calculate time taken to travel the distance
        time_taken = distance / speed * 60  # in minutes
        current_time_in_minutes += time_taken
        # if we are on the return leg we skip to the next package after the time has been accumulated
        if package == 'HUB':
            continue
        # Convert total minutes back to hours and minutes for the format HH:MM
        delivery_hour = int(current_time_in_minutes // 60)
        delivery_minute = int(current_time_in_minutes % 60)

        # Append delivery time and package number to the result
        delivery_times.append((package, f"{delivery_hour:02}:{delivery_minute:02}"))

    return delivery_times


def calculate_total_distance(truck):
    distance_total = 0.0
    for package in truck:
        # the distance traveled to deliver this package is stored in package[1]
        distance_total += package[1]

    return distance_total