


from django import template
import math

register = template.Library()

# Tag to calculate the selling price based on price and discount
@register.simple_tag
def cal_sellprice(price, discount):
    try:
        # Convert price and discount to float to avoid the multiplication error
        price = float(price)
        discount = float(discount)
    except (ValueError, TypeError):
        # In case of an invalid value, return the original price
        return price

    # If discount is None or 0, return the original price
    if discount == 0:
        return price

    # Calculate the discounted price
    sellprice = price - (price * discount * 0.01)

    # Return the floor value of the selling price
    return math.floor(sellprice)

# Filter to format the price in rupees
@register.filter
def rupee(price):
    try:
        # Convert price to float and format it with ₹ symbol and two decimal places
        price = float(price)
    except (ValueError, TypeError):
        return price  # Return the original price if conversion fails
    
    return f'₹{price:.2f}'
