import pytest
from accounts.models.user import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_new_user(self):
        user = User.objects.create_user(username="test", email="test@gmail.com", password="test pass")

        assert User.objects.all().count() == 1
