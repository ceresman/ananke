from ananke.base import BaseObject
import pytest
from ananke.llm.thudm import ZhiPu
from ananke.llm.azure import Azure
from ananke.llm.ernie import Ernie
__author__ = "OOXXXXOO"
__copyright__ = "OOXXXXOO"
__license__ = "MIT"


import re
import nltk
from nltk.sem import logic
from nltk.sem import Expression

logic._counter._value = 0
read_expr = Expression.fromstring


class Math(BaseObject):
    def __init__(self, **kwargs):
        super.__init__();
        pass

    def handle_math(self, user_input: str) -> str:
        pass


class Logic(BaseObject):
    def __init__(self, **kwargs):
        super.__init__()
        self.openai_model = Azure(chat_model_name="Ananke3-1106-US-WEST")
		# pass

    def handle_logic(self, user_input: str) -> str:
        input_text = user_input
        input_context = '''
        Now you are First-order and higher-order logic analysis assistant：
        The Definition of First-order & Higher-order
        First-order logic representation:
        Individuals: Represented by lowercase letters (e.g., x, y, z, etc.).
        Predicates: Represented by uppercase letters (e.g., P, Q, R, etc.).
        Quantifiers: Universal quantifier (∀) represents "for all," and existential quantifier (∃) represents "there exists."
        
        Higher-order logic representation:
        Predicates and relations: Represented by uppercase letters (e.g., P, Q, R, etc.).
        Quantifiers: Universal quantifier (∀) represents "for all," and existential quantifier (∃) represents "there exists."
        
        You need analysis given the text to output First-Order logic and higher-order expression formula.
        
        Here is example:
        Input_text:
        ```text
        everyone loves music.
        ```
        Output:
        1st-logic:
        ```
        ∀x (person(x) → love_music(x))
        ```
        higher-logic:
        ```
        ∀P (∀x (person(x) → P(x)))
        P:love_music
        ```
        Now I will provide you with the input text {} . Remember reply must as example format & style.
        '''.format(input_text)
        output = self.openai_model.chat(input_context)
        output_list = output.split('```')
        response = {output_list[0].strip('\n'):output_list[1].strip('\n'), 
             output_list[2].strip('\n'):output_list[3].strip('\n')}
        return response
		# pass


class Agent(BaseObject):
	def __init__(self, **kwargs):
		self.math = Math(**{})
		self.logic = Logic(**{})
		self.conversation_cache = None
		self.logger.info("agent init")

	def handle_conversation(self, conversation_id:str, user_input:str,):
        logic_parse = self.logic.handle_logic(user_input)
        return {'math': '', 'logic': logic_parse, 'doc_search': ''}

       # def _get_user_intent(self, user_input:str) -> int:
       #     pass
        
