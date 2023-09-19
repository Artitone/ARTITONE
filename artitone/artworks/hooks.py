# from paypal.standard.models import ST_PP_COMPLETED
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.ipn.signals import valid_ipn_received


@csrf_exempt
@receiver(valid_ipn_received)
def webhook(sender, **kwargs):
    # ipn_obj = sender
    print("this is hook")
    return
