from django.template import Library
register = Library()

@register.inclusion_tag('../templates/userjourney.html')
def display_user_journey(activeStep, stepper_data):
    return {'activeStep': activeStep, 'stepper' : stepper_data}