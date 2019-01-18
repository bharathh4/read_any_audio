import os
from os.path import join
import subprocess, shlex
from sys import argv

import scipy, scipy.io.wavfile
import numpy as np

OS_TYPE = os.name

if not os.path.exists('temp'):
    os.mkdir('temp')

def run(cmd):    
    try:
        output = subprocess.check_output(shlex.split(cmd))
        return [out for out in output.split(b'\n') if out]
    except subprocess.CalledProcessError as e:
        print('Command {0} failed to execute. {1}'.format(cmd, repr(e)))
        exit(1)
    
def convert(filepath):

    filename = os.path.split(filepath)[-1]
    outputfilepath = join('temp', filename)
    cmd = '''sox "%s" -e signed-integer -c 1 "%s"''' % (filepath, outputfilepath)
    run(cmd)
    return outputfilepath

def is_pcm(filepath):

    cmd_windows = 'sox --i "%s"' % filepath
    cmd_linux = 'soxi "%s"' % filepath
    platform_cmd = {'nt': cmd_windows, 'posix': cmd_linux}
    output = run(platform_cmd[OS_TYPE])
    encoding_details = output[-1].split(b": ")
    return b'Signed Integer PCM' in encoding_details

def read_audio(filepath):

    if not is_pcm(filepath):
        filepath = convert(filepath)

    fs, y = scipy.io.wavfile.read(filepath, mmap=False)
    return y, fs
    
if __name__ == "__main__":
    
    filepath = join('audio', 'aaron.wav')
    y, fs = read_audio(filepath)
