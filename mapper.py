#!/usr/bin/python2.7

import psycopg2
import psycopg2.extras
import time
import datetime

def user_storage_grp_insert (user_id, storage_grp_id):
	
	try:
        	conn = psycopg2.connect("dbname='test' user='transuser' host='172.12.24.10' password='transcirrus1'")

	except:
        	print "Error!!! Cannot connect"

	
	try:
	
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		#query = "INSERT INTO user_cinder(user_id, cinder_id) VALUES ("
	
		ts = time.time()
	#	print ts
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	#	print st
	
		cur.execute("Insert INTO user_storage_grp(user_id, storage_grp_id, date_timestamp) VALUES(%s,%s, %s)",(user_id,storage_grp_id,st))
		conn.commit()

	except psycopg2.DatabaseError, e:
    
    		if conn:
        		conn.rollback()
    
    		print 'Error %s' % e

	finally:
    
    		if conn:
        		conn.close()
	
	return;

def storage_grp_cinder_insert (storage_grp_id, cinder_id):

        try:
                conn = psycopg2.connect("dbname='test' user='transuser' host='172.12.24.10' password='transcirrus1'")

        except:
                print "Error!!! Cannot connect"


        try:

                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                #query = "INSERT INTO user_cinder(user_id, cinder_id) VALUES ("

                ts = time.time()
         #       print ts
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
         #       print st

                cur.execute("Insert INTO storage_grp_cinder(storage_grp_id,cinder_id, date_timestamp) VALUES(%s,%s,%s)",(storage_grp_id,cinder_id,st))
                conn.commit()

        except psycopg2.DatabaseError, e:

                if conn:
                        conn.rollback()

                print 'Error %s' % e

        finally:

                if conn:
                        conn.close()

        return;

def user_cinder_fetch_user (cinder_id):

	myList=[]
        try:
                conn = psycopg2.connect("dbname='test' user='transuser' host='172.12.24.10' password='transcirrus1'")

        except:
                print "Error!!! Cannot connect"


	try:

		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                #query = "INSERT INTO user_cinder(user_id, cinder_id) VALUES ("

		cur.execute("Select distinct us.user_id from user_storage_grp us, storage_grp_cinder sg where us.storage_grp_id = sg.storage_grp_id and sg.cinder_id = %s",(cinder_id))

		rows = cur.fetchall()
		i=0;
		for row in rows:
			myList.append(row[0])
                	i=i+1
	
	except psycopg2.DatabaseError, e:

		if conn:
			conn.rollback()

		print 'Error %s' % e

	finally:

		if conn:
			conn.close()
        
	return myList;


def user_cinder_fetch_cinder (user_id):

	myList=[]
        try:
                conn = psycopg2.connect("dbname='test' user='transuser' host='172.12.24.10' password='transcirrus1'")

        except:
                print "Error!!! Cannot connect"


        try:

                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                #query = "INSERT INTO user_cinder(user_id, cinder_id) VALUES ("

                cur.execute("Select distinct sg.cinder_id from storage_grp_cinder sg, user_storage_grp us where us.storage_grp_id = sg.storage_grp_id and us.user_id = %s",(user_id))

                rows = cur.fetchall()

                for row in rows:
                        myList.append(row[0])

        except psycopg2.DatabaseError, e:


                if conn:
                        conn.rollback()

                print 'Error %s' % e

        finally:

                if conn:
                        conn.close()


        return myList;

print "Hello World"

#print user_storage_grp_insert('a',1)
#print user_storage_grp_insert('b',1)
#print user_storage_grp_insert('a',2)
#print storage_grp_cinder_insert(1,'c')
#print storage_grp_cinder_insert(1,'d')
#print storage_grp_cinder_insert(2,'e')
#print storage_grp_cinder_insert(2,'f')

arr = user_cinder_fetch_user('e')

for element in arr:
	print "User-",element

cinder = user_cinder_fetch_cinder('b')

for element in cinder:
	print "Cinder - ",element

ts = time.time()
#print ts
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#print st
#rows = cur.fetchall()

#print "\nShow me the databases:\n"
#for row in rows:
 #   print "   ", row[0]
