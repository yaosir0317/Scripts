from abc import ABC
from typing import Union, TypeVar, Generic, Sequence

import uvicorn
from pydantic import BaseModel, Field
from fastapi import Depends, FastAPI, Query, Form, UploadFile
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from pydantic.generics import GenericModel

T = TypeVar("T")


class MyParams(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    per_page: int = Query(50, ge=1, le=100, description="Size per page")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.per_page,
            offset=self.per_page * (self.page - 1),
        )


class MyPageContent(GenericModel, Generic[T], ABC):
    total: int
    items: Sequence[T]
    page: int
    per_page: int


class MyPage(AbstractPage[T], Generic[T]):
    code: int = 0
    message: str = "Success"
    data: MyPageContent[T]

    __params_type__ = MyParams  # Set params related to Page

    @classmethod
    def create(
            cls,
            items: Sequence[T],
            total: int,
            params: MyParams,
    ) -> AbstractPage:
        return cls(data=MyPageContent(
            total=total,
            items=items,
            page=params.page,
            per_page=params.per_page
        ))


async def d_a():
    yield "a"
    print("a")


async def d_b(_=Depends(d_a)):
    yield "b"
    print("b")


async def d_c(_=Depends(d_b)):
    yield "c"
    print("c")


# api_router = APIRouter(prefix="/api")
app = FastAPI()
# app.include_router(api_router)


class Item(BaseModel):
    name: str = Query(default="a", title="姓名", description="用户姓名")
    age: int = Field(default=10, title="age", description="年龄")


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/", response_model=MyPage[Item])
async def read_items(a: str = "a"):
    return paginate([Item(name=a)])


@app.get("/users/", response_model=Page[Item])
async def read_users(
    item: str = Query(default="a", title="姓名", description="用户姓名"),
    c: dict = Depends(common_parameters)
):
    print(c)
    i = Item(name=item, age=18)
    return paginate([i])


class CommonParam:
    def __init__(self, offset: int = 0, limit: int = 100):
        self.offset = offset
        self.limit = limit


@app.get("/common/")
async def read_common(obj: CommonParam = Depends(CommonParam), _=Depends(d_c)):
    print(obj)
    return obj.offset


class ItemForm(BaseModel):
    name: str = Form(title="姓名", description="用户姓名")
    age: int = Form(title="age", description="年龄")


@app.post("/form/")
async def read_form(a: UploadFile):
    print(a.filename)
    print(await a.read())
    return "123"


add_pagination(app)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8008)
