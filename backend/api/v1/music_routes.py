# -*- coding: utf-8 -*-
from api.dependencies import music_service
from api.v1.base_crud_router import BaseCRUDRouter
from core.schemas import (
    MusicCreate,
    MusicDelete,
    MusicResponse,
    MusicResponseList,
    MusicUpdate,
)

router = BaseCRUDRouter[
    MusicCreate, MusicUpdate, MusicResponse, MusicResponseList, MusicDelete
](prefix="/Musics", tags=["Musics"], service_instance=music_service).router
