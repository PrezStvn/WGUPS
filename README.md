# WGUPS










C950 WGUPS Algorithm Overview


Student Name
ID #004439406
WGU Email: sper314@wgu.edu
8/14/2023

C950 Data Structures and Algorithms II
 

Introduction: 
The task at hand is a variation of the Traveling Salesman Problem(TSP), we, WGUPS, need to deliver 40 packages by the end of the day.  WGUPS has 3 trucks and 2 drivers, each truck can hold 16 packages, take no time to load, do not need to stop to deliver the package, and travel at an average of 18 mph.  WGUPS needs to deliver these packages in under 140 miles and adhere to some packages specific delivery instructions, e.g. must be delivered before 10:30, or package not arriving till 9:05 am.
A. Algorithm Identification
Nearest-Neighbor algorithm:
	Given a starting address in a data structure, loop through all other addresses(packages) and determine the one with the minimum distance from our current location.
	Once found remove from old data structure and add to new list
	Repeat until no packages remain.
B1. Logic Comments
Nearest Neighbor:
This is within a SortTruck class that has access to 
Self.packages, address_map, distance_table, package_set, sorted_packages, number_of_packages
Sort_packages(self):
While length of sorted_packages < length of number_of_packages_on_truck
	current_package = nearest_neighbor(current_address)  {current_address is default to ‘hub’ address}
	current_address = current_package[‘Address]
	add this package to sorted_packages
	packages.remove(current_package)  remove from all packages
	same_address(current_package_
	return sorted_packages

nearest_neighbor(self, current_address):
	min_distance = (set to some arbitrary value greater than any in distance table)
	nearest_package = None
	for pkg in packages:
		if the address of this package is in address map set index to that value for reference
	index = address_map[package_address]
	current_index = address_map[current_address] these each represent an address index in our 2d distance_table
	#since only half of matrix is built flip indexes to not be out of bounds
	If curr_index < index
		Temp = curr
		Curr = index
		Index = curr_index
	If distance_table[of the two indices ^] < min_distance
		Min_distance = distance_table[]
		Nearest_address = current_package

	Return nearest_package

Same_address(self, address):
Same_address_list = []
	For pkg in packages:
		If package address == address
			Add current package to sorted packages
			Add to same address list[]
	For pkg in same_address_list
		Remove packages added to sorted from packages
	


B2. Development Environment
Python 3.+ in Pycharm 2023.1.4 community edition
PC Specs:
	Windows 10
	Ryzen 1 1700x
	AMD Radeon 5700xt 
	64 gigabytes DDR4 Ram
B3. Space-Time and Big-O
FileReader: O(n^2)
	read_packages(): O(n)
	read_distances(): O(n)
	csv_to_distance_matrix(): O(n^2)

TruckLoader: O(n^2)
	load_trucks(): O(n^2) calls to same_address loader && remove_used_packages
	same_address_loader(): O(n^2)
	remove_used_packages(): O(n^2)
Same_address(): O(n)
Nearest_neighbor: O(n)
Sort_packages: O(n^2) 
DeliveryCalculator: O(n)
DeliverySimulator: O(n)
Overall Space Time Complexity:
		O(n^2) since no in loop call is made to any function with a bigO >= O(n^2)

B4. Scalability and Adaptability
A lot of the solution is hard coded in to deal with constraints of this given project.  Despite that there is presently no logic to decide why a package would be on a truck prior to the trucks “loading.”  This is both good and bad.  If the trucks are still loaded arbitrarily then the max size that the sorting algorithm would ever deal with theoretically would be n = 16.  This means the program can be scaled almost infinitely, but I imagine there is a negative correlation between this algorithm’s efficiency and the number of packages to be delivered in a day. I imply that if there is no logic behind package loading on trucks, then the algorithm will always have hindered efficiency. .  
If the scenario for this project were a bit different and packages not having specific constraints(outside of being late to the hub, I mean constraints such as “must be on truck 1” or “must be delivered with package14) I most likely would have tried to place the sorting algorithm in front of my simulated loading of trucks.  My idea for a solution around this preload sorting started with choosing a package or “target” that was furthest from the hub and using the distance from the current address to the target address as a metric. My idea is a slight variation of the nearest neighbor algorithm where we would prioritize the nearest addresses but given that the distance to target(distance_to_target) < (last_distance_to_target).  So choosing a close address to the hub but while we are heading in the direction of the target address.  Until there are no addresses that would bring us near the target except for that target address itself.  Then essentially, we switch the target back to the hub and start moving back towards the hub(given some checks are done frequently to see if packages share an address or if we are at 16 packages on the truck already).  In the given scenario that last bit is only relevant if the truck must return to the hub to pick up more packages.   
B5. Software Efficiency and Maintainability
At present the software efficiency is at a reasonable state for being handled by a single person.  Using a Hashtable to hold the packages and their data with an O(1) lookup and access time is great.  Also our second primary data structure for comparisons is the 2d Distance matrix.  The code accesses indices directly giving this a 0(1) lookup as well.  Using these two data structures we create our list of packages to pass to the trucks for sorting. 
There are still some sections of my code that are repeated.  Meaning I can still do some refactoring or breaking down of code into further functions.  Still a skill I am in need of developing further.  Also had variable naming issues as my brain was used to camelCase.  I think I have found and refactored most to snake_case.
B6. Self-Adjusting Data Structures
As per the instructions I went with a rather simple hashtable.  The table would take the total size of packages read from whatever csv is being used and set the buckets to that size.  Since the environment was so controlled and I could guarantee that there would be no collisions, I made the decision to omit collision handling code such as linear/quadratic probing or chaining.  So bucket # = len(packages) so each package id should map directly to an address in memory.  Using this package Id in a HashTable.get(id) returns the rest of the package object.
Because of the omission of collision handling in any means, I do not know if this data structure qualifies as self-adjusting without this feature.  The total # of buckets is variable and based on the number of objects coming in from the csv.  Also in reviewing my code I noticed that my load factor for this hashtable is 1.0 or .9, if my understanding is correct.  Perhaps in the future the size or number of buckets would be increased.  In this scenario that is not necessary given the size of n is so small.  Also if collision handling is required in my data structure I would probably implement chaining.  This would entail turning each “bucket” into the head of a linked list.  If any key hashes to the same value the head would just add an address it is pointing to.  The .get() for this would follow the key to the start of the “bucket” and head down the linked list checking the key at each address to see if key == getKey exactly and return the value at that address.
D1. Data Structures and Their Explanations
HashTable:
	the original data structure used to store the package(id as key, rest as k/v pairs in an object)  the most important value stored here is the “Address”.  I used the “Address” value as a map to my 2d distance matrix. 
Address_Map:
	HashMap that hashes the string “Address” and returns the corresponding Address’ index in the distance matrix
Matrix:
	Represents the excel distance table provided.  each index corresponds to an address of a package.  This allows me to take access a package by key in my HashTable O(1) lookup.  Then access it’s “Address” value O(1) and input that in to my Address_Map returning the integer index of that package’s address in the 2d distance matrix. 
List:
	Used to create the routes the truck drivers will go on.  The lists are just the package number(so package data can be retrieved from hashtable) and the distance from the last package in the route that was delivered.  This can then be used to determine the times that each package will get delivered by using the avg speed traveled to calculate how long it would take the truck to drive his route given a starting time.



G1. First Status Check
 
G2. Second Status Check
 







G3. Third Status Check
 
H. Screenshots of Code Execution
 
I1. Strengths of Chosen Algorithm
The nearest neighbor algorithm is extremely simple in theory and implementation.  This vastly increases the maintainability of the code.  Anyone else who comes to work on this code base will within a few minutes be able to comprehend exactly what this algorithm is doing and therefore be able to make easy adjustments.  
I2. Verification of Algorithm
The nearest neighbor algorithm is probably one of the simplest solutions that could be used for this scenario.  The logic is extremely easy to understand(what address is closest to my current address) which makes maintainability for it very high.  I must admit that it is not very scalable though.   While the constraints of this particular problem limit the amount of packages that need to be sorted at once to around 16.  In the real world this would not be the case.  Also sorting would ideally happen before the packages are on the trucks.  For this specific problem attaining under 140 miles did not require much optimization. The first iteration of my solution placed the preset packages where they need to be.  Then I added packages from the remaining group into truck1, 2, 3 until they were full or there were no remaining packages.  I am pointing out that there was no optimization done at this step and package to truck association is completely random beyond presets.  Even with this simply looking for the shortest route on each truck got the total miles to around 120.  So almost the most costly version this algorithm could spit out given preset parameters.  Still with all that the algorithm met the mile requirements.  I will admit that the referenced version of my program did not deliver the required packages before their deadline in the morning.  But by simply adding a same_address() function to my truck_loader I dropped the total miles from 120 to 88.2 and delivered the deadline packages on time.  This with truck 1 starting immediately at 8:00 am and getting all deadline packages done on time and with truck 3 starting at the last delayed packages’ arrival at 9:05 with the packages that need to be delivered before 10:30 making it on time as well.  Truck 3’s driver then must return to the hub to swap to truck 2 to deliver the remaining packages.  Driver one on truck one after route completion and with the truck still in the field, drove 26.6 miles and finished its final delivery of package 39 at 9:36 am.  Driver 2 finished their final delivery of package 35 on truck 3 at 9:56 am.   They then returned to the hub to switch to truck 2.  Driver 2 finished his second route with a days total of  61.6 miles, finishing the day at 12:30 delivering package 22 and leaving the truck in the field.  
I3. Other possible Algorithms
Another approach could be to use brute force.  Given that the trucks are loaded in the same fashion as I have in my code, the max size of n that would be passed to the brute force algorithm would be 16.  Since we keep the size to 16 for each run this limits the runtime complexity to (16!).  Admittedly this is not amazing and some steps can be taken to lessen the runtime complexity.  One idea that comes to mind is keeping a running minimum and use that as a disqualifier.  Instead of building every possible combination, we could keep track of a minimum distance(set to infinity then set to the first completed route’s distance) and while building another route if ever the route exceeds the current minimum we would exit this and go to the next iteration of the outer loop.  This approach quickly stretches the limits of feasibility if the size of n increases at all. 
After further inspection of the data in the distance table I also think a version of Dijkstra’s algorithm would work well for this scenario.  The distances in the table seem to not represent what the shortest path between the two addresses are.  Some distances between a combination of addresses < point to point distance.  One would assume this is not the case but some weight may be applied to the distances.  given this information though, a simple check to see if the addition in between two points lessens the distance to the target address.  This can then be used, perhaps, in the truck loading logic.  Using this on the packages that are preset onto the trucks to determine potential packages or “addresses” to add between the preset points would greatly decrease distance traveled.   If Dijkstra’s algorithm is used and run on the preset packages on each truck, it is most likely possible to create a truck delivery route that is a sequence of optimized smaller routes determined when loading them on to the truck or before.  This would circumvent the need for the nearest neighbor algorithm being run on the packages once loaded on to the trucks, since the packages are loaded on to the trucks as a series of routes starting at the hub and ending at the last package on the truck.  In conclusion, I believe that running Dijkstra’s algorithm on a truck with preset packages already determined and after running same_address() on the presets would result in a sub 100 mile total for the given scenario.  Since this scenario is by package and not address, a call to same_address() would most likely be called when a new package(well address) is added to a route. I would like to point out that Dijkstra’s algorithm is not a direct solution to any variation of the Traveling Salesman Problem, and is usually used as a way to make other solutions more efficient.  Also given the nature of Dijkstra’s algorithm, some custom logic may be needed for its application to this specific problem.  Dijkstra’s algorithm cares only about the shortest path from point a to point b, but we may be able to add a weight to routes.  So instead of aiming for minimum distance we can aim for a ratio of distance to addresses visited.  This will hopefully help populate our routes with a few more addresses visited per short route.

J. Different Approach
If I were to start fresh on this project today my first step would be to strictly define the way in which I intake data.  Splitting the special instructions column into a few specific columns that adhere to very strict rules.  This would allow for simpler data intake with less custom logic.  Beyond that, I would like to try and create my own custom greedy algorithm.  I would either use a system that includes a proximity value for each address(this would allow me to prioritize outliers if I am near them) or add weight to each address.  The latter method would track the global state of by using a distance/address ratio.  When thinking on the second method I keep running into the thought that total distance accounts for this inherently regardless. 
K1. Data Structure
The hashtable meets all requirements for the given scenario.  The lookup time no matter the length of packages stored should be O(1).  If the number of packages increases the algorithm in use would encounter issues far before the HashTable would.  If the packages are increased to extreme lengths obviously some issues might arise.  Most scenarios should be overcome with simple chaining to circumvent collisions or if the set becomes large enough an implementation of quadratic probing could be in order.
Truck 1 - 26.6 miles
Truck 2 - 36.5 miles
Truck 3 - 22.7 miles
Total miles - 88.19 miles

K1A. Efficiency
As mentioned above, an increase in packages should still result in a HashTable lookup time of O(1).  
K1B. Overhead
If the number of packages increases so does the space used to store that data.  To my knowledge the space taken to store the packages would be in a 1 to 1 ratio.  Every package would be stored at its own address regardless of HashTable implementation. What I mean by this is that HashTables seem to be implemented in one of two ways.  The first being depth, each bucket mapping to a linked list head, in order to avoid potential collisions.  The other implementation involves increasing the number of buckets to avoid collisions, I mentally view this as width or horizontal growth as opposed to the chaining’s “depth”.  In both of these scenarios at a minimum every package maps to one address.  
K1C. Implications
The impact of changing the number of trucks or the number of cities on our data structure should be minimal.  If we are talking about their impact on the storage of packages in my HashTable then they are next to none.  The overall impact on the program could be quite severe though.  More cities would equate to more distance tables with addresses being stored in memory.  This also means that our sorting algorithm would need to be run more often.  Increasing the number of trucks implies an increase in packages.  The trucks only become relevant if there too are packages to fill them all.  With my program’s current build, trucks end up being stored as a list of package_id, distance values in order that they will be delivered.  I suppose I could add some fields in the hashtable to include what truck the package is on and when it should be delivered.  This would eliminate the need to hold on to the list of package_id, distance once the theoretical delivery time has been calculated.  
K2 Data Structure Comparison
Another data structure that could be used is an array. In the controlled scenario of this project, an array could perform comparably to a hash table. Like a hash table, an array offers O(1) access time, assuming that package IDs map directly to array indices. This makes it a viable choice for package data storage and address lookup in our program. Coupled with a list or priority queue to track the current route or for route building, an array could easily meet the requirements of this scenario.

However, the array falls short in a real-world context for several reasons. One major issue arises when dealing with non-sequential package identification numbers. This would necessitate the creation of an O(n) lookup function to iterate through array indices, negating the benefit of O(1) access time. In contrast, a hash table remains effective as it is not dependent on the order or sequential nature of keys.
Another disadvantage of using an array emerges when adding new packages after the initial creation of the array. This would require creating a new array to accommodate the additional packages, which is computationally expensive. A hash table, on the other hand, can handle this scenario more gracefully. Although my implementation does not allow for dynamic resizing of buckets (a problem that can be easily fixed), the impact on performance would be much less than that of an array.
Another alternative to a hash table is a list. Generally, using a list for this application would not be ideal, primarily due to its O(n) time complexity for lookups. However, there are specific contexts where a list could be justified.
In our controlled scenario, where the data set is finite and well-defined, a list could be acceptable if we're willing to sacrifice computational efficiency for simplicity. Using a list for data storage is straightforward and could be more intuitive for someone reading the code, thereby improving ease of use. Probably the biggest downside is the time complexity for get(item) operations, which is O(n). However, this issue could be mitigated to some extent by redesigning parts of the program. For example, we could save routes with both an address and a package_id. Doing so would allow us to access the address_map directly, bypassing the need to perform an O(n) lookup on our list to retrieve the address.
While this doesn't bring the time complexity down to O(1) like in a hash table or an array, it does reduce the number of O(n) operations required, making the list more efficient than it would be otherwise. Nevertheless, in a dynamic, real-world environment where the size and complexity of the data set are not as predictable, a hash table would be a far more suitable choice.
In short, arrays offer O(1) lookup times but are inflexible when it comes to resizing or handling non-sequential IDs. Lists, on the other hand, offer more flexibility in terms of adding or removing elements, but their O(n) lookup time is a significant drawback.


McDowell, G. L. (2015). Cracking the Coding Interview, 6th Edition. CareerCup.
Lysecky, R., & Vahid, F. (2018, June). C950: Data Structures and Algorithms II. zyBooks.
https://learn.zybooks.com/zybook/WGUC950AY20182019/


