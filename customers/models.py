from django.db import models
from django.core.exceptions import ValidationError
from utils.models import AbstractBaseModel
from utils.helpers import enforce_all_required_arguments_are_truthy
import uuid
from utils.validators import validate_international_phone_number



class CustomerManager(models.Manager):
    """
    Manager class for the Customer model.
    """
    def create_customer(self, **kwargs):
        """
        Method to actually create a customer. Ensure all arguments in `REQUIRED_ARGS` are provided.
        """
        REQUIRED_ARGS = (
           "name",
           "phone"
        )

        enforce_all_required_arguments_are_truthy(kwargs, REQUIRED_ARGS)

        customer = self.model(**kwargs)
        customer.clean()  # ensure the model is valid before saving
        customer.save()
        return customer
    

class Customer(AbstractBaseModel, models.Model):
    """
    Class for modelling Customer entities.
    """
    name = models.CharField(max_length=50)
    phone = models.CharField(unique=True, max_length=50)
    # Added this just so we can track the customer without using the auto-incrementing pk
    code = models.UUIDField(
        default=uuid.uuid4, blank=True, editable=False, unique=True, db_index=True
    )
    objects = CustomerManager()
    
    def __str__(self):
        return self.name
    
    
    def clean(self):
        """
        We ensure that the phone number is of the proper format before we save it.
        """

        phone = self.phone

        if not validate_international_phone_number(phone):
            raise ValidationError(
                {"phone": "Please enter a valid international phone number."}
            )
        return super().clean()


    




