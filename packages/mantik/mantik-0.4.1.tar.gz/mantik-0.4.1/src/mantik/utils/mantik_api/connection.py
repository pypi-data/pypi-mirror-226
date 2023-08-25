import typing as t
import uuid

import pydantic


class Connection(pydantic.BaseModel):
    """
    Model for the Connection credentials delivered by Mantik API.

    Attributes
    ----------
    name: the name of the Connection
    username: the username of the Connection credentials
    password: the password of the Connection credentials
    """

    connection_id: uuid.UUID = pydantic.Field(..., alias="connectionId")
    user_id: uuid.UUID = pydantic.Field(..., alias="userId")
    connection_name: str = pydantic.Field(..., alias="connectionName")
    connection_provider: str = pydantic.Field(..., alias="connectionProvider")
    auth_method: str = pydantic.Field(..., alias="authMethod")
    login_name: t.Optional[str] = pydantic.Field(..., alias="loginName")
    password: t.Optional[str]
    token: t.Optional[str]
