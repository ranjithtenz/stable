# archive.py
# - split tables horizontally for better performance
# - create union views

import webnotes

class Archiver:
	def __init__(self, dt):
		self.dt = dt
		self.arc_sql_ins = ("INSERT IGNORE INTO `arc%s` SELECT * FROM `tab%s` WHERE " %(self.dt,self.dt))
		self.arc_sql_del = ("DELETE FROM `tab%s` WHERE " %(self.dt))
		self.res_sql_ins = ("INSERT IGNORE INTO `tab%s` SELECT * FROM `arc%s` WHERE " %(self.dt,self.dt))
		self.res_sql_del = ("DELETE FROM `arc%s` WHERE " %(self.dt))
		self.child_doc_sql = ("INSERT")
		self.condition = ''
		
	def _sync_schema(self):
		# if not exists, create it
		if not ('arc'+self.dt) in [r[0] for r in webnotes.conn.sql("show tables")]:
			webnotes.conn.sql("create table `arc%s` like `tab%s`" % (self.dt, self.dt))
			webnotes.conn.sql("alter table `arc%s` ENGINE = MyISAM" % self.dt)
			# run update dt on the archive table
			# ??
	def condition_parse(self,filters):
		#filters: Filters is a dictionary with field:value. for range use a list for values. either {x:[val1,val2]} or {x:[[val1,val2][op1,op2]]} or {x:value}
		# self.condition at the moment only handling > and < by default.
		# the field datatype is as it is set by the values.Probably have to check from the tables.
		for each in filters:
			
			if self.condition:
				self.condition = self.condition + ' AND '
#			print filters,type(filters[each])
			if isinstance(filters[each],int):
				self.condition = self.condition + ('%s=%d' % (each,filters[each]))
			if isinstance(filters[each],str):
				self.condition = self.condition + ('%s=\'%s\'' % (each,filters[each]))
			if isinstance(filters[each],float):
				self.condition = self.condition + ('%s=%f' % (each,filters[each]))
				
			# Can't shake off the feeling there ought to be a cleaner/simpler way..
			#This is brute, gotta reuse some code from django(where.py,query.py)codebase.But that is too many classes.
			if isinstance(filters[each],list):
				assert type(filters[each][0]) == type(filters[each][1])
				assert len(filters[each]) == 2
				if isinstance(filters[each][0],list):
					assert type(filters[each][0][0]) == type(filters[each][0][1])
					assert len(filters[each][0]) == 2
					if isinstance(filters[each][0][0],str):
						print filters
						self.condition = self.condition + ('%s %s \'%s\'  AND ' % (each,filters[each][1][0],filters[each][0][0]))
						self.condition = self.condition + ('%s <  %s' % (each,filters[each][1][0],filters[each][0][1]))
					if isinstance(filters[each][0][0],int):
						print filters
						self.condition = self.condition + ('%s %s  %d AND ' % (each,filters[each][1][0],filters[each][0][0]))
						self.condition = self.condition + ('%s %s  %d' % (each,filters[each][1][1],filters[each][0][1]))
					if isinstance(filters[each][0][0],float):
						print filters
						self.condition = self.condition + ('%s %s  %f AND ' % (each,filters[each][1][0],filters[each][0][0]))
						self.condition = self.condition + ('%s %s  %f' % (each,filters[each][1][1],filters[each][0][1]))
					
					
				if isinstance(filters[each][0],str):
					self.condition = self.condition + ('%s >  %s  AND ' % (each,'%s'%(filters[each][0])))
					self.condition = self.condition + ('%s <  %s' % (each,'%s'%(filters[each][1])))
				if isinstance(filters[each][0],int):
					self.condition = self.condition + ('%s >  %d AND ' % (each,(filters[each][0])))
					self.condition = self.condition + ('%s <  %d' % (each,(filters[each][1])))
				if isinstance(filters[each][0],float):
					self.condition = self.condition + ('%s >  %f AND ' % (each,(filters[each][0])))
					self.condition = self.condition + ('%s <  %f' % (each,(filters[each][1])))
	
	def archive(self):
		# schema sync
		self._sync_schema()
		print self.condition
			
		self.arc_sql_ins = self.arc_sql_ins + self.condition
		self.arc_sql_del = self.arc_sql_del + self.condition
		
		print "Archive insert sql:",self.arc_sql_ins
		print "Archive del sql:",self.arc_sql_del
		webnotes.conn.sql(self.arc_sql_ins)
		webnotes.conn.sql(self.arc_sql_del)
		webnotes.conn.sql('commit')


	def restore(self):
		self._sync_schema()
		self.res_sql_ins = self.res_sql_ins + self.condition
		self.res_sql_del = self.res_sql_del + self.condition
		
		print "Restore insert sql:",self.res_sql_ins
		print "Restore del sql:",self.res_sql_del
		webnotes.conn.sql(self.res_sql_ins)
		webnotes.conn.sql(self.res_sql_del)
		webnotes.conn.sql('commit')
		
	def make_union_view(self):
		pass# archive.py
# - split tables horizontally for better performance
# - create union views

