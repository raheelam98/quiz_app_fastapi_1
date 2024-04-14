
# custom exception class for invalid input scenarios
class InvalidInputException(Exception):
    def __init__(self, args : object) -> None:
        self.invalid_input = args

# custom exception class for not found scenarios
class NotFoundException(Exception):
    def __init__(self, args: object) -> None:
        self.not_found = args        

# custom exception class for not found scenarios
class ConflictException(Exception):
    def __init__(self, args : object) -> None:
        self.conflict_input = args             


### https://fastapi.tiangolo.com/tutorial/handling-errors/