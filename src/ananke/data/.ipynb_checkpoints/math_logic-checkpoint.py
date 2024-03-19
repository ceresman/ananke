from ananke.base import BaseObject

class Math(BaseObject):
	def __init__(self, **kwargs):
		super.__init__();
		pass

	def handle_math(self, user_input: str) -> str:
		pass


class Logic(BaseObject):
	def __init__(self, **kwargs):
		super.__init__()
		pass

	def handle_logic(self, user_input: str) -> str:
		pass


class Agent(BaseObject):
	def __init__(self, **kwargs):
		self.math = Math(**kwargs)
		self.logic = Logic(**kwargs)
		self.conversation_cache = None
		self.logger.info("agent init")

	def handle_conversation(self, conversation_id:str, user_input:str,):
		pass


	def _get_user_intent(self, user_input:str) -> int:
		'''
		0 - math
		1 - logic
		2 - doc search
		'''

		pass