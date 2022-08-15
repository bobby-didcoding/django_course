from django import template
from django.template.loader import render_to_string
from ..models import Item
from ..utils import EcommerceManager
register = template.Library()


@register.simple_tag(takes_context=True)
def item_button(context, target):
    '''
    Handles the logic for a button used to add items to a users cart.
    '''
    user = context['request'].user
    ecommerce_manager = EcommerceManager(user = user)

    # do nothing when user isn't authenticated
    if not user.is_authenticated:
        return ''

    target_model = '.'.join((target._meta.app_label, target._meta.object_name))
    undo = False
    cart = ecommerce_manager.cart_object()
    item_field = cart.items
    if cart.item_check(target):
        undo = True

    qty = cart.qty_check(target)

    return render_to_string(
        'ecommerce/item_button.html', {
            'target_model': target_model,
            'object_id': target.id,
            'object_quantity': qty,
            'object_stock': target.stock,
            'undo': undo,
            'item_count': item_field.all().count()
        }
    )

@register.simple_tag(takes_context=True)
def item_button_v2(context, target):
    '''
    Handles the logic for a button used to remove items to a users cart.
    '''
    user = context['request'].user
    ecommerce_manager = EcommerceManager(user = user)

    # do nothing when user isn't authenticated
    if not user.is_authenticated:
        return ''

    target_model = '.'.join((target._meta.app_label, target._meta.object_name))

    undo = False
    # prepare button to remove item if
    # already in cart

    cart = ecommerce_manager.cart_object()
    item_field = cart.items
    if cart.item_check(target):
        undo = True
    qty = cart.qty_check(target)
    return render_to_string(
        'ecommerce/item_button_v2.html', {
            'target_model': target_model,
            'object_id': target.id,
            'object_quantity': qty,
            'object_stock': target.stock,
            'undo': undo,
            'item_count': item_field.all().count()
        }
    )
