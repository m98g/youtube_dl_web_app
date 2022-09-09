from typing import List
from typing import Optional

from fastapi import Request

class downloadform:
    def __init__(self, request:Request):
        self.request: Request = request
        self.errors: List = []
        self.url: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.url = form.get("Url")

    def is_valid(self):
        if not self.url and (self.url.__contains__("Url")):
            self.errors.append("Not a youtube url.")