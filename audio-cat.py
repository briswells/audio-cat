#!/usr/bin/env python3
from pydub import AudioSegment
import os
import re
import sys
import argparse

debug = False

def print_help():
    print("Usage: audio-cat [options] [export filename] [input filepath]")
    print("Required:\n\t[input filepath] [export filename]")
    print("Optional:\n\t[-f export format]  will default to .wav\n\t[-m] enables multiprocess execution")
    print('Example:\n\t python audio-cat -f mp3 -m "The Night Circus" "C:/Documents/The Night Circus"')

def arg_parse(parser):
    parser.add_argument('-help', action='store_true',
                        default=False,
                        dest='help')

    parser.add_argument('-m', action='store_true',
                        default=False,
                        dest='multi')

    parser.add_argument('-f', action='store',
                        default="wav",
                        dest='format')

    parser.add_argument('name', nargs='?', default='null')
    parser.add_argument('filepath', nargs='?', default='null')

    results = parser.parse_args()
    print(results)

    if results.help:
        print_help()
        exit()

    if results.name == 'null':
        print("Invalid arguments: Please add export name")
        exit()

    if results.filepath == 'null':
        print("Invalid arguments: Please add import filepath")
        exit()
    return results

# Sorting algorithm that will sort using any ints in the track names
def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',text) ]

def combine_tracks():
        tracks = []
        first = True
        audiobook = None
        for filename in os.listdir(os.getcwd()):
            tracks.append(str(filename))
        tracks.sort(key=natural_keys)

        # combines files into one master track
        for file in tracks:
            if first:
                #added since I was unable to append to a null variable
                audiobook = AudioSegment.from_mp3(file)
                first = False
                if debug:
                    print("Opened first file: " + file)
            else:
                try:
                    song = AudioSegment.from_mp3(file)
                    if debug:
                        print("Just opened " + file)
                    audiobook += song
                except:
                    break
        return audiobook

def export_book(book, name, export):
        #attempting to export with given format but error will cause an override to wav
        try:
            book.export(name + "." + export, format=export)
        except:
            print("Unable to export to requested format. Overriding to .WAV")
            os.remove(name + "." + export )
            book.export(name + "." + "wav", format="wav")


def main():
    #checks arguments
    parser = argparse.ArgumentParser(add_help=False)
    info = arg_parse(parser)

    # Update cwd to audiobook location
    os.chdir(info.filepath)

    # gather file names and sorts into numerical order and combines into one track
    audiobook = combine_tracks()

    export_book(audiobook, info.name, info.format)


if __name__ == "__main__":
    main()
