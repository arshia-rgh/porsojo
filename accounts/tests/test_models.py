import pytest
from accounts.models.otp_token import OtpToken
from accounts.models.user import User
from django.utils import timezone


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
    def test_create_new_code(self):
        token = OtpToken.objects.create(phone_number="09121101111", code=OtpToken.generate_code())
        assert OtpToken.objects.all().count() == 1

    def test_retrieve_token_by_phone_number(self):
        token = OtpToken.objects.create(phone_number="09121101111", code=OtpToken.generate_code())
        retrieved_token = OtpToken.objects.get(phone_number="09121101111")
        assert retrieved_token.code == token.code

    def test_update_token(self):
        token = OtpToken.objects.create(phone_number="09121101111", code=OtpToken.generate_code())
        new_code = OtpToken.generate_code()
        token.code = new_code
        token.save()
        updated_token = OtpToken.objects.get(phone_number="09121101111")
        assert updated_token.code == new_code

    def test_delete_token(self):
        token = OtpToken.objects.create(phone_number="09121101111", code=OtpToken.generate_code())
        token_id = token.id
        token.delete()
        with pytest.raises(OtpToken.DoesNotExist):
            OtpToken.objects.get(id=token_id)

    def test_token_expiry(self):
        ten_minutes_before = timezone.now() - timezone.timedelta(minutes=10)
        token = OtpToken.objects.create(phone_number="09121101111", code=OtpToken.generate_code())

        token.created = ten_minutes_before
        token.save()
        assert token.is_expire == True
