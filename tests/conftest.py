import pytest
from app import db
 
@pytest.fixture(scope="function", autouse=True)
def my_own_function_run_at_beginning(request):
    db.create_all()
 
    def my_own_function_run_at_end():
            db.drop_all()
    request.addfinalizer(my_own_function_run_at_end)