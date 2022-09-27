from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from pathlib import Path

def fetch_video_stream(id: str):
    vid_path = Path('./static/videos/{id}.mp4'.format(id=id))
    with open(vid_path.resolve(), "rb") as file:
        yield from file

router = APIRouter(prefix="/video")

@router.get("/{videoId}", response_class=StreamingResponse)
def get_video(videoId: str):
    return StreamingResponse(fetch_video_stream(videoId), media_type="video/mp4")