import json
import subprocess
import typer
from pathlib import Path
from datetime import timedelta

# Initialize the Typer app
app = typer.Typer(help="lenvid - Calculate total duration of all MP4 files in a directory.")

def get_video_duration(file_path: Path) -> float | None:
    """Get video duration using ffprobe"""
    try:
        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'json',
                str(file_path)
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return float(data.get('format', {}).get('duration', 0))
        return 0
        
    except Exception:
        return None

@app.command()
def lenvid(
    path: Path = typer.Argument(
        ".", 
        help="Target directory to recursively scan for MP4 files"
    )
):
    """Scans a directory recursively and outputs the total duration of all .mp4 files."""
    target_dir = path.resolve()
    
    if not target_dir.exists():
        typer.secho(f"Error: Path not found: {target_dir}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    
    if not target_dir.is_dir():
        typer.secho(f"Error: Not a directory: {target_dir}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    
    # Find all MP4 files recursively
    mp4_files = list(target_dir.rglob("*.mp4"))
    
    if not mp4_files:
        typer.echo(f"No MP4 files found in {target_dir}")
        raise typer.Exit()
    
    typer.echo(f"Scanning {len(mp4_files)} MP4 files...\n")
    
    total_seconds = 0.0
    file_count = 0
    errors = []
    
    # Use Typer's built-in progress bar instead of manual print tracking
    with typer.progressbar(mp4_files, label="Processing videos") as progress:
        for video_file in progress:
            duration = get_video_duration(video_file)
            
            if duration is None:
                errors.append(f"Failed: {video_file.name}")
            elif duration > 0:
                total_seconds += duration
                file_count += 1
            else:
                errors.append(f"No duration: {video_file.name}")
    
    # Display results
    typer.echo(f"\n{'='*50}")
    typer.secho(f"✓ Processed: {file_count} files", fg=typer.colors.GREEN)
    
    if errors:
        typer.secho(f"⚠ Issues: {len(errors)}", fg=typer.colors.YELLOW)
        if len(errors) <= 5:
            for error in errors:
                typer.echo(f"  {error}")
        else:
            for error in errors[:3]:
                typer.echo(f"  {error}")
            typer.echo(f"  ... and {len(errors) - 3} more")
    
    # Format duration
    td = timedelta(seconds=int(total_seconds))
    # hours, remainder = divmod(td.seconds, 3600)
    # minutes, seconds = divmod(remainder, 60)
    # hours += td.days * 24
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    
    typer.secho(f"\n🎬 Total: {hours:02d}:{minutes:02d}:{seconds:02d}", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"   ({total_seconds:.2f} seconds)")
    typer.echo(f"{'='*50}")

if __name__ == "__main__":
    app()