from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        from_attributes=True
    )

