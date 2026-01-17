from app.repositories.base import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self, client):
        super().__init__(client, "users", User)

    def get_by_email(self, email: str) -> User | None:
        response = self.client.table(self.table)\
            .select("*")\
            .eq("email", email)\
            .execute()
        if not response.data:
            return None
        return self.model(**response.data[0])
