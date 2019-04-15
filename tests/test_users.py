from app.users import User
from app.exceptions import InvalidMail
import unittest

class  AddUsersTest(unittest.TestCase):

	def test_addusers_incorrect(self):

		self.assertRaises(InvalidMail, User.add_user('agustin','agustin.payasliangmail.com')) 

