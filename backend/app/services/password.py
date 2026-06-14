from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_password_hash(password: str) -> str:
    """Create password hash."""
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password by hash."""
    return password_context.verify(password, password_hash)