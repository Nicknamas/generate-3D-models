from dataclasses import asdict
from typing import Optional, List
from sqlalchemy.sql._typing import _ColumnExpressionArgument

from tree_ai.domains.credits.models import CreditsModel
from tree_ai.domains.credits.repository import CreditsRepository
from tree_ai.domains.credits.schemas import CreditsCreate, CreditsGet, CreditsTransactionResult

class CreditsService:
    def __init__(self, credits_repository: CreditsRepository):
        self.credits_repository = credits_repository

    def create(self, dto: CreditsCreate) -> CreditsGet:
        existing = self.credits_repository.get_by_user(dto.user_id)
        if existing:
            existing.amount = dto.amount
            self.credits_repository.update(existing)
            return CreditsGet.from_model(existing)

        data = asdict(dto)
        model = CreditsModel(**data)
        self.credits_repository.create(model)
        return CreditsGet.from_model(model)

    def add_credits(self, user_id: int, amount: int) -> CreditsTransactionResult:
        if amount <= 0:
            return CreditsTransactionResult(
                success=False,
                message="Amount must be positive",
                new_balance=0,
                transaction_type='add',
                amount=amount
            )

        credits = self.credits_repository.get_by_user(user_id)

        if not credits:
            credits = CreditsModel(user_id=user_id, amount=amount)
            self.credits_repository.create(credits)
        else:
            credits.amount += amount
            self.credits_repository.update(credits)

        return CreditsTransactionResult(
            success=True,
            message=f"Successfully added {amount} credits",
            new_balance=credits.amount or 0,
            transaction_type='add',
            amount=amount
        )

    def spend_credits(self, user_id: int, amount: int) -> CreditsTransactionResult:
        if amount <= 0:
            return CreditsTransactionResult(
                success=False,
                message="Amount must be positive",
                new_balance=0,
                transaction_type='spend',
                amount=amount
            )

        credits = self.credits_repository.get_by_user(user_id)

        if not credits:
            return CreditsTransactionResult(
                success=False,
                message="User has no credits",
                new_balance=0,
                transaction_type='spend',
                amount=amount
            )

        if credits.amount < amount:
            return CreditsTransactionResult(
                success=False,
                message=f"Insufficient credits. Available: {credits.amount}, Required: {amount}",
                new_balance=credits.amount,
                transaction_type='spend',
                amount=amount
            )

        credits.amount -= amount
        self.credits_repository.update(credits)

        return CreditsTransactionResult(
            success=True,
            message=f"Successfully spent {amount} credits",
            new_balance=credits.amount,
            transaction_type='spend',
            amount=amount
        )

    def get_list(self) -> List[CreditsGet]:
        credits_list = self.credits_repository.get_list()
        return [CreditsGet.from_model(c) for c in credits_list]

    def get_by_id(self, credits_id: int) -> Optional[CreditsGet]:
        credits = self.credits_repository.get_one(credits_id)
        return CreditsGet.from_model(credits) if credits else None

    def get_by_user(self, user_id: int) -> Optional[CreditsGet]:
        credits = self.credits_repository.get_by_user(user_id)
        return CreditsGet.from_model(credits) if credits else None

    def get_one_or_none(self, *filters: _ColumnExpressionArgument[bool]) -> Optional[CreditsGet]:
        credits = self.credits_repository.get_one_or_none(*filters)
        return CreditsGet.from_model(credits) if credits else None

    def get_balance(self, user_id: int) -> int:
        credits = self.credits_repository.get_by_user(user_id)
        return credits.amount if credits else 0

    def delete_by_id(self, credits_id: int) -> bool:
        return self.credits_repository.delete_by_id(credits_id)

    def delete_by_user(self, user_id: int) -> bool:
        return self.credits_repository.delete_by_user(user_id)
