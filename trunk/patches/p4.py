# clear code cache
try:
	sql("delete from `__CodeFileTimeStamps`")
except Exception, e:
	pass