from fastapi import HTTPException

user_not_found_exception = HTTPException(
    status_code=404,
    detail="User not found",
)

access_denied_exception = HTTPException(
    status_code=403,
    detail="Access denied",
)

transport_not_found_exception = HTTPException(
    status_code=404,
    detail="Transport not found",
)

rent_not_found_exception = HTTPException(
    status_code=404,
    detail="Rent not found",
)
