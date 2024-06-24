from django.core.exceptions import ValidationError
from phonenumbers import parse, is_valid_number
from phonenumbers.phonenumberutil import region_code_for_number


def validate_uzbekistan_number(value):
    from apps.forAUTH.models import User

    try:
        phone = parse(value, "UZ")
        if not is_valid_number(phone):
            raise ValidationError("The phone number entered is not valid.")
        if region_code_for_number(phone) != "UZ":
            raise ValidationError("The phone number must be a Uzbekistan number.")
        users = User.objects.filter(phone=value)
        if users.exists():
            raise ValidationError("The phone number is already registered.")
    except Exception as e:
        raise ValidationError("Invalid phone number format.")
