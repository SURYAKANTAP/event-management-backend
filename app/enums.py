import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    normal = "normal"