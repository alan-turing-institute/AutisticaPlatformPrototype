class Stepper:
    def __init__(self, stepper_data=None, request=None):
        self.stepper_data = stepper_data
        self.request = request

    def get_stepper_data(self):
        return self.stepper_data

    def update(self):
        print(self.request.method)
        if self.request.method == "POST":
            if self.request.POST.get('nextStep') == 'end':
                nextStep = self.request.POST.get('nextStep')
                self.request.session['activeStepper'] = nextStep
            else:
                nextStep = int(self.request.POST.get('nextStep'))
                self.request.session['activeStepper'] = nextStep
        elif self.request.method == "GET":
            self.request.session['activeStepper'] = 1
        else:
            print("error")