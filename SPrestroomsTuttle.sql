DROP TABLE IF EXISTS restrooms, cities, states;--Dropping any tables that may already exist in order to create tables in a new DBO
	
	--parent table to cities
	CREATE TABLE states (
	sid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	state VARCHAR(1000)
	);
	
	--parent table to restrooms
	CREATE TABLE cities (
	cid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	cityname VARCHAR(1000) NOT NULL,
	sid INT REFERENCES states (sid) ON DELETE CASCADE --foreign key that refers to states table
	);
	
	--child table, decomposed into two breakout tables because cities and states repeated themselves
	CREATE TABLE restrooms (
	rid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(1000) NOT NULL,
	accessible boolean, --does not need to be decomposed as there are only Y/N options
	unisex boolean,--does not need to be decomposed since there are only Y/N options
	cid INT REFERENCES cities (cid) ON DELETE CASCADE --foreign key that refers to cities table
	);


	--making a stored procedure to add multiple entries from a csv in one fell swoop when called
	DROP PROCEDURE IF EXISTS addrestroom;
	CREATE PROCEDURE addrestroom(
		pName VARCHAR(1000), --parameter for name/venue of restrooms
		pCity VARCHAR(1000), --parameter for city
		pState VARCHAR(1000), --parameter for state
		pAccessible BOOLEAN, --parameter for whether a restroom is accessible or not with TRUE representing accessible and FALSE representing not accessible
		pUnisex BOOLEAN--parameter for whether a restroom is accessible or not with TRUE representing unisex and FALSE representing not unisex
		
	)
	AS $$
	DECLARE sidout INT;
	DECLARE cidout INT;
	

	BEGIN
	IF (SELECT COUNT(*) FROM states WHERE state=pState)=1 THEN
			SELECT sid INTO sidout FROM states WHERE state=pState;
		ELSE
			INSERT INTO states(state) VALUES (pState);
			SELECT LASTVAL() INTO sidout;
		END IF;
	IF (SELECT COUNT(*) FROM cities WHERE cityname=pCity)=1 THEN
			SELECT cid INTO cidout FROM cities WHERE cityname=pCity; 
		ELSE
			INSERT INTO cities(cityname, sid) VALUES (pCity, sidout);
			SELECT LASTVAL() INTO cidout;
		END IF;
	--arguments that would be passed into the parameters
	INSERT INTO restrooms
	(name, accessible, unisex, cid) 
	VALUES 
	(pName, pAccessible, pUnisex, cidout);

	--COMMIT; --Don't use here, use in python
	END; $$
	language plpgsql;


--making calls to test whether the SP works

call addrestroom('Theater', 'Pittsburgh', 'Pennsylvania', TRUE, FALSE);
call addrestroom('Zoo', 'Pittsburgh', 'Pennsylvania', FALSE, FALSE);

call addrestroom('Other Theater', 'Washington', 'District of Columbia', FALSE, FALSE);
call addrestroom('Yet Another Theater', 'New York', 'New York', FALSE, TRUE);
call addrestroom('Even One More Theater', 'Pittsburgh', 'Pennsylvania', TRUE, FALSE);
call addrestroom('More Theater!', 'Omaha', 'Nebraska', FALSE, FALSE);

--SELECT COUNT(accessible) FROM restrooms WHERE accessible=TRUE;
--SELECT * FROM cities;
--SELECT * FROM states;
--SELECT restrooms.rid, restrooms.name, cities.cityname, states.state, restrooms.accessible, restrooms.unisex FROM (cities INNER JOIN restrooms ON cities.cid=restrooms.cid) INNER JOIN states on cities.sid=states.sid;
--select cities.cityname, count(restrooms.name) as thecount from cities inner join restrooms on cities.cid = restrooms.cid group by cityname;
--testing our aggregate queries below, which will be utilized in a separate Python file with connectivity to this DB using psycopg library
select cities.cityname, count(restrooms.cid) as thecount from restrooms inner join cities on restrooms.cid=cities.cid group by cityname;
select accessible, cities.cityname,count(restrooms.accessible) as accessiblecount from restrooms inner join cities on restrooms.cid=cities.cid group by cityname, accessible;
select accessible, cities.cityname, count(restrooms.accessible) as accessiblecount from restrooms inner join cities on restrooms.cid=cities.cid where cityname='Pittsburgh' group by cityname, accessible;
