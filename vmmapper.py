#!/usr/bin/python2.7

import psycopg2
import psycopg2.extras
import time
import datetime

class Mapper:

	@staticmethod
	def insert_user_storage_grp (user_id, storage_grp_id):
	
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

	@staticmethod
	def insert_storage_grp_cinder (storage_grp_id, cinder_id):

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

	@staticmethod
	def get_user_from_cinder (cinder_id):

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

	@staticmethod
	def get_cinder_from_user (user_id):

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

	@staticmethod
	def check_exist_user_cinder (user_id, cinder_id):
 	
		try:
                	conn = psycopg2.connect("dbname='test' user='transuser' host='172.12.24.10' password='transcirrus1'")

	        except:
        	        print "Error!!! Cannot connect"

	        try:

        	        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                	#query = "INSERT INTO user_cinder(user_id, cinder_id) VALUES ("

	                cur.execute("Select count(*) as cnt from storage_grp_cinder sg, user_storage_grp us where us.storage_grp_id = sg.storage_grp_id and us.user_id = %s and sg.cinder_id = %s",(user_id,cinder_id))

                	rows = cur.fetchall()

	                output = rows[0][0]
	#		print("op - ",output)

        	except psycopg2.DatabaseError, e:


                	if conn:
                        	conn.rollback()

	                print 'Error %s' % e

        	finally:

                	if conn:
                        	conn.close()

	        if output == 0L:
	#		print("Inside 0L");
			return bool(False);
		else:
	#		print("Inside 1L");
			return bool(True);
