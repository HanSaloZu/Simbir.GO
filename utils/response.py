from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

nonunique_username_response = JSONResponse(
    status_code=422,
    content=jsonable_encoder(
        [
            {
                "type": "nonunique",
                "loc": ["body", "username"],
                "msg": "Value already in use",
            }
        ]
    ),
)
