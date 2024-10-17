import os
import subprocess

ffmpeg_path = '../bin/ffmpeg.exe'

def replace_extension(filename, extension='mp3'):
    file_name, _ = os.path.splitext(filename)
    return f"{file_name}.{extension}"

def toMP3(fileToConvert, output_file='Optional'):
    output_file = replace_extension(fileToConvert) if output_file == 'Optional' else output_file
    
    fileToConvert = os.path.abspath(fileToConvert)
    output_file = os.path.abspath(output_file)

    ffmpeg_command = [ffmpeg_path, '-i', fileToConvert, output_file]
    
    print(f"Converting {fileToConvert} to {output_file}")

    try:
        result = subprocess.run(
            ffmpeg_command, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print(f"Conversion successful: {output_file}")
            
            if not fileToConvert.endswith('.mp3'):
                try:
                    os.remove(fileToConvert)
                    print(f"Deleted: {fileToConvert}")
                except OSError as e:
                    print(f"Error deleting file {fileToConvert}: {e}")
        else:
            print(f"Conversion failed with return code: {result.returncode}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during conversion: {e}")

if __name__ == '__main__':
    toMP3(os.path.join(os.path.dirname(os.path.realpath('.')), 'songs/Discord’s Discovery Feature is perfectly balanced....webm'), output_file='Optional')