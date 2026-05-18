from fastapi import APIRouter, status

from app.modules.auth.dependencies import CurrentActiveUserDep
from app.modules.rental.schemas import RentalCreate, RentalList, RentalResponse, RentalUpdate
from app.modules.rental.service import RentalServiceDep

router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.get("/")
def list_rentals(service: RentalServiceDep, current_user: CurrentActiveUserDep) -> RentalList:
    return service.list_all_rentals(current_user)


@router.get("/me")
def list_rentals_by_customer(
    service: RentalServiceDep,
    current_user: CurrentActiveUserDep,
) -> RentalList:
    return service.list_by_customer(current_user.id)


@router.get("/{rental_id}")
def get_rental_by_id(
    service: RentalServiceDep,
    current_user: CurrentActiveUserDep,
    rental_id: int,
) -> RentalResponse:
    return service.get_by_id(current_user, rental_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def register_rental(
    service: RentalServiceDep,
    current_user: CurrentActiveUserDep,
    request: RentalCreate,
) -> RentalResponse:
    return service.register(current_user, request)


@router.patch("/{rental_id}")
def update_rental(
    service: RentalServiceDep,
    current_user: CurrentActiveUserDep,
    rental_id: int,
    request: RentalUpdate,
) -> RentalResponse:
    return service.modify(current_user, rental_id, request)


@router.delete("/{rental_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rental(
    service: RentalServiceDep,
    current_user: CurrentActiveUserDep,
    rental_id: int,
) -> None:
    return service.remove(current_user, rental_id)
