#!/usr/bin/python3

import argparse
import re
import hashlib
import base64

def main():
    parser = argparse.ArgumentParser(description="Adjust hashes in an unpacked JARs MANIFEST.MF.")
    parser.add_argument("--manifest", dest="manifestFile", help="Path to the MANIFEST.MF to modify")
    parser.add_argument("--src", dest="srcDirectory", help="Path to the unpacked JAR")

    parser.add_argument("additionalFiles", metavar="FILE", nargs="*", help="Paths within the unpacked JAR to additional files to be included in the MANIFEST")

    args = parser.parse_args()

    prefix, files = parseManifest(args.manifestFile)
    for _file in args.additionalFiles:
        files.append(_file)
   
    fileHashMap = calculateHashes(args.srcDirectory, files)
    
    manifest = str(prefix[0])
    for (_file, _hash) in fileHashMap.items():
        manifest += "Name: " + _file + "\n"
        manifest += "SHA-256-Digest: " + _hash.decode("UTF-8") + "\n\n"
   
    writeOutput(manifest, args.manifestFile)

def writeOutput(manifest, manifestFile):
    with open(manifestFile, "w") as f:
        f.write(manifest)



def calculateHashes(srcDirectory, files):
    fileHashMap = {}
    for _file in files:
        _file = re.sub(r'\s', '', _file)
        data = None
        with open(srcDirectory + "/" + _file, "rb") as f:
            data = f.read()
        fileHashMap[_file] = base64.b64encode(hashlib.sha256(data).digest())

    return fileHashMap
        

def parseManifest(manifestFile):
    data = None
    with open(manifestFile, "r") as f:
        data = f.read()
    prefix = re.findall(r'^([\w\W]+?)Name:', data)
    filenames = re.findall(r'Name:\s+([\w\W]+?)SHA', data)
    return prefix, filenames



if __name__ == "__main__":
    main()
