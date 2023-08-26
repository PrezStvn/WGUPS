# class DeliverySimulator:
#     __init__
#
#
# def package_status_at_time(packages, driver1_calculated_times, driver2_calculated_times, target_time):
#     # tracker that changes all packages['Status'] 'At the hub' --> 'en route'
#     # tracker for driver1 can be driver1_calculated_times[0][1]?
#     # tracker for driver2 can only initialize packages up to the package that driver2_calculated_times[i][0] == 'Hub'
#     # custom logic to detect when package id == 'Hub'  then set packages succeeding hub to en route
#     # Convert start_time (string) to hours and minutes
#     hours, minutes = map(int, target_time.split(":"))
#
#     # Convert hours and minutes to total minutes
#     target_time_in_minutes = hours * 60 + minutes

class DeliverySim:
    # O(n)
    def __init__(self, packages, driver1_calculated_times, driver2_calculated_times, target_time):
        self.packages = packages
        self.driver1_times = dict(driver1_calculated_times)
        self.driver2_times = dict(driver2_calculated_times)
        self.target_time = target_time
        # Convert target_time (string) to hours and minutes
        hours, minutes = map(int, target_time.split(":"))

        # Convert hours and minutes to total minutes
        self.target_time_in_minutes = hours * 60 + minutes

    def print_package_status(self):
        current_package_id = 1
        # for package_id, package in self.packages.table:
        #     print(f'Package ID: {package_id} Address: {package["Address"]} Status: {package["Status"]}')
        for package in self.packages.status():
            print(f'Package ID: {current_package_id} Address: {package["Address"]} Status: {package["Status"]}')
            current_package_id += 1

    def check_package_status(self):
        for package_id, package_delivery_time in self.driver1_times.items():
            if package_delivery_time <= self.target_time_in_minutes:
                delivery_hour = int(package_delivery_time // 60)
                delivery_minute = int(package_delivery_time % 60)
                package = self.packages.get(package_id)
                package['Status'] = f"Delivered by Driver 1 on Truck 1 at {delivery_hour:02}:{delivery_minute:02}"
                self.packages.put(package_id, package)
            else:
                package = self.packages.get(package_id)
                package['Status'] = 'In Transit or At the Hub'
                self.packages.put(package_id, package)
        current_truck = 3
        for package_id, package_delivery_time in self.driver2_times.items():

            if package_id == 'HUB':
                current_truck = 2
                continue
            if package_delivery_time <= self.target_time_in_minutes:
                delivery_hour = int(package_delivery_time // 60)
                delivery_minute = int(package_delivery_time % 60)
                package = self.packages.get(package_id)
                package['Status'] = f"Delivered by Driver 2 on Truck {current_truck} at {delivery_hour:02}:{delivery_minute:02}"
                self.packages.put(package_id, package)
            else:
                package = self.packages.get(package_id)
                package['Status'] = 'In Transit or At the Hub'
                self.packages.put(package_id, package)
        self.print_package_status()

    def get_package_status(self, package_id):
        return self.packages.get(package_id, {}).get('Status', 'Package not found')




# # Example Usage:
# packages = [
#     {'Package ID': '1', 'Address': '123 Street', 'Other Info': 'XYZ'},
#     # ... add other packages
# ]
#
# driver1_calculated_times = [('1', '08:15')]
# driver2_calculated_times = []
# target_time = '08:20'
#
# simulator = DeliverySimulator(packages, driver1_calculated_times, driver2_calculated_times, target_time)
# status = simulator.check_package_status()
# print(status['1'])  # It should display: 'Delivered by Driver 1 at 08:15'