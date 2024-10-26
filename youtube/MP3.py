import os
import subprocess

ffmpeg_path = './bin/ffmpeg.exe'

extension = 'wav'
def replace_extension(filename, extension=extension):
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


def run_ffmpeg(input_file, output_file=""):
    if output_file == '':
        output_file = replace_extension(input_file)

    command = [ffmpeg_path, '-i', input_file, output_file]
    print("Running command:", ' '.join(command))
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    
    while True:
        output = process.stderr.readline()        
        if output == "" and process.poll() is not None:  break
        if output: print(output.strip())
        if process.stdin: process.stdin.write('y\n');
    
    process.wait()

    if process.returncode == 0:
        print(f"Conversion successful: {output_file}")
        
        if not input_file.endswith('.mp3'):
            try:
                os.remove(input_file)
                print(f"Deleted: {input_file}")
            except OSError as e:
                print(f"Error deleting file {input_file}: {e}")
    else:
        print(f"Conversion failed with return code: {process.returncode}")
    print(f"Conversion complete!\n {input_file} -> {output_file}")
