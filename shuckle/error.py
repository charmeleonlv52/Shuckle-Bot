class ShuckleError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'Error: ' + self.message

class ShucklePermissionError(ShuckleError):
    def __init__(self):
        super().__init__('I don\'t have permission to do this.')

class ShuckleUserPermissionError(ShuckleError):
    def __init__(self):
        super().__init__('You don\'t have permission to use this command.')
