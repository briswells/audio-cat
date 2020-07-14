#!/usr/bin/env python3
from pydub import AudioSegment
import os
import re
import sys

debug = False

def print_help():
    print("Usage: audio-cat [input filepath] [export filename] [export format]")
    print("Required:\n  [input filepath] [export filename]")
    print("Optional:\n  [export format] -- will default to .wav")

def arg_check(argv):
    if argv[1] == "--help":
        print_help()
        return

    if len(argv) < 3 or len(argv) > 4:
        print("Invalid number of arguments use --help for usage")
        return

    argument = {"path":str(argv[1]),"name":str(argv[2])}

    try:
        argument["export"] = str(argv[3])
    except:
        argument["export"] = "wav"

    return argument

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
    info = arg_check(sys.argv)

    # Update cwd to audiobook location
    os.chdir(info["path"])

    # gather file names and sorts into numerical order and combines into one track
    audiobook = combine_tracks()

    export_book(audiobook, info["name"], info["export"])


if __name__ == "__main__":
    main()
