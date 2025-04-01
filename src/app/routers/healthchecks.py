from fastapi import APIRouter


router = APIRouter(
    tags=["healthcheck"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def execute_healthcheck():
    return {"message": "Contacts API is up and running."}
