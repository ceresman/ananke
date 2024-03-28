
def client_init():
	global _global_manager_dict
	_global_manager_dict = {}

def client_set(key, value):
    _global_manager_dict[key] = value	

def client_get(key):
	return _global_manager_dict.get(key, None)