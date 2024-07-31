from django.core.validators import RegexValidator

iranian_phone_number_validator = RegexValidator(
    r"^(09|\+989)\d{9}$",
    "Invalid Iranian phone number.",
)
