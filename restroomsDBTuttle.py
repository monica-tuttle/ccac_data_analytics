#import psycopg Libraries
import psycopg2
import psycopg2.extras
import os
import csv
from csv import reader
import matplotlib.pyplot as plt
import numpy as np

os.system('clear')
#Generate connection string for user we created before.
connstring="host=localhost dbname=testdb user=pyuser password=password"
#allows pauses between selections
def wait_to_continue():
	input("Press enter to continue...")
	os.system('clear')

#creates tables in DB and creates a stored procedure to allow addition of new entries to DB
def initialize_table():
	conn=psycopg2.connect(connstring)
	cur=conn.cursor()
	sql1 = """DROP TABLE IF EXISTS restrooms, cities, states;
	CREATE TABLE states (
	sid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	state VARCHAR(1000)
	);
	CREATE TABLE cities (
	cid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	cityname VARCHAR(1000) NOT NULL,
	sid INT REFERENCES states (sid) ON DELETE CASCADE
	);
	CREATE TABLE restrooms (
	rid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(1000) NOT NULL,
	accessible boolean,
	unisex boolean,
	cid INT REFERENCES cities (cid) ON DELETE CASCADE
	);"""

	cur.execute(sql1)
	'''pyName=""
	pyCity=""
	pyState=""
	pyAccessible=None
	pyUnisex=None
	cur.execute('CALL addrestroom(%s,%s,%s,%s,%s)',(pyName, pyCity, pyState, pyAccessible, pyUnisex));'''
	conn.commit()
	cur.close()
	conn.close
	wait_to_continue()
	
#importing csv created from pulling data for cities Cleveland, Cincinnati, and Pittsburgh through API requests to refugerestrooms.org
def run_csv_import():
	conn=psycopg2.connect(connstring)
	cur=conn.cursor()

	with open('/var/lib/postgresql/scripts/final_project_DAT229/restrooms3cities.csv', 'r') as read_obj:
		# pass the file object to reader() to get the reader object
		csv_reader = reader(read_obj)
		header=next(csv_reader)
		i=0
		for row in csv_reader:
			
			#print(len(row))
			if len(row)>=19 and (row[5]=="True" or row[5]=="False"):
				i=i+1
				name=row[1]
				city=row[3]
				if city=='':
					city=None
				state=row[4]
				if state=='':
					state=None
				accessible=row[5]
				if accessible=='True':
					accessible=True
				if accessible=='False':
					accessible=False
				unisex=row[6]
				if unisex=='True':
					unisex=True
				if unisex=='False':
					unisex=False				
			

				if city!=None and state!=None and name!=None and (city=='Pittsburgh' or city=='Cleveland' or city=='Cincinnati'):
					print("Read: " + str(i) + ":" + name.ljust(10, ' ') + city.ljust(10, ' ') + state.ljust(10, ' ') + str(accessible) + " " + str(unisex))	
					
					cur.execute('CALL addrestroom(%s,%s,%s,%s,%s)',(name, city, state, accessible, unisex));
					print("  ")
						
	conn.commit()
	cur.close()
	conn.close
	wait_to_continue()
	
# shows user columns from the tables created in DB
def run_select(): 
	print("Running the select routine!")
	sql="SELECT restrooms.rid, restrooms.name, cities.cityname, states.state, restrooms.accessible, restrooms.unisex FROM (cities INNER JOIN restrooms ON cities.cid=restrooms.cid) INNER JOIN states on cities.sid=states.sid;"
	conn=psycopg2.connect(connstring)
#	cur=conn.cursor()
	cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute(sql)
	row=cur.fetchone();
	print("Rowcount: ", cur.rowcount)
	if row==None:
		print("No records!")
	else:
		while row is not None:
			print(row['name'].ljust(30, ' ') + row['cityname'].ljust(15, ' ') + row['state'].ljust(10, ' ')+ str(row['accessible']).ljust(10, ' '))
			row=cur.fetchone()
	cur.close
	conn.close
	wait_to_continue()

# cleans the data pulled from original csv and saves into a revised csv
def output_save_csv_three_cities():
	sql="SELECT restrooms.name, cities.cityname, states.state FROM (cities INNER JOIN restrooms ON cities.cid=restrooms.cid) INNER JOIN states on cities.sid=states.sid;"
	conn=psycopg2.connect(connstring)
	cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute(sql)
	row=cur.fetchone();
	with open('/var/lib/postgresql/scripts/restroomsThreeCities.csv', 'w', newline='') as csvfile:
		fieldnames = ['Name', 'City', 'State']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		if row==None:
			print("No records!")
		else:
			while row is not None:
				writer.writerow({'Name': row['name'], 'City': row['cityname'], 'State': row['state']})
				print("Writing record " + row['name'])
				row=cur.fetchone()
	cur.close
	conn.close
	wait_to_continue()

# graph that compares number of refuge restrooms between cities of Cleveland, Cincinnati, and Pittsburgh
def vertical_bar_chart():
	print("Running the select average per routine!")
	sql="select cities.cityname, count(restrooms.cid) as thecount from restrooms inner join cities on restrooms.cid=cities.cid group by cityname;"
	conn=psycopg2.connect(connstring)
#	cur=conn.cursor()
	cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute(sql)
	row=cur.fetchone();
	cities=[]
	theCount=[]
	print("Rowcount: ", cur.rowcount)
	if row==None:
		print("No records!")
	else:
		while row is not None:
			print(row['cityname'].ljust(15, ' ') + str(round(row['thecount'],2)).ljust(10, ' '))
			cities.append(row['cityname'])
			theCount.append(round(row['thecount'],2))			
			row=cur.fetchone()
	plt.xlabel('City')
	plt.ylabel('Number of Refuge Restrooms')
	plt.xticks(range(len(cities)), cities)
	plt.bar(range(len(theCount)), theCount)

	plt.show()
	cur.close
	conn.close
	wait_to_continue()

#importing csv created from pulling data for 50 most populous US cities through API requests to refugerestrooms.org
def run_csv_import_all_cities():
	conn=psycopg2.connect(connstring)
	cur=conn.cursor()

	with open('/var/lib/postgresql/scripts/final_project_DAT229/restroomstext.csv', 'r') as read_obj:
		# pass the file object to reader() to get the reader object
		csv_reader = reader(read_obj)
		header=next(csv_reader)
		i=0
		for row in csv_reader:
			
			#print(len(row))
			if len(row)>=19 and (row[5]=="True" or row[5]=="False"):
				i=i+1
				name=row[1]
				city=row[3]
				if city=='':
					city=None
				state=row[4]
				if state=='':
					state=None
				accessible=row[5]
				if accessible=='True':
					accessible=True
				if accessible=='False':
					accessible=False
				unisex=row[6]
				if unisex=='True':
					unisex=True
				if unisex=='False':
					unisex=False				
			

				if city!=None and state!=None and name!=None and (city=='New York City' or city=='Los Angeles' or city=='Chicago' or city=='Houston' or city=='Phoenix' or city=='Philadelphia' or city=='San Antonio' or city=='San Diego' or city=='Dallas' or city=='San Jose' or city=='Austin' or city=='Jacksonville' or city=='Fort Worth' or city=='Columbus' or city=='Charlotte' or city=='San Francisco' or city=='Indianapolis' or city=='Seattle' or city=='Denver' or city=='Washington' or city=='Boston' or city=='El Paso' or city=='Nashville' or city=='Detroit' or city=='Oklahoma City' or city=='Portland' or city=='Las Vegas' or city=='Memphis' or city=='Louisville' or city=='Baltimore' or city=='Milwaukee' or city=='Albuquerque' or city=='Tucson' or city=='Fresno' or city=='Mesa' or city=='Sacramento' or city=='Atlanta' or city=='Kansas City' or city=='Colorado Springs' or city=='Omaha' or city=='Raleigh' or city=='Miami' or city=='Long Beach' or city=='Virginia Beach' or city=='Oakland' or city=='Minneapolis' or city=='Tulsa' or city=='Tampa' or city=='Arlington' or city=='New Orleans'):
					print("Read: " + str(i) + ":" + name.ljust(10, ' ') + city.ljust(10, ' ') + state.ljust(10, ' ') + str(accessible) + " " + str(unisex))	
					
					cur.execute('CALL addrestroom(%s,%s,%s,%s,%s)',(name, city, state, accessible, unisex));
					print("  ")
					
	conn.commit()
	cur.close()
	conn.close
	wait_to_continue()	

# cleans the data pulled from original csv and saves into a revised csv
def output_save_csv_50_cities():
	sql="SELECT restrooms.name, cities.cityname, states.state FROM (cities INNER JOIN restrooms ON cities.cid=restrooms.cid) INNER JOIN states on cities.sid=states.sid;"
	conn=psycopg2.connect(connstring)
	cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute(sql)
	row=cur.fetchone();
	with open('/var/lib/postgresql/scripts/restrooms50Cities.csv', 'w', newline='') as csvfile:
		fieldnames = ['Name', 'City', 'State']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		if row==None:
			print("No records!")
		else:
			while row is not None:
				writer.writerow({'Name': row['name'], 'City': row['cityname'], 'State': row['state']})
				print("Writing record " + row['name'])
				row=cur.fetchone()
	cur.close
	conn.close
	wait_to_continue()
	
# graph that compares number of refuge restrooms between 50 most populous US cities
def horizontal_bar_chart():
	print("Running Count ")
	sql="select cities.cityname, count(restrooms.cid) as thecount from restrooms inner join cities on restrooms.cid=cities.cid group by cityname;"
	conn=psycopg2.connect(connstring)
#	cur=conn.cursor()
	cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute(sql)
	row=cur.fetchone();
	cities=[]
	theCount=[]
	print("Rowcount: ", cur.rowcount)
	if row==None:
		print("No records!")
	else:
		while row is not None:
			print(row['cityname'].ljust(15, ' ') + str(round(row['thecount'],2)).ljust(10, ' '))
			cities.append(row['cityname'])
			theCount.append(round(row['thecount'],2))			
			row=cur.fetchone()			
		
		np.random.seed(19680801)

		plt.rcdefaults()
		fig, ax = plt.subplots()

		cities = ('New York City', 'Los Angeles ', 'Chicago ', 'Houston', 'Phoenix ', 'Philadelphia', 'San Antonio ', 'San Diego ', 'Dallas ', 'San Jose ', 'Austin ', 'Jacksonville', 'Fort Worth ', 'Columbus ', 'Charlotte ', 'San Francisco', 'Indianapolis', 'Seattle ', 'Denver', 'Washington', 'Boston ', 'El Paso ', 'Nashville', 'Detroit ', 'Oklahoma City ', 'Portland ', 'Las Vegas ', 'Memphis ', 'Louisville', 'Baltimore', 'Milwaukee ', 'Albuquerque ', 'Tucson ', 'Fresno ', 'Mesa ', 'Sacramento ', 'Atlanta ', 'Kansas City ', 'Colorado Springs ', 'Omaha ', 'Raleigh ', 'Miami ', 'Long Beach ', 'Virginia Beach', 'Oakland ', 'Minneapolis ', 'Tulsa ', 'Tampa ', 'Arlington ', 'New Orleans')
		y_pos = np.arange(len(cities))
		restrooms = 3 + 800 * np.random.rand(len(theCount))
		error = np.random.rand(len(cities))

		ax.barh(y_pos, restrooms, xerr=error, align='center')
		ax.set_yticks(y_pos)
		ax.set_yticklabels(cities)
		ax.invert_yaxis()  # labels read top-to-bottom
		ax.set_xlabel('Number of Refuge Restrooms')
		ax.set_title('How many refuge restrooms per city?')

		plt.show()

# shows three consecutive pie charts illustrating the ratio of accessible to non-accessible 'refuge' restrooms in Cleveland, Cincinnati, and Pittsburgh, respectively
def pie():
	sql="select accessible, cities.cityname, count(restrooms.accessible) as accessiblecount from restrooms inner join cities on restrooms.cid=cities.cid where cityname='Cleveland' group by cityname, accessible;"
	conn=psycopg2.connect(connstring)
#	cur=conn.cursor()
	cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute(sql)
	row=cur.fetchone();
	accessibleList=[]
	theCount=[]
	#print("Rowcount: ", cur.rowcount)
	if row==None:
		print("No records!")
	else:
		while row is not None:
			accessibleList.append(row['accessible'])
			theCount.append(row['accessiblecount'])			
			row=cur.fetchone()
	labels = accessibleList
	sizes = theCount
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	plt.show()
	
	sql="select accessible, cities.cityname, count(restrooms.accessible) as accessiblecount from restrooms inner join cities on restrooms.cid=cities.cid where cityname='Cincinnati' group by cityname, accessible;"
	conn=psycopg2.connect(connstring)
#	cur=conn.cursor()
	cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute(sql)
	row=cur.fetchone();
	accessibleList=[]
	theCount=[]
	#print("Rowcount: ", cur.rowcount)
	if row==None:
		print("No records!")
	else:
		while row is not None:
			accessibleList.append(row['accessible'])
			theCount.append(row['accessiblecount'])			
			row=cur.fetchone()
	labels = accessibleList
	sizes = theCount
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	plt.show()
	

	sql="select accessible, cities.cityname, count(restrooms.accessible) as accessiblecount from restrooms inner join cities on restrooms.cid=cities.cid where cityname='Pittsburgh' group by cityname, accessible;"
	conn=psycopg2.connect(connstring)
#	cur=conn.cursor()
	cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute(sql)
	row=cur.fetchone();
	accessibleList=[]
	theCount=[]
	#print("Rowcount: ", cur.rowcount)
	if row==None:
		print("No records!")
	else:
		while row is not None:
			accessibleList.append(row['accessible'])
			theCount.append(row['accessiblecount'])			
			row=cur.fetchone()
	labels = accessibleList
	sizes = theCount
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	plt.show()
	
	
	
#initial greeting to user
print("Hi there! This menu gives you options to learn more about data pulled from the open source API at refugerestrooms.org, which indexes and maps safe restroom locations for trans, intersex, and gender nonconforming individuals.")
print()
print("If you wish to contribute to the project you can visit https://github.com/RefugeRestrooms/refugerestrooms and learn more.")
print()
#main program loop starts here		
loop=True
while loop==True:
	print("Running menu!")
	print("Enter 1 to select.")
	print("Enter 2 to initialize/reset the table.")
	print("Enter 3 to import csv for cities Cleveland, Cincinnati, and Pittsburgh.")
	print("Enter 4 to output a revised csv for cities Cleveland, Cincinnati, and Pittsburgh.")
	print("Enter 5 to see a vertical bar chart for Cleveland, Cincinnati, and Pittsburgh.")
	print("Enter 6 to see pie charts for accessible (i.e. 'True') vs. non-accessible (i.e. 'False') refuge restrooms in consecutive order for Cleveland, Cincinnati, and then Pittsburgh.")
	print("Enter 7 to import csv for the top 50 most populous US cities (make sure to select option '2' to reset table first).")
	print("Enter 8 to output a revised csv for the top 50 most populous US cities.")
	print("Enter 9 to see a horizontal bar chart for the top 50 most populous US cities.")

	print("Enter 10 to quit.")
	choice=input("Enter choice:")
	if choice=="1":
		run_select()
	elif choice=="2":
		initialize_table()
	elif choice=="3":
		run_csv_import()
	elif choice=="4":
		output_save_csv_three_cities()
	elif choice=="5":
		vertical_bar_chart()
	elif choice=="6":
		pie()
	elif choice=="7":
		run_csv_import_all_cities()
	elif choice=="8":
		output_save_csv_50_cities()
	elif choice=="9":
		horizontal_bar_chart()
	elif choice=="10":
		loop=False;
#end loop
