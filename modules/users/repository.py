import uuid

from datetime import datetime

from sqlalchemy.orm import Session

from modules.users.models import (
    AuthUserModel
)


class UserRepository:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    def create_user(

        self,

        merchant_id: str,

        username: str,

        password_hash: str,

        role: str,

        branch_id: str | None = None

    ):

        user = AuthUserModel(

            user_id=str(
                uuid.uuid4()
            ),

            merchant_id=merchant_id,

            branch_id=branch_id,

            username=username.lower().strip(),

            password_hash=password_hash,

            role=role,

            active=True

        )

        self.db.add(
            user
        )

        self.db.commit()

        self.db.refresh(
            user
        )

        return user

    def get_by_username(

        self,

        merchant_id: str,

        username: str

    ):

        return (

            self.db.query(
                AuthUserModel
            )

            .filter(

                AuthUserModel.merchant_id
                == merchant_id,

                AuthUserModel.username
                == username.lower().strip()

            )

            .first()

        )

    def get_by_user_id(
        self,
        user_id: str
    ):

        return (

            self.db.query(
                AuthUserModel
            )

            .filter(
                AuthUserModel.user_id
                == user_id
            )

            .first()

        )

    def count_merchant_users(
        self,
        merchant_id: str
    ) -> int:

        return (

            self.db.query(
                AuthUserModel
            )

            .filter(
                AuthUserModel.merchant_id
                == merchant_id
            )

            .count()

        )

    def deactivate_user(
        self,
        user_id: str
    ):

        user = self.get_by_user_id(
            user_id
        )

        if not user:

            return None

        user.active = False

        user.updated_at = datetime.utcnow()

        self.db.commit()

        self.db.refresh(
            user
        )

        return user