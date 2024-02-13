from django.db import models
from django.core.exceptions import ValidationError
from utils.models import AbstractBaseModel
from utils.helpers import enforce_all_required_arguments_are_truthy
from utils.validators import validate_international_phone_number
from customers.models import Customer


class OrderManager(models.Manager):
    """
    Manager class for the Order model.
    """
    def create_order(self, **kwargs):
        """
        Method to actually create an order. Ensure all arguments in `REQUIRED_ARGS` are provided.
        """
        REQUIRED_ARGS = (
           "item",
           "amount",
           "customer"
        )

        enforce_all_required_arguments_are_truthy(kwargs, REQUIRED_ARGS)

        order = self.model(**kwargs)
        order.save()
        return order
    

class Order(AbstractBaseModel, models.Model):
    """
    Class for modelling Order entities.
    """
    item = models.CharField(max_length=50)
    amount = models.DecimalField(
        max_digits=12, decimal_places=4
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    
    objects = OrderManager()
    
    def __str__(self):
        return self.item
    
    
    

    






