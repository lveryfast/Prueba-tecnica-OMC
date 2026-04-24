from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt

from app.domain.entities.user import User
from app.domain.interfaces.user_repository import UserRepositoryInterface
from app.infrastructure.database.models import UserModel


class UserRepository(UserRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        model = await self.get_by_email(email)
        if model and bcrypt.verify(password, model.password_hash):
            return self._to_entity(model)
        return None

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            nombre=model.nombre,
            rol=model.rol,
            is_active=model.is_active
        )