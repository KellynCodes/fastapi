import bcrypt

class Bcrypt():
    def hash(self, str: str) -> str:
        """Hash the string using bcrypt."""
        if len(str.encode("utf-8")) > 72:
            raise ValueError("Password too long for bcrypt (max 72 bytes)")
        salt: bytes = bcrypt.gensalt()
        hashed = bcrypt.hashpw(str.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify(self, str: str, hashed: str) -> bool:
        """Verify the string against a bcrypt hash."""
        return bcrypt.checkpw(str.encode("utf-8"), hashed.encode("utf-8"))
