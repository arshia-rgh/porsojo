import pytest
from accounts.models.user import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_new_user(self):
        user = User.objects.create_user(username="test", email="test@gmail.com", password="test pass")
        assert User.objects.all().count() == 1
        assert User.objects.get(email="test@gmail.com").is_email_verified == False

    def test_retrieve_user_by_username(self):
        user = User.objects.create_user(username="testuser", email="testuser@gmail.com", password="test pass")
        retrieved_user = User.objects.get(username="testuser")
        assert retrieved_user.email == "testuser@gmail.com"

    def test_user_password_is_hashed(self):
        user = User.objects.create_user(username="testuser", email="testuser@gmail.com", password="test pass")
        assert user.password != "test pass"
        assert user.check_password("test pass") == True

    def test_update_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@gmail.com", password="test pass")
        user.email = "newemail@gmail.com"
        user.save()
        updated_user = User.objects.get(username="testuser")
        assert updated_user.email == "newemail@gmail.com"

    def test_delete_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@gmail.com", password="test pass")
        user_id = user.id
        user.delete()
        with pytest.raises(User.DoesNotExist):
            User.objects.get(id=user_id)


@pytest.mark.django_db
class TestOTPToken:
    pass
