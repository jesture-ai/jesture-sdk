# jesture-sdk

Official repo for Jesture AI SDK.

## MacOS howto

### Install (if you are the SDK client)

```
unzip jesturesdk-osx-x64-0.1.0.zip
sudo bash offline_install.sh
GLOG_logtostderr=1 ./full_main_cpu --cam_device_id=ID
```

### Deinstall

```
sudo bash remove_jesture_sdk.sh  # remove all installed dependencies
cd ..
sudo rm -r jesturesdk-osx-x64-0.1.0  # remove the folder with the SDK
```

### Make new release (if you are the SDK developer)

```
sudo bash build_sdk.sh  # build, move and change dynamic lybraries paths
sudo bash make_release.sh  # zip all dependencies and SDK binary
```

If you made some changes to the dependencies (onnxruntime, OpenCV), check if all the files are in corresponding folders in `third_party/` folder and execute:
```
sudo bash zip_third_parties.sh
```
Also edit `make_release.sh` if you have new dependencies.
