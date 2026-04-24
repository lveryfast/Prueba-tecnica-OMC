from app.domain.interfaces.user_repository import UserRepositoryInterface
from app.application.dtos.auth_dto import LoginDto


class AuthUseCases:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def login(self, dto: LoginDto):
        user = await self.user_repo.authenticate(dto.email, dto.password)
        if not user:
            raise ValueError("Credenciales inválidas")
        return user