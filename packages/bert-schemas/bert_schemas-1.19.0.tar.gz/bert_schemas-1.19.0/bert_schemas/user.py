# type: ignore
from datetime import datetime
from typing import List, Optional, Type

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel, EmailStr, constr, HttpUrl

from .questionnaire import RegistrationQandA

external_user_id: Type[str] = constr(regex=r"^auth0|[a-z0-9]{24}$")


class RoleName(StrEnum):
    SUPERUSER = "SUPERUSER"
    ORG_ADMIN = "ORG_ADMIN"

    def __str__(self):
        return str(self.value)


class PurchaseEntity(StrEnum):
    USER = "USER"
    PAID = "PAID"
    ORG = "ORG"


class JobLimitType(StrEnum):
    JOB_RATE = "JOB_RATE"
    JOB_QUOTA = "JOB_QUOTA"


class ExternalUserId(BaseModel):
    external_user_id: external_user_id


class RoleBase(BaseModel):
    name: RoleName
    description: Optional[str]

    class Config:
        orm_mode = True


class Role(RoleBase):
    pass


class Organization(BaseModel):
    name: str
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    affiliation: str

    class Config:
        orm_mode = True
        extra = "forbid"


class OrganizationUser(UserBase):
    external_user_id: external_user_id
    jobs_run_today: int


class EmailPreference(BaseModel):
    jobs: bool
    general: bool

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    email_preferences: Optional[EmailPreference]


class UserResponse(UserBase):
    signup_date: datetime
    external_user_id: external_user_id
    roles: Optional[List[Role]]
    organization: Optional[Organization]
    active: bool
    email_preferences: EmailPreference


class UserSearchResponse(UserBase):
    external_user_id: str
    organization: Optional[Organization]


class User(UserBase):
    id: int
    external_user_id: external_user_id
    signup_date: datetime
    roles: Optional[List[Role]]
    organization: Optional[Organization]


class UserCreate(UserBase):
    external_user_id: external_user_id


class UserSignUp(UserBase):
    questionnaire: RegistrationQandA
    response: Optional[str]

    class Config:
        use_enum_values = True


class JobLimit(BaseModel):
    daily_limit: int
    daily_used: int
    daily_remaining: int
    purchased: Optional[int]
    purchased_remaining: Optional[int]


class JobPurchase(BaseModel):
    purchase_date: datetime
    quantity: int

    class Config:
        orm_mode = True


class UserJobPurchase(JobPurchase):
    user_id: int


class OrgJobPurchase(JobPurchase):
    org_id: int


class PurchasePriceData(BaseModel):
    currency: str
    product_data: dict
    unit_amount: int


class PurchaseLineItem(BaseModel):
    amount: int | None
    currency: str | None
    description: str | None
    price: str
    quantity: int
    price_data: PurchasePriceData | None


class CheckoutSessionResponse(BaseModel):
    session_url: HttpUrl


class ContactUs(BaseModel):
    subject: str
    email: EmailStr
    content: constr(min_length=1, max_length=500)
