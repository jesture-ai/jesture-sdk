# jesture-sdk

Official repo of Jesture AI SDK.

## Use-cases with Jesture AI SDK
Immersive Gaming | Web apps                                                                                          
:----------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: 
![gaming](docs/gifs/afterspell.gif)| ![web](docs/gifs/web.gif)

Slides Control | Snap Masks                                                                                                                     
:-------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------:
![slides](docs/gifs/slides.gif)| ![snap](docs/gifs/snap-zoom.gif)

## MacOS howto

### Install (if you are the SDK client)

```
unzip jesturesdk-osx-x64-0.1.0.zip
sudo bash offline_install.sh
GLOG_logtostderr=1 ./main_full_cpu --cam_device_id=ID
```

### Deinstall

```
sudo bash remove_jesture_sdk.sh  # remove all installed dependencies
cd ..
sudo rm -r jesturesdk-osx-x64-0.1.0  # remove the folder with the SDK
```

### Make new release (if you are the SDK developer)

```
# build executable, move and change dynamic lybraries paths
sudo bash build_sdk.sh main_full_cpu 

# build shared object, move and change dynamic lybraries paths
sudo bash build_sdk.sh full_cpu.dylib  

# zip all dependencies and SDK binary
sudo bash make_release.sh  
```

If you made some changes to the dependencies (onnxruntime, OpenCV), check if all the files are in corresponding folders in `third_party/` folder and execute:
```
sudo bash zip_third_parties.sh
```
Also edit `make_release.sh` if you have new dependencies.
