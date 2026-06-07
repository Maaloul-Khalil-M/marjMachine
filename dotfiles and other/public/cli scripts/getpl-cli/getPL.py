import re
import typer
from pathlib import Path
from typing import Optional

# Initialize the Typer app
app = typer.Typer(help="getPL - Single M3U8 Playlist Generator")

def sanitize_name(name: str) -> str:
    """Removes illegal characters for Windows file/folder names."""
    if not name:
        return ""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def create_m3u8(playlist_path: Path, video_files: list):
    """Writes standard M3U8 formatting with absolute paths."""
    with open(playlist_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for video in video_files:
            f.write(f"#EXTINF:-1,{video.stem}\n")
            f.write(f"{video}\n")  # Absolute path
    typer.echo(f"  -> Created: {playlist_path.name} ({len(video_files)} videos)")

@app.command()
def generate_playlist(
    path: Path = typer.Argument(
        ".", 
        help="Target root folder path (e.g., the Course folder)"
    ),
    title: Optional[str] = typer.Option(
        None, 
        "--title", 
        "-t", 
        help="Custom title for the playlist file"
    ),
    sort: bool = typer.Option(
        False, 
        "--sort", 
        "-s", 
        help="Force alphabetical sorting of video files"
    )
):
    """Generates a single M3U8 playlist from a root folder and its 1st-level subdirectories."""
    source_dir = path.resolve()
    
    if not source_dir.is_dir():
        typer.secho(f"Error: Directory '{source_dir}' not found.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    # 1. Determine the playlist file name
    raw_title = title if title else source_dir.name
    safe_course_name = sanitize_name(raw_title)
    
    if not safe_course_name:
        safe_course_name = "Unnamed_Course"

    # 2. Define the target directory and file
    playlists_base_dir = Path(r"D:\playlists")
    playlists_base_dir.mkdir(parents=True, exist_ok=True) 
    
    playlist_path = playlists_base_dir / f"{safe_course_name}.m3u8"
    typer.echo(f"Generating single playlist: {playlist_path}\n")

    video_files = []
    
    # 3. Gather root folder videos first
    root_videos = source_dir.glob("*.mp4")
    if sort:
        video_files.extend(sorted(root_videos))
    else:
        video_files.extend(list(root_videos))

    # 4. Gather exactly ONE level deep (Folder level remains sorted)
    for child_dir in sorted(source_dir.iterdir()):
        if child_dir.is_dir():
            child_videos = child_dir.glob("*.mp4")
            if sort:
                video_files.extend(sorted(child_videos))
            else:
                video_files.extend(list(child_videos))

    # 5. Write the file if we found videos
    if video_files:
        create_m3u8(playlist_path, video_files)
        typer.secho(f"\nSuccess! Generated playlist with {len(video_files)} total video(s).", fg=typer.colors.GREEN)
    else:
        typer.echo("\nNo .mp4 files found in the root or first-level subdirectories.")

if __name__ == "__main__":
    app()