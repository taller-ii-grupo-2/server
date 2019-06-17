from app.admins import Admin
from app.exceptions import NotAdminWeb
import pytest


def test_check_if_admin_incorrect():
	with pytest.raises(NotAdminWeb):
		Admin.check_if_admin('payas','payaslianadas')

def test_check_if_admin_correct():
	admin = Admin.check_if_admin('payas','payaslian')
	assert admin.name == 'payas'