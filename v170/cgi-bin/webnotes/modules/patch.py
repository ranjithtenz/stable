# patch manager

def run():
	import webnotes
	from webnotes.utils import cint
	
	# get the folder find last patch
	next_patch = cint(webnotes.conn.get_global('next_patch'))
	
	patch_list = [next_patch]
	
	for patch in patch_list:
		patch_code = get_patch(patch)
		
		# patch found?
		if patch_code:
			webnotes.conn.begin()
		
			# execute
			execute_patch(patch_code, patch)
			
			# next
			patch_list.append(patch+1)
			webnotes.conn.set_global('next_patch', str(patch+1))
			
			# commit - each patch
			webnotes.conn.commit()
			
def get_patch(patch):
	import webnotes.defs, os
	
	try:
		file = open(os.path.join(webnotes.defs.modules_path, 'patches', 'p' + str(patch) + '.py'), 'r')
		code = file.read()
		file.close()
		return code
	except IOError, e:
		if e.args[0]==2:
			return None # no such patch
		else:
			raise e

def execute_patch(patch_code, patch):
	import webnotes.model.code
	
	webnotes.model.code.execute(patch_code)
	