from dataclasses import dataclass
from typing import Optional
from tree_ai.domains.credits.models import CreditsModel


@dataclass
class CreditsCreate:
    user_id: int
    amount: int = 0

@dataclass
class CreditsGet:
    id: Optional[int]
    user_id: Optional[int]
    amount: Optional[int]

    @classmethod
    def from_model(cls, model: CreditsModel):
        return cls(
            id=model.id,
            user_id=model.user_id,
            amount=model.amount,
        )


@dataclass
class CreditsTransactionResult:
    success: bool
    message: str
    new_balance: int
    transaction_type: str
    amount: int
