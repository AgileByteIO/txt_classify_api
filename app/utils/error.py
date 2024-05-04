class BusinessException(Exception):
    def __init__(self, code: int, message: str, cause: Exception | None):
        self.code = code
        self.message = message
        self.cause = cause

    def get_result(self) -> dict:

        match self.code:
            case 500:
                self.message = "Internal Server Error"
            case 502:
                self.message = "Subsystem Error"

        return {"code": self.code, "message": self.message}
