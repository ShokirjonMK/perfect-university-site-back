from celery import shared_task

import datetime
from pathlib import Path
from subprocess import PIPE, run

from django.conf import settings


def compress_video_file(video_path):
    """
    Compress video file to approximately 20 MB

    :param video_path: Path to video file
    :return: str of compressed video file relative path from MEDIA_ROOT
    """
    video_path = Path(video_path)

    # get video duration
    duration = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            video_path,
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    duration = float(duration.stdout.decode("utf-8").strip())

    # get file original size
    original_size = video_path.stat().st_size

    """
    1. Low-Quality Videos (240p to 480p):
        Original Size: 10 MB to 100 MB
        Compression: Reduce by 50% to 70%
        Target Size: 3 MB to 30 MB
    2. Medium-Quality Videos (480p to 720p):
        Original Size: 100 MB to 500 MB
        Compression: Reduce by 30% to 50%
        Target Size: 50 MB to 250 MB
    3. High-Quality Videos (1080p and above):
        Original Size: 500 MB to 2 GB
        Compression: Reduce by 20% to 40%
        Target Size: 300 MB to 1.2 GB
    """
    if original_size < 100 * 1024 * 1024:
        # low-quality videos
        target_size = original_size * 0.3
    elif original_size < 500 * 1024 * 1024:
        # medium-quality videos
        target_size = original_size * 0.4
    elif original_size < 2 * 1024 * 1024 * 1024:
        # high-quality videos
        target_size = original_size * 0.6
    else:
        # very high-quality videos
        target_size = original_size * 0.8

    print(f"Original size: {original_size}, Target size: {target_size}")

    # calculate target bitrate
    # target_bitrate = target_size(in bytes) * 8 / duration
    target_bitrate = int(target_size * 8 / duration)

    # get output file path, add random string to file name to avoid overwriting
    output_file = (
        f"{video_path.parent}/{video_path.stem}_{datetime.datetime.now().strftime('%Y%m%d%H%M')}_compressed.mp4"
    )

    run(["ffmpeg", "-i", video_path, "-b", str(target_bitrate), output_file])

    relative_path = output_file.replace(str(settings.MEDIA_ROOT), "")
    return relative_path


@shared_task
def compress_video_task(video_id):
    from admin_panel.model.activity import StudentVideo

    student_video = StudentVideo.objects.get(id=video_id)

    # if file extension is mp4 or mov
    if student_video.video and student_video.video.name.endswith((".mp4", ".mov")):
        # compress uploaded video file, and delete original file
        compressed_video_file = compress_video_file(student_video.video.path)
        # delete original video file
        student_video.video.delete(save=False)
        student_video.video = compressed_video_file
        student_video.save(update_fields=["video"])
