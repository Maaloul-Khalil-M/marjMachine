#!/usr/bin/env python3
import sys
import json
import subprocess
from pathlib import Path
from datetime import timedelta

def get_video_duration(file_path):
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
        
    except Exception as e:
        return None

def lenvid(directory="."):
    path = Path(directory).resolve()
    
    if not path.exists():
        print(f"Error: Path not found: {directory}", file=sys.stderr)
        sys.exit(1)
    
    if not path.is_dir():
        print(f"Error: Not a directory: {directory}", file=sys.stderr)
        sys.exit(1)
    
    # Find all MP4 files
    mp4_files = list(path.rglob("*.mp4"))
    
    if not mp4_files:
        print(f"No MP4 files found in {directory}")
        return
    
    print(f"Scanning {len(mp4_files)} MP4 files...\n")
    
    total_seconds = 0.0
    file_count = 0
    errors = []
    
    for idx, video_file in enumerate(mp4_files, 1):
        # Progress indicator
        if idx % 10 == 0 or idx == len(mp4_files):
            print(f"Progress: {idx}/{len(mp4_files)}", end='\r', flush=True)
        
        duration = get_video_duration(video_file)
        
        if duration is None:
            errors.append(f"Failed: {video_file.name}")
        elif duration > 0:
            total_seconds += duration
            file_count += 1
        else:
            errors.append(f"No duration: {video_file.name}")
    
    print()  # New line after progress
    
    # Display results
    print(f"\n{'='*50}")
    print(f"✓ Processed: {file_count} files")
    
    if errors:
        print(f"⚠ Issues: {len(errors)}")
        if len(errors) <= 5:
            for error in errors:
                print(f"  {error}")
        else:
            for error in errors[:3]:
                print(f"  {error}")
            print(f"  ... and {len(errors) - 3} more")
    
    # Format duration
    td = timedelta(seconds=int(total_seconds))
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours += td.days * 24
    
    print(f"\n🎬 Total: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print(f"   ({total_seconds:.2f} seconds)")
    print(f"{'='*50}")

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    lenvid(directory)