import os
import requests
from zipfile import ZipFile

def unblockDLLs(path2dlls):
    """Unblock DLLs"""
    for filename in os.listdir(path2dlls):
        if filename.endswith(".dll"):
            try:
                os.remove(os.path.join(pathDLL,filename+":"+"Zone.Identifier"))
            except:
                pass





PATHVM = os.path.abspath(os.path.join(os.path.dirname(__file__)))

print("\n------- Fetching DLLs --------")

# Get the zip of DLLs
path2zip = os.path.join(PATHVM,"DLLs.zip")
path2GithubZip = r"https://github.com/Videometer/videometer-toolbox-python/raw/main/src/videometer/DLLs.zip?download="

print("\n------- Finished fetching --------")
print("\n------- Unzipping.. --------")

r = requests.get(path2GithubZip)
with open(path2zip, "wb") as code:
    code.write(r.content)

# Unzip
with ZipFile(path2zip, 'r') as zObject:
    zObject.extractall(path=PATHVM)

print("\n------- Removing zip and unblocking DLLs ... --------")

# Delete zip file 
os.remove(path2zip)

path2dlls = os.path.join(PATHVM, "DLLs")
# Unlock all zip files 
intelDlls = os.path.join(path2dlls,"IPP2019Update1","intel64")
videometerDlls = os.path.join(path2dlls,"VM")

unblockDLLs(intelDlls)
unblockDLLs(videometerDlls)

print("\n------- Finished successfully! --------")


