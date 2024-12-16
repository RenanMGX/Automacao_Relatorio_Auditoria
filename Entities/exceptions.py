class LoginRequired(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class ElementNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NavNotStarted(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Alert(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)