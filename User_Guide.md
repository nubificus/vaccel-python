# vAccel Python bindings

This document briefly describes the process to use vAccel from Python programs.

- [Build from Source](#build-from-source) or [get the binary packages](#get-the-binary-packages) [currently only for Debian/Ubuntu variants and pip]
- Run a [simple example](#simple-example) [using the `noop` plugin]
- Run a more [elaborate example](#jetson-example) [using the `jetson-inference` plugin]

## Get the binary packages

We provide freshly built packages, based on the current development of the
vAccel components.

### Get vAccelRT deb

You can install vAccelRT (in `/usr/local`) using the following commands:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
sudo dpkg -i vaccel-0.5.0-Linux.deb
```

### Get python bindings

#### Prerequisites

In Ubuntu-based systems, you need to have the following packages installed:

```bash
sudo apt-get install -y python3-dev python3-venv python3-pip
```

#### Install the Python package

To install the python bindings we use a whl package. Create a fresh virtual environment and install the package there:

```bash
python3 -m venv .vaccel-venv
.vaccel-venv/bin/pip3 install https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-python-0.0.1.tar.gz
```

## Build from Source

### Prerequisites for building

In Ubuntu-based systems, you need to have the following packages to build `vaccelrt`:

- cmake
- build-essential
- python3-dev
- python3-venv

You can install them using the following command:

```bash
sudo apt-get install -y cmake build-essential python3-dev python3-venv
```

### Get the source code

Get the source code for **python-vaccel** and **vaccelrt**:

```bash
git clone https://github.com/nubificus/python-vaccel.git
cd python-vaccel
mkdir libs
cd libs
git clone https://github.com/cloudkernels/vaccelrt --recursive
```

### Build and install vaccelrt

Build vaccelrt and package it in a **.deb** file:

```bash
cd vaccelrt
mkdir build
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_PLUGIN_NOOP=ON -DBUILD_EXAMPLES=ON
make
cpack
```

Install **vaccelrt**:

```bash
sudo dpkg -i vaccel*.deb
```

***

### Build the Python package

We will create a virtual environment to install the **python-vaccel** package inside the root directory of **python-vaccel**.

```bash
cd ../../..
python3 -m venv venv
```

Now, go ahead and activate the newly created environment:

```bash
. venv/bin/activate
```

Update pip and install Python's dependencies:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install wheel
python3 -m pip install flake8 build setuptools \
    cffi pytest pytest-cov datestamp cmake_build_extension
```

Now let's build the package:

```bash
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib
export PYTHONPATH=.
python3 builder.py
python3 setup.py install
```

[Optional] Run the tests to make sure everything was build correctly:

```bash
python3 -m pytest
```

## Do It Yourself

To see python vAccel bindings in action, let's try the following example:

### Simple Example

Download an adorable kitten photo:

```bash
wget https://i.imgur.com/aSuOWgU.jpeg -O cat.jpeg
```

***

Create a new python file called **cat.py** and add the following lines:

```python
from vaccel.session import Session
from vaccel.image import ImageClassify

source = "cat.jpeg"

def main():
    ses = Session(flags=3)
    print(f'Session id is {ses.id()}')
    res = ImageClassify.classify_from_filename(session=ses, source=source)
    print(res)

if __name__=="__main__":
    main()
```

Now, when you run that python file, you can see the dummy classification tag for that image:

```bash
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib
export PYTHONPATH=.
python3 cat.py
# Loading libvaccel
# Loading plugins
# Loading plugin: /usr/local/lib/libvaccel-noop.so
# Loaded plugin noop from /usr/local/lib/libvaccel-noop.so
# Session id is 1
# [noop] Calling Image classification for session 1
# [noop] Dumping arguments for Image classification:
# [noop] len_img: 54372
# [noop] will return a dummy result
# This is a dummy classification tag!
# Shutting down vAccel
```

### Jetson example

To use vAccel on a more real-life example we'll use the jetson-inference framework. This way we will be able to perform image inference on a GPU and get something more useful than a dummy classification tag ;-)

Let's re-use the python program from the [simple example](#simple-example) above.

#### `x86_64`

We will need to use a host with an NVIDIA GPU (our's is just an `RTX 2060
SUPER`) and jetson-inference installed. To facilitate dependency resolving we
use a [container image](#appendix-i-build-a-jetson-inference-container-image)
on a host with nvidia-container-runtime installed.

so, assuming our code is in `/data/code` let's spawn our container and see this in action:

```bash
docker run --gpus 0 --rm -it -v/data/code:/data/ -w /data nubificus/jetson-inference-updated:x86_64 /bin/bash
```

Afterwards, the steps are more or less the same as above. Install the vAccelRT package:

```bash
root@32e90efe86b9:/data/code# wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
--2022-11-05 13:43:43--  https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
Resolving s3.nbfc.io (s3.nbfc.io)... 84.254.1.240
Connecting to s3.nbfc.io (s3.nbfc.io)|84.254.1.240|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2124230 (2.0M) [application/x-debian-package]
Saving to: 'vaccel-0.5.0-Linux.deb'

vaccel-0.5.0-Linux.deb          100%[=======================================================>]   2.03M  --.-KB/s    in 0.06s

2022-11-05 13:43:43 (33.8 MB/s) - 'vaccel-0.5.0-Linux.deb' saved [2124230/2124230]

root@32e90efe86b9:/data/code# dpkg -i vaccel-0.5.0-Linux.deb
Selecting previously unselected package vaccel.
(Reading database ... 60677 files and directories currently installed.)
Preparing to unpack vaccel-0.5.0-Linux.deb ...
Unpacking vaccel (0.5.0) ...
Setting up vaccel (0.5.0) ...
```

Get and install the jetson plugin:

```bash
root@32e90efe86b9:/data/code# wget https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/jetson_inference/master/x86_64/vaccelrt-plugin-jetson-0.1-Linux.deb
--2022-11-05 14:45:53--  https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/jetson_inference/master/x86_64/vaccelrt-plugin-jetson-0.1-Linux.deb
Resolving s3.nubificus.co.uk (s3.nubificus.co.uk)... 84.254.1.240
Connecting to s3.nubificus.co.uk (s3.nubificus.co.uk)|84.254.1.240|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 13146 (13K) [application/x-debian-package]
Saving to: 'vaccelrt-plugin-jetson-0.1-Linux.deb'

vaccelrt-plugin-jetson-0.1-Linu 100%[=======================================================>]  12.84K  --.-KB/s    in 0.001s

2022-11-05 14:45:53 (8.39 MB/s) - 'vaccelrt-plugin-jetson-0.1-Linux.deb' saved [13146/13146]

root@32e90efe86b9:/data/code# dpkg -i vaccelrt-plugin-jetson-0.1-Linux.deb
(Reading database ... 60748 files and directories currently installed.)
Preparing to unpack vaccelrt-plugin-jetson-0.1-Linux.deb ...
Unpacking vaccelrt-plugin-jetson (0.1) over (0.1) ...
Setting up vaccelrt-plugin-jetson (0.1) ...
```

Install the bindings:

```bash
root@32e90efe86b9:/data/code# .vaccel-venv/bin/pip3 install https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-2022.11.5.tar.gz
Collecting https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-2022.11.5.tar.gz
  Downloading https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-2022.11.5.tar.gz (23 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
    Preparing wheel metadata ... done
Collecting cffi>=1.0.0
  Using cached cffi-1.15.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (442 kB)
Collecting pycparser
  Using cached pycparser-2.21-py2.py3-none-any.whl (118 kB)
Building wheels for collected packages: vaccel
  Building wheel for vaccel (PEP 517) ... done
  Created wheel for vaccel: filename=vaccel-2022.11.5-cp38-cp38-linux_x86_64.whl size=44494 sha256=a63bd263ba219e985821fc34416dc8f12ced508eb8e265b78a896ac2ed375f72
  Stored in directory: /root/.cache/pip/wheels/a6/e6/1c/4c91a42c1cad7e5e4ca86acd006bcded10cba25e85268e81ef
Successfully built vaccel
Installing collected packages: pycparser, cffi, vaccel
Successfully installed cffi-1.15.1 pycparser-2.21 vaccel-2022.11.5
```

Now let's go ahead and run the example!

```bash
root@32e90efe86b9:/data/code# export LD_LIBRARY_PATH=/usr/local/lib/
root@32e90efe86b9:/data/code# export VACCEL_BACKENDS=/usr/local/lib/libvaccel-jetson.so
root@32e90efe86b9:/data/code# export VACCEL_IMAGENET_NETWORKS=/data/code/networks
root@32e90efe86b9:/data/code# .vaccel-venv/bin/python3 cat.py
Loading libvaccel
Loading plugins
Loading plugin: /usr/local/lib/libvaccel-jetson.so
Loaded plugin jetson-inference from ./libvaccel-jetson.so

imageNet -- loading classification network model from:
         -- prototxt     ./local_net//googlenet.prototxt
         -- model        ./local_net//bvlc_googlenet.caffemodel
         -- class_labels ./local_net//ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.5.1
[TRT]    loading NVIDIA plugins...
[TRT]    Registered plugin creator - ::BatchedNMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::BatchedNMS_TRT version 1
[TRT]    Registered plugin creator - ::BatchTilePlugin_TRT version 1
[TRT]    Registered plugin creator - ::Clip_TRT version 1
[TRT]    Registered plugin creator - ::CoordConvAC version 1
[TRT]    Registered plugin creator - ::CropAndResizeDynamic version 1
[TRT]    Registered plugin creator - ::CropAndResize version 1
[TRT]    Registered plugin creator - ::DecodeBbox3DPlugin version 1
[TRT]    Registered plugin creator - ::DetectionLayer_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Explicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Implicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_ONNX_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_TRT version 1
[TRT]    Could not register plugin creator -  ::FlattenConcat_TRT version 1
[TRT]    Registered plugin creator - ::GenerateDetection_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchor_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchorRect_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 2
[TRT]    Registered plugin creator - ::LReLU_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelCropAndResize_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelProposeROI_TRT version 1
[TRT]    Registered plugin creator - ::MultiscaleDeformableAttnPlugin_TRT version 1
[TRT]    Registered plugin creator - ::NMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::NMS_TRT version 1
[TRT]    Registered plugin creator - ::Normalize_TRT version 1
[TRT]    Registered plugin creator - ::PillarScatterPlugin version 1
[TRT]    Registered plugin creator - ::PriorBox_TRT version 1
[TRT]    Registered plugin creator - ::ProposalDynamic version 1
[TRT]    Registered plugin creator - ::ProposalLayer_TRT version 1
[TRT]    Registered plugin creator - ::Proposal version 1
[TRT]    Registered plugin creator - ::PyramidROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::Region_TRT version 1
[TRT]    Registered plugin creator - ::Reorg_TRT version 1
[TRT]    Registered plugin creator - ::ResizeNearest_TRT version 1
[TRT]    Registered plugin creator - ::ROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::RPROI_TRT version 1
[TRT]    Registered plugin creator - ::ScatterND version 1
[TRT]    Registered plugin creator - ::SpecialSlice_TRT version 1
[TRT]    Registered plugin creator - ::Split version 1
[TRT]    Registered plugin creator - ::VoxelGeneratorPlugin version 1
[TRT]    detected model format - caffe  (extension '.caffemodel')
[TRT]    desired precision specified for GPU: FASTEST
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +307, GPU +0, now: CPU 320, GPU 223 (MiB)
[TRT]    Trying to load shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    Loaded shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    [MemUsageChange] Init builder kernel library: CPU +262, GPU +74, now: CPU 636, GPU 297 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]    native precisions detected for GPU:  FP32, FP16, INT8
[TRT]    selecting fastest native precision for GPU:  FP16
[TRT]    attempting to open engine cache file ./local_net//bvlc_googlenet.caffemodel.1.1.8501.GPU.FP16.engine
[TRT]    loading network plan from engine cache... ./local_net//bvlc_googlenet.caffemodel.1.1.8501.GPU.FP16.engine
[TRT]    device GPU, loaded ./local_net//bvlc_googlenet.caffemodel
[TRT]    Loaded engine size: 15 MiB
[TRT]    Trying to load shared library libcudnn.so.8
[TRT]    Loaded shared library libcudnn.so.8
[TRT]    Using cuDNN as plugin tactic source
[TRT]    Using cuDNN as core library tactic source
[TRT]    [MemUsageChange] Init cuDNN: CPU +576, GPU +236, now: CPU 977, GPU 477 (MiB)
[TRT]    Deserialization required 488590 microseconds.
[TRT]    [MemUsageChange] TensorRT-managed allocation in engine deserialization: CPU +0, GPU +13, now: CPU 0, GPU 13 (MiB)
[TRT]    Trying to load shared library libcudnn.so.8
[TRT]    Loaded shared library libcudnn.so.8
[TRT]    Using cuDNN as plugin tactic source
[TRT]    Using cuDNN as core library tactic source
[TRT]    [MemUsageChange] Init cuDNN: CPU +0, GPU +8, now: CPU 977, GPU 477 (MiB)
[TRT]    Total per-runner device persistent memory is 94720
[TRT]    Total per-runner host persistent memory is 147088
[TRT]    Allocated activation device memory of size 3612672
[TRT]    [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +3, now: CPU 0, GPU 16 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       72
[TRT]       -- maxBatchSize 1
[TRT]       -- deviceMemory 3612672
[TRT]       -- bindings     2
[TRT]       binding 0
                -- index   0
                -- name    'data'
                -- type    FP32
                -- in/out  INPUT
                -- # dims  3
                -- dim #0  3
                -- dim #1  224
                -- dim #2  224
[TRT]       binding 1
                -- index   1
                -- name    'prob'
                -- type    FP32
                -- in/out  OUTPUT
                -- # dims  3
                -- dim #0  1000
                -- dim #1  1
                -- dim #2  1
[TRT]
[TRT]    binding to input 0 data  binding index:  0
[TRT]    binding to input 0 data  dims (b=1 c=3 h=224 w=224) size=602112
[TRT]    binding to output 0 prob  binding index:  1
[TRT]    binding to output 0 prob  dims (b=1 c=1000 h=1 w=1) size=4000
[TRT]
[TRT]    device GPU, ./local_net//bvlc_googlenet.caffemodel initialized.
[TRT]    imageNet -- loaded 1000 class info entries
[TRT]    imageNet -- ./local_net//bvlc_googlenet.caffemodel initialized.
class 0281 - 0.219604  (tabby, tabby cat)
class 0282 - 0.062927  (tiger cat)
class 0283 - 0.018173  (Persian cat)
class 0284 - 0.017746  (Siamese cat, Siamese)
class 0285 - 0.483398  (Egyptian cat)
class 0287 - 0.180664  (lynx, catamount)
imagenet: 48.33984% class #285 (Egyptian cat)
imagenet: attempting to save output image
imagenet: completed saving
imagenet: shutting down...
48.340% Egyptian cat
Shutting down vAccel
```

#### `aarch64`

For aarch64 things are more or less the same. We run the example on a Jetson
Xavier AGX, so jetson-inference and the nvidia stack is included in the Jetson
Linux variant (L4T).

The steps to take only refer to installing jetson-inference libs, vAccel and
the python bindings so assuming there's a Jetson Linux distro with Jetpack
installed:

- install jetson-inference:

```bash
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference 
mkdir build
cd build
cmake ../
make install
```

- install vAccelRT:

```bash
wget https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/master/aarch64/Release-deb/vaccel-0.5.0-Linux.deb
dpkg -i vaccel-0.5.0-Linux.deb
```

- install the jetson plugin:

```bash
wget https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/jetson_inference/master/aarch64/vaccelrt-plugin-jetson-0.1-Linux.deb
dpkg -i vaccelrt-plugin-jetson-0.1-Linux.deb
```

- install python bindings in a virtual env:

```bash
python3 -m venv .vaccel-venv
.vaccel-venv/bin/pip3 install https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/aarch64/vaccel-2022.11.5.tar.gz
```

- run the example:

```bash
# .vaccel-venv/bin/python3 cat.py
Loading libvaccel
2022.11.05-20:25:12.79 - <debug> Initializing vAccel
2022.11.05-20:25:12.79 - <debug> Created top-level rundir: /run/user/0/vaccel.G2ZhVr
Loading plugins
Loading plugin: /usr/local/lib/libvaccel-jetson.so
2022.11.05-20:25:12.91 - <debug> Registered plugin jetson-inference
2022.11.05-20:25:12.91 - <debug> Registered function image classification from plugin jetson-inference
2022.11.05-20:25:12.91 - <debug> Registered function image detection from plugin jetson-inference
2022.11.05-20:25:12.91 - <debug> Registered function image segmentation from plugin jetson-inference
Loaded plugin jetson-inference from /usr/local/lib/libvaccel-jetson.so
2022.11.05-20:25:12.96 - <debug> session:1 New session
Session id is 1
2022.11.05-20:25:12.96 - <debug> session:1 Looking for plugin implementing image classification
2022.11.05-20:25:12.96 - <debug> Found implementation in jetson-inference plugin

imageNet -- loading classification network model from:
         -- prototxt     /home/ananos/develop/jetson-inference/data/networks/googlenet.prototxt
         -- model        /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel
         -- class_labels /home/ananos/develop/jetson-inference/data/networks/ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.4.1
[TRT]    loading NVIDIA plugins...
[TRT]    Registered plugin creator - ::GridAnchor_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchorRect_TRT version 1
[TRT]    Registered plugin creator - ::NMS_TRT version 1
[TRT]    Registered plugin creator - ::Reorg_TRT version 1
[TRT]    Registered plugin creator - ::Region_TRT version 1
[TRT]    Registered plugin creator - ::Clip_TRT version 1
[TRT]    Registered plugin creator - ::LReLU_TRT version 1
[TRT]    Registered plugin creator - ::PriorBox_TRT version 1
[TRT]    Registered plugin creator - ::Normalize_TRT version 1
[TRT]    Registered plugin creator - ::ScatterND version 1
[TRT]    Registered plugin creator - ::RPROI_TRT version 1
[TRT]    Registered plugin creator - ::BatchedNMS_TRT version 1
[TRT]    Registered plugin creator - ::BatchedNMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::BatchTilePlugin_TRT version 1
[TRT]    Could not register plugin creator -  ::FlattenConcat_TRT version 1
[TRT]    Registered plugin creator - ::CropAndResize version 1
[TRT]    Registered plugin creator - ::CropAndResizeDynamic version 1
[TRT]    Registered plugin creator - ::DetectionLayer_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_ONNX_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Explicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Implicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::ProposalDynamic version 1
[TRT]    Registered plugin creator - ::Proposal version 1
[TRT]    Registered plugin creator - ::ProposalLayer_TRT version 1
[TRT]    Registered plugin creator - ::PyramidROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::ResizeNearest_TRT version 1
[TRT]    Registered plugin creator - ::Split version 1
[TRT]    Registered plugin creator - ::SpecialSlice_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 2
[TRT]    Registered plugin creator - ::CoordConvAC version 1
[TRT]    Registered plugin creator - ::DecodeBbox3DPlugin version 1
[TRT]    Registered plugin creator - ::GenerateDetection_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelCropAndResize_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelProposeROI_TRT version 1
[TRT]    Registered plugin creator - ::NMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::PillarScatterPlugin version 1
[TRT]    Registered plugin creator - ::VoxelGeneratorPlugin version 1
[TRT]    Registered plugin creator - ::MultiscaleDeformableAttnPlugin_TRT version 1
[TRT]    detected model format - caffe  (extension '.caffemodel')
[TRT]    desired precision specified for GPU: FASTEST
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +187, GPU +0, now: CPU 211, GPU 3925 (MiB)
[TRT]    [MemUsageChange] Init builder kernel library: CPU +131, GPU +123, now: CPU 361, GPU 4067 (MiB)
[TRT]    native precisions detected for GPU:  FP32, FP16, INT8
[TRT]    selecting fastest native precision for GPU:  FP16
[TRT]    found engine cache file /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel.1.1.8401.GPU.FP16.engine
[TRT]    found model checksum /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel.sha256sum
[TRT]    echo "$(cat /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel.sha256sum) /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel" | sha256sum --check --status
[TRT]    model matched checksum /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel.sha256sum
[TRT]    loading network plan from engine cache... /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel.1.1.8401.GPU.FP16.engine
[TRT]    device GPU, loaded /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel
[TRT]    [MemUsageChange] Init CUDA: CPU +0, GPU +0, now: CPU 245, GPU 4080 (MiB)
[TRT]    Loaded engine size: 14 MiB
[TRT]    Deserialization required 15317 microseconds.
[TRT]    [MemUsageChange] TensorRT-managed allocation in engine deserialization: CPU +0, GPU +13, now: CPU 0, GPU 13 (MiB)
[TRT]    Total per-runner device persistent memory is 75776
[TRT]    Total per-runner host persistent memory is 110304
[TRT]    Allocated activation device memory of size 5218304
[TRT]    [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +5, now: CPU 0, GPU 18 (MiB)
[TRT]
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       72
[TRT]       -- maxBatchSize 1
[TRT]       -- deviceMemory 5218304
[TRT]       -- bindings     2
[TRT]       binding 0
                -- index   0
                -- name    'data'
                -- type    FP32
                -- in/out  INPUT
                -- # dims  3
                -- dim #0  3
                -- dim #1  224
                -- dim #2  224
[TRT]       binding 1
                -- index   1
                -- name    'prob'
                -- type    FP32
                -- in/out  OUTPUT
                -- # dims  3
                -- dim #0  1000
                -- dim #1  1
                -- dim #2  1
[TRT]
[TRT]    binding to input 0 data  binding index:  0
[TRT]    binding to input 0 data  dims (b=1 c=3 h=224 w=224) size=602112
[TRT]    binding to output 0 prob  binding index:  1
[TRT]    binding to output 0 prob  dims (b=1 c=1000 h=1 w=1) size=4000
[TRT]
[TRT]    device GPU, /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel initialized.
[TRT]    loaded 1000 class labels
[TRT]    imageNet -- /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel initialized.
class 0281 - 0.222134  (tabby, tabby cat)
class 0282 - 0.063147  (tiger cat)
class 0283 - 0.018521  (Persian cat)
class 0284 - 0.018234  (Siamese cat, Siamese)
class 0285 - 0.477663  (Egyptian cat)
class 0287 - 0.182722  (lynx, catamount)
imagenet: 47.76627% class #285 (Egyptian cat)
imagenet: attempting to save output image
imagenet: completed saving
imagenet: shutting down...
47.766% Egyptian cat
2022.11.05-20:25:16.39 - <debug> session:1 Free session
Shutting down vAccel
2022.11.05-20:25:16.45 - <debug> Shutting down vAccel
2022.11.05-20:25:16.45 - <debug> Cleaning up plugins
2022.11.05-20:25:16.45 - <debug> Unregistered plugin jetson-inference
```

### Appendix I: Build a jetson-inference container image

[Jetson-inference](https://github.com/dusty-nv/jetson-inference) is an suite of
tools built around TensorRT to expose an image inference API. Installing this
suite on x86 used to be a real challenge (kind of still is), but things are
getting better!

We use a container file to capture the individual steps to install jetson inference. Assuming the host is debian-based (we tried that on Ubuntu 20.04), and has a recent NVIDIA driver (`520.61.05`) we follow the steps below:

- clone the container repo:

```bash
git clone https://github.com/nubificus/jetson-inference-container
```

- build the container image:

```bash
docker build -t nubificus/jetson-inference-updated:x86_64 -f Dockerfile .
```

or just get the one we've built (could take some time, i'ts 12GB...):

```bash
docker pull nubificus/jetson-inference-updated:x86_64
```

- run the `jetson-inference` example:

Run the container:

```bash
# docker run --gpus all --rm -it -v/data/code:/data/code -w $PWD nubificus/jetson-inference-updated:x86_64 /bin/bash
root@9f5224cb28cc:/data/code#
```

Use pre-installed example images and models to do image inference:

```bash
root@9f5224cb28cc:/data/code# ln -s /usr/local/data/images .
root@9f5224cb28cc:/data/code# ln -s /usr/local/data/networks .

root@9f5224cb28cc:/data/code# imagenet-console images/dog_0.jpg
[video]  created imageLoader from file:///data/code/images/dog_0.jpg
------------------------------------------------
imageLoader video options:
------------------------------------------------
  -- URI: file:///data/code/images/dog_0.jpg
     - protocol:  file
     - location:  images/dog_0.jpg
     - extension: jpg
  -- deviceType: file
  -- ioType:     input
  -- codec:      unknown
  -- width:      0
  -- height:     0
  -- frameRate:  0.000000
  -- bitRate:    0
  -- numBuffers: 4
  -- zeroCopy:   true
  -- flipMethod: none
  -- loop:       0
  -- rtspLatency 2000
------------------------------------------------
[video]  videoOptions -- failed to parse output resource URI (null)
[video]  videoOutput -- failed to parse command line options
imagenet:  failed to create output stream

imageNet -- loading classification network model from:
         -- prototxt     networks/googlenet.prototxt
         -- model        networks/bvlc_googlenet.caffemodel
         -- class_labels networks/ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.5.1
[TRT]    loading NVIDIA plugins...
[TRT]    Registered plugin creator - ::BatchedNMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::BatchedNMS_TRT version 1
[TRT]    Registered plugin creator - ::BatchTilePlugin_TRT version 1
[TRT]    Registered plugin creator - ::Clip_TRT version 1
[TRT]    Registered plugin creator - ::CoordConvAC version 1
[TRT]    Registered plugin creator - ::CropAndResizeDynamic version 1
[TRT]    Registered plugin creator - ::CropAndResize version 1
[TRT]    Registered plugin creator - ::DecodeBbox3DPlugin version 1
[TRT]    Registered plugin creator - ::DetectionLayer_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Explicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Implicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_ONNX_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_TRT version 1
[TRT]    Could not register plugin creator -  ::FlattenConcat_TRT version 1
[TRT]    Registered plugin creator - ::GenerateDetection_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchor_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchorRect_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 2
[TRT]    Registered plugin creator - ::LReLU_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelCropAndResize_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelProposeROI_TRT version 1
[TRT]    Registered plugin creator - ::MultiscaleDeformableAttnPlugin_TRT version 1
[TRT]    Registered plugin creator - ::NMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::NMS_TRT version 1
[TRT]    Registered plugin creator - ::Normalize_TRT version 1
[TRT]    Registered plugin creator - ::PillarScatterPlugin version 1
[TRT]    Registered plugin creator - ::PriorBox_TRT version 1
[TRT]    Registered plugin creator - ::ProposalDynamic version 1
[TRT]    Registered plugin creator - ::ProposalLayer_TRT version 1
[TRT]    Registered plugin creator - ::Proposal version 1
[TRT]    Registered plugin creator - ::PyramidROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::Region_TRT version 1
[TRT]    Registered plugin creator - ::Reorg_TRT version 1
[TRT]    Registered plugin creator - ::ResizeNearest_TRT version 1
[TRT]    Registered plugin creator - ::ROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::RPROI_TRT version 1
[TRT]    Registered plugin creator - ::ScatterND version 1
[TRT]    Registered plugin creator - ::SpecialSlice_TRT version 1
[TRT]    Registered plugin creator - ::Split version 1
[TRT]    Registered plugin creator - ::VoxelGeneratorPlugin version 1
[TRT]    detected model format - caffe  (extension '.caffemodel')
[TRT]    desired precision specified for GPU: FASTEST
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +298, GPU +0, now: CPU 321, GPU 223 (MiB)
[TRT]    Trying to load shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    Loaded shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    [MemUsageChange] Init builder kernel library: CPU +262, GPU +76, now: CPU 637, GPU 299 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]    native precisions detected for GPU:  FP32, FP16, INT8
[TRT]    selecting fastest native precision for GPU:  FP16
[TRT]    attempting to open engine cache file networks/bvlc_googlenet.caffemodel.1.1.8501.GPU.FP16.engine
[TRT]    loading network plan from engine cache... networks/bvlc_googlenet.caffemodel.1.1.8501.GPU.FP16.engine
[TRT]    device GPU, loaded networks/bvlc_googlenet.caffemodel
[TRT]    Loaded engine size: 15 MiB
[TRT]    Trying to load shared library libcudnn.so.8
[TRT]    Loaded shared library libcudnn.so.8
[TRT]    Using cuDNN as plugin tactic source
[TRT]    Using cuDNN as core library tactic source
[TRT]    [MemUsageChange] Init cuDNN: CPU +576, GPU +236, now: CPU 978, GPU 477 (MiB)
[TRT]    Deserialization required 506628 microseconds.
[TRT]    [MemUsageChange] TensorRT-managed allocation in engine deserialization: CPU +0, GPU +13, now: CPU 0, GPU 13 (MiB)
[TRT]    Trying to load shared library libcudnn.so.8
[TRT]    Loaded shared library libcudnn.so.8
[TRT]    Using cuDNN as plugin tactic source
[TRT]    Using cuDNN as core library tactic source
[TRT]    [MemUsageChange] Init cuDNN: CPU +1, GPU +8, now: CPU 979, GPU 477 (MiB)
[TRT]    Total per-runner device persistent memory is 94720
[TRT]    Total per-runner host persistent memory is 147808
[TRT]    Allocated activation device memory of size 3612672
[TRT]    [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +3, now: CPU 0, GPU 16 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       75
[TRT]       -- maxBatchSize 1
[TRT]       -- deviceMemory 3612672
[TRT]       -- bindings     2
[TRT]       binding 0
                -- index   0
                -- name    'data'
                -- type    FP32
                -- in/out  INPUT
                -- # dims  3
                -- dim #0  3
                -- dim #1  224
                -- dim #2  224
[TRT]       binding 1
                -- index   1
                -- name    'prob'
                -- type    FP32
                -- in/out  OUTPUT
                -- # dims  3
                -- dim #0  1000
                -- dim #1  1
                -- dim #2  1
[TRT]
[TRT]    binding to input 0 data  binding index:  0
[TRT]    binding to input 0 data  dims (b=1 c=3 h=224 w=224) size=602112
[TRT]    binding to output 0 prob  binding index:  1
[TRT]    binding to output 0 prob  dims (b=1 c=1000 h=1 w=1) size=4000
[TRT]
[TRT]    device GPU, networks/bvlc_googlenet.caffemodel initialized.
[TRT]    imageNet -- loaded 1000 class info entries
[TRT]    imageNet -- networks/bvlc_googlenet.caffemodel initialized.
[image]  loaded 'images/dog_0.jpg'  (500x375, 3 channels)
class 0248 - 0.229980  (Eskimo dog, husky)
class 0249 - 0.605469  (malamute, malemute, Alaskan malamute)
class 0250 - 0.160400  (Siberian husky)
imagenet:  60.54688% class #249 (malamute, malemute, Alaskan malamute)

[TRT]    ------------------------------------------------
[TRT]    Timing Report networks/bvlc_googlenet.caffemodel
[TRT]    ------------------------------------------------
[TRT]    Pre-Process   CPU   0.02498ms  CUDA   0.21392ms
[TRT]    Network       CPU   1.04583ms  CUDA   0.86154ms
[TRT]    Post-Process  CPU   0.02265ms  CUDA   0.02288ms
[TRT]    Total         CPU   1.09346ms  CUDA   1.09834ms
[TRT]    ------------------------------------------------

[TRT]    note -- when processing a single image, run 'sudo jetson_clocks' before
                to disable DVFS for more accurate profiling/timing measurements

[image]  imageLoader -- End of Stream (EOS) has been reached, stream has been closed
imagenet:  shutting down...
imagenet:  shutdown complete.
```

**Note**: _The first time the engine needs to do some autotuning, so it will take some time and drop output similar to the one below_:

<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

```bash
...
[TRT]    Tactic: 0x89c2d153627e52ba Time: 0.0134678
[TRT]    loss3/classifier Set Tactic Name: volta_h884cudnn_256x128_ldg8_relu_exp_small_nhwc_tn_v1 Tactic: 0xc110e19c9f5aa36e
[TRT]    Tactic: 0xc110e19c9f5aa36e Time: 0.0752844
[TRT]    loss3/classifier Set Tactic Name: turing_h1688cudnn_256x128_ldg8_relu_exp_medium_nhwc_tn_v1 Tactic: 0xdc1c841ef1cd3e8e
[TRT]    Tactic: 0xdc1c841ef1cd3e8e Time: 0.0422516
[TRT]    loss3/classifier Set Tactic Name: sm70_xmma_fprop_implicit_gemm_f16f16_f16f16_f16_nhwckrsc_nhwc_tilesize128x64x32_stage1_warpsize2x2x1_g1_tensor8x8x4_t1r1s1 Tactic: 0x4c17dc9d992e6a1d
[TRT]    Tactic: 0x4c17dc9d992e6a1d Time: 0.0231476
[TRT]    loss3/classifier Set Tactic Name: sm75_xmma_fprop_implicit_gemm_f16f16_f16f16_f16_nhwckrsc_nhwc_tilesize128x128x64_stage1_warpsize2x2x1_g1_tensor16x8x8_t1r1s1 Tactic: 0xc399fdbffdc34032
[TRT]    Tactic: 0xc399fdbffdc34032 Time: 0.0262451
[TRT]    loss3/classifier Set Tactic Name: turing_h1688cudnn_256x64_sliced1x2_ldg8_relu_exp_interior_nhwc_tn_v1 Tactic: 0x105f56cf03ee5549
[TRT]    Tactic: 0x105f56cf03ee5549 Time: 0.0241811
[TRT]    Fastest Tactic: 0x017a89ce2d82b850 Time: 0.00878863
[TRT]    >>>>>>>>>>>>>>> Chose Runner Type: CaskGemmConvolution Tactic: 0x0000000000020318
[TRT]    =============== Computing costs for
[TRT]    *************** Autotuning format combination: Float(1000,1,1,1) -> Float(1000,1,1,1) ***************
[TRT]    --------------- Timing Runner: prob (CudaSoftMax)
[TRT]    Tactic: 0x00000000000003ea Time: 0.00364102
[TRT]    Fastest Tactic: 0x00000000000003ea Time: 0.00364102
[TRT]    --------------- Timing Runner: prob (CaskSoftMax)
[TRT]    CaskSoftMax has no valid tactics for this config, skipping
[TRT]    >>>>>>>>>>>>>>> Chose Runner Type: CudaSoftMax Tactic: 0x00000000000003ea
[TRT]    *************** Autotuning format combination: Half(1000,1,1,1) -> Half(1000,1,1,1) ***************
[TRT]    --------------- Timing Runner: prob (CudaSoftMax)
[TRT]    Tactic: 0x00000000000003ea Time: 0.00370118
[TRT]    Fastest Tactic: 0x00000000000003ea Time: 0.00370118
[TRT]    --------------- Timing Runner: prob (CaskSoftMax)
[TRT]    CaskSoftMax has no valid tactics for this config, skipping
[TRT]    >>>>>>>>>>>>>>> Chose Runner Type: CudaSoftMax Tactic: 0x00000000000003ea
[TRT]    *************** Autotuning format combination: Half(500,1:2,1,1) -> Half(500,1:2,1,1) ***************
[TRT]    --------------- Timing Runner: prob (CudaSoftMax)
[TRT]    Tactic: 0x0000000000000012 Time: 0.00347464
[TRT]    Fastest Tactic: 0x0000000000000012 Time: 0.00347464
[TRT]    >>>>>>>>>>>>>>> Chose Runner Type: CudaSoftMax Tactic: 0x0000000000000012
[TRT]    Adding reformat layer: Reformatted Input Tensor 0 to conv1/7x7_s2 + conv1/relu_7x7 (data) from Float(150528,50176,224,1) to Half(100352,50176:2,224,1)
[TRT]    Adding reformat layer: Reformatted Input Tensor 0 to conv2/3x3_reduce + conv2/relu_3x3_reduce (pool1/norm1) from Half(100352,3136:2,56,1) to Half(25088,1:8,448,8)
[TRT]    Adding reformat layer: Reformatted Input Tensor 0 to conv2/norm2 (conv2/3x3) from Half(75264,1:8,1344,24) to Half(301056,3136:2,56,1)
[TRT]    Adding reformat layer: Reformatted Output Tensor 0 to pool2/3x3_s2 (pool2/3x3_s2) from Half(75264,784:2,28,1) to Half(18816,1:8,672,24)
[TRT]    Adding reformat layer: Reformatted Output Tensor 0 to inception_4a/1x1 + inception_4a/relu_1x1 || inception_4a/3x3_reduce + inception_4a/relu_3x3_reduce || inception_4a/5x5_reduce + inception_4a/relu_5x5_reduce (inception_4a/1x1 + inception_4a/relu_1x1 || inception_4a/3x3_reduce + inception_4a/relu_3x3_reduce || inception_4a/5x5_reduce + inception_4a/relu_5x5_reduce) from Half(7448,1:8,532,38) to Half(29792,196:2,14,1)
...
```

<!-- markdownlint-restore -->

**Note**: _If you want to avoid that everytime you run the container, keep the networks folder outside the container and bind mount it (eg. in the `/data/code` path). That is, instead of doing `ln -s /usr/local/data/networks .` do a `cp -avf /usr/local/data/networks .`. Thus, every time you re-run the example using this folder, the auto-tuned engine will be there._

## Appendix I Build a jetson-inference container image

We only need this for `x86_64` Hosts, as for the `aarch64` case,
`nvidia-container-toolkit` is bound to the `l4t` distribution so running in a
container with different `cuda` and `cudnn`/`tensorrt` version is really
tricky.

The following Dockerfile includes the steps to setup and install the `jetson-inference` suite on an `x86_64` host:

```Dockerfile
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

### Install dependencies
RUN apt update && TZ=Etc/UTC apt install -y build-essential \
        git \
        cmake \
        python3 \
        python3-venv \
        libpython3-dev \
        python3-numpy \
        gcc-8 \
        g++-8 \
        lsb-release \
        wget \
        software-properties-common && \
        rm -rf /var/cache/apt/archives /var/lib/apt/lists && \
        update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 8 && \
        update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 8 && \
        update-alternatives --set gcc /usr/bin/gcc-8

RUN git clone https://github.com/dusty-nv/jetson-inference --recursive

### Install NVIDIA CUDA, CUDNN and TENSORRT
ARG OS=ubuntu2004
RUN wget http://developer.download.nvidia.com/compute/machine-learning/repos/${OS}/x86_64/nvidia-machine-learning-repo-${OS}_1.0.0-1_amd64.deb && \
        dpkg -i nvidia-machine-learning-repo-${OS}_1.0.0-1_amd64.deb && \
        apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/machine-learning/repos/${OS}/x86_64/7fa2af80.pub && \
        wget https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/cuda-${OS}.pin && \
        mv cuda-${OS}.pin /etc/apt/preferences.d/cuda-repository-pin-600 && \
        apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/3bf863cc.pub && \
        add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/ /" && \
        apt-get update && \
        apt-get install -y libcudnn8 libcudnn8-dev tensorrt nvidia-cuda-toolkit && \
        rm -rf /var/cache/apt/archives /var/lib/apt/lists


### Build jetson-inference and download models
RUN cd jetson-inference && \
        git checkout x86 && \
        git submodule update --init && \
        mkdir build && \
        cd build && \
        cmake ../ && \
        make -j$(nproc) install && \
        cd /jetson-inference/tools && \
        ./download-models.sh 0 && \
        cd / && cp -avf /jetson-inference/data /usr/local/data && \
        cp -avf /jetson-inference/utils/image/stb /usr/local/include && \
        rm -rf /jetson-inference
```

Essentially, the pain points are the following:

- Add custom NVIDIA repos for `cuda`, `cudnn` and `tensorrt`
- Use `gcc-8` as the default compiler

Other than that, the steps are straightforward. From the jetson-inference build
dir, we need to keep `data/networks` as it holds the models for inference. We
also keep `image/stb` include files for the building of the vAccelRT jetson
plugin.

Build using the following command:

```bash
docker build -t jetson-inference:x86_64 -f Dockerfile .
```

expect a lot of output, and about ~15' on a generic machine (6 cores, 16GB of RAM).

and run an example:

```console
# docker run --rm -it --gpus all  nubificus/jetson-inference-updated:x86_64 /bin/bash
root@f741113696a8:/# cd /usr/local/data/
root@f741113696a8:/usr/local/data# export LD_LIBRARY_PATH=/usr/local/lib/
root@f741113696a8:/usr/local/data# imagenet-console images/dog_0.jpg
[video]  created imageLoader from file:///usr/local/data/images/dog_0.jpg
------------------------------------------------
imageLoader video options:
------------------------------------------------
  -- URI: file:///usr/local/data/images/dog_0.jpg
     - protocol:  file
     - location:  images/dog_0.jpg
     - extension: jpg
  -- deviceType: file
  -- ioType:     input
  -- codec:      unknown
  -- width:      0
  -- height:     0
  -- frameRate:  0.000000
  -- bitRate:    0
  -- numBuffers: 4
  -- zeroCopy:   true
  -- flipMethod: none
  -- loop:       0
  -- rtspLatency 2000
------------------------------------------------
[video]  videoOptions -- failed to parse output resource URI (null)
[video]  videoOutput -- failed to parse command line options
imagenet:  failed to create output stream

imageNet -- loading classification network model from:
         -- prototxt     networks/googlenet.prototxt
         -- model        networks/bvlc_googlenet.caffemodel
         -- class_labels networks/ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.5.1
[TRT]    loading NVIDIA plugins...
[TRT]    Registered plugin creator - ::BatchedNMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::BatchedNMS_TRT version 1
[TRT]    Registered plugin creator - ::BatchTilePlugin_TRT version 1
[TRT]    Registered plugin creator - ::Clip_TRT version 1
[TRT]    Registered plugin creator - ::CoordConvAC version 1
[TRT]    Registered plugin creator - ::CropAndResizeDynamic version 1
[TRT]    Registered plugin creator - ::CropAndResize version 1
[TRT]    Registered plugin creator - ::DecodeBbox3DPlugin version 1
[TRT]    Registered plugin creator - ::DetectionLayer_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Explicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Implicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_ONNX_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_TRT version 1
[TRT]    Could not register plugin creator -  ::FlattenConcat_TRT version 1
[TRT]    Registered plugin creator - ::GenerateDetection_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchor_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchorRect_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 2
[TRT]    Registered plugin creator - ::LReLU_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelCropAndResize_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelProposeROI_TRT version 1
[TRT]    Registered plugin creator - ::MultiscaleDeformableAttnPlugin_TRT version 1
[TRT]    Registered plugin creator - ::NMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::NMS_TRT version 1
[TRT]    Registered plugin creator - ::Normalize_TRT version 1
[TRT]    Registered plugin creator - ::PillarScatterPlugin version 1
[TRT]    Registered plugin creator - ::PriorBox_TRT version 1
[TRT]    Registered plugin creator - ::ProposalDynamic version 1
[TRT]    Registered plugin creator - ::ProposalLayer_TRT version 1
[TRT]    Registered plugin creator - ::Proposal version 1
[TRT]    Registered plugin creator - ::PyramidROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::Region_TRT version 1
[TRT]    Registered plugin creator - ::Reorg_TRT version 1
[TRT]    Registered plugin creator - ::ResizeNearest_TRT version 1
[TRT]    Registered plugin creator - ::ROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::RPROI_TRT version 1
[TRT]    Registered plugin creator - ::ScatterND version 1
[TRT]    Registered plugin creator - ::SpecialSlice_TRT version 1
[TRT]    Registered plugin creator - ::Split version 1
[TRT]    Registered plugin creator - ::VoxelGeneratorPlugin version 1
[TRT]    detected model format - caffe  (extension '.caffemodel')
[TRT]    desired precision specified for GPU: FASTEST
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +298, GPU +0, now: CPU 321, GPU 223 (MiB)
[TRT]    Trying to load shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    Loaded shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    [MemUsageChange] Init builder kernel library: CPU +262, GPU +76, now: CPU 637, GPU 299 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]    native precisions detected for GPU:  FP32, FP16, INT8
[TRT]    selecting fastest native precision for GPU:  FP16
[TRT]    attempting to open engine cache file networks/bvlc_googlenet.caffemodel.1.1.8501.GPU.FP16.engine
[TRT]    loading network plan from engine cache... networks/bvlc_googlenet.caffemodel.1.1.8501.GPU.FP16.engine
[TRT]    device GPU, loaded networks/bvlc_googlenet.caffemodel
[TRT]    Loaded engine size: 15 MiB
[TRT]    Deserialization required 7510 microseconds.
[TRT]    [MemUsageChange] TensorRT-managed allocation in engine deserialization: CPU +0, GPU +13, now: CPU 0, GPU 13 (MiB)
[TRT]    Total per-runner device persistent memory is 94720
[TRT]    Total per-runner host persistent memory is 149472
[TRT]    Allocated activation device memory of size 3612672
[TRT]    [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +3, now: CPU 0, GPU 16 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       71
[TRT]       -- maxBatchSize 1
[TRT]       -- deviceMemory 3612672
[TRT]       -- bindings     2
[TRT]       binding 0
                -- index   0
                -- name    'data'
                -- type    FP32
                -- in/out  INPUT
                -- # dims  3
                -- dim #0  3
                -- dim #1  224
                -- dim #2  224
[TRT]       binding 1
                -- index   1
                -- name    'prob'
                -- type    FP32
                -- in/out  OUTPUT
                -- # dims  3
                -- dim #0  1000
                -- dim #1  1
                -- dim #2  1
[TRT]
[TRT]    binding to input 0 data  binding index:  0
[TRT]    binding to input 0 data  dims (b=1 c=3 h=224 w=224) size=602112
[TRT]    binding to output 0 prob  binding index:  1
[TRT]    binding to output 0 prob  dims (b=1 c=1000 h=1 w=1) size=4000
[TRT]
[TRT]    device GPU, networks/bvlc_googlenet.caffemodel initialized.
[TRT]    imageNet -- loaded 1000 class info entries
[TRT]    imageNet -- networks/bvlc_googlenet.caffemodel initialized.
[image]  loaded 'images/dog_0.jpg'  (500x375, 3 channels)
class 0248 - 0.230449  (Eskimo dog, husky)
class 0249 - 0.607152  (malamute, malemute, Alaskan malamute)
class 0250 - 0.158385  (Siberian husky)
imagenet:  60.71516% class #249 (malamute, malemute, Alaskan malamute)

[TRT]    ------------------------------------------------
[TRT]    Timing Report networks/bvlc_googlenet.caffemodel
[TRT]    ------------------------------------------------
[TRT]    Pre-Process   CPU   0.02392ms  CUDA   0.21290ms
[TRT]    Network       CPU   1.04193ms  CUDA   0.85664ms
[TRT]    Post-Process  CPU   0.02108ms  CUDA   0.02154ms
[TRT]    Total         CPU   1.08694ms  CUDA   1.09107ms
[TRT]    ------------------------------------------------

[TRT]    note -- when processing a single image, run 'sudo jetson_clocks' before
                to disable DVFS for more accurate profiling/timing measurements

[image]  imageLoader -- End of Stream (EOS) has been reached, stream has been closed
imagenet:  shutting down...
[TRT]    3: [engine.cpp::~Engine::307] Error Code 3: API Usage Error (Parameter check failed at: runtime/api/engine.cpp::~Engine::307, condition: mObjectCounter.use_count() == 1. Destroying an engine object before destroying objects it created leads to undefined behavior.
)
imagenet:  shutdown complete.
```
