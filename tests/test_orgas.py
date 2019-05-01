from app.users import User
from app.organizations import Organization
import pytest
from app import db
from app.exceptions import InvalidOrganizationName


def test_addorgas_too_long_name():
    db.create_all()

    org_name = "Rs4hi5zVr9TVHilIPTOCPPRqOvBIuPOnl"
    with pytest.raises(InvalidOrganizationName):
        Organization.add_orga(org_name,1)


def test_addorgas_correctly():
	org_name = "Exxon mobile"
	orga = Organization.add_orga(org_name,1)
	assert org_name == orga.org_name
