GPU-enabled GROMACS 2024.3 installation: follow steps 1, 2, 3, 4
CPU-enabled GROMACS 2024.3 installation: follow steps 1, 3, 4 

#### 1. **Install GCC 9** (compatible with CUDA 11.2) for GPU-enabled GROMACS 2024.3
```
sudo apt-get purge gcc-13 gcc-13-base gcc-13-x86-64-linux-gnu
sudo apt-get purge gcc-14 gcc-14-base gcc-14-x86-64-linux-gnu
sudo apt-get purge g++-13 g++-13-x86-64-linux-gnu
sudo apt-get purge gcc g++
sudo apt-get autoremove --purge

sudo apt-get install gcc-9 g++-9
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 9
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 9
sudo update-alternatives --config gcc
sudo update-alternatives --config g++
sudo apt-mark hold gcc-9 g++-9
```

Create or edit a file /etc/apt/preferences.d/gcc9-pin to pin GCC 9 and prevent upgrading:

`sudo vi /etc/apt/preferences.d/gcc9-pin`

Content:

```
Package: gcc-9 g++-9 libgcc-9-dev libstdc++-9-dev
Pin: version 9*
Pin-Priority: 1001
```

Check:

```
gcc --version
g++ --version
```

.
#### 2. **CUDA dependencies and installation:**
```
wget http://security.ubuntu.com/ubuntu/pool/universe/n/ncurses/libtinfo5_6.3-2ubuntu0.1_amd64.deb
sudo apt install ./libtinfo5_6.3-2ubuntu0.1_amd64.deb
sudo apt install cmake git doxygen libfftw3-dev libxml2-dev python3
```

- NVIDIA CUDA Toolkit installation for GPU-enabled GROMACS - Provide details of system type and follow the instructions on:
https://developer.nvidia.com/cuda-downloads

- GROMACS 2024 supports GCC compiler versions 9.x - 11.x. CUDA 13 forcibly installs GCC compiler version 13. Therefore, install CUDA 11.2 instead which supports GCC 9

- Choose to install using a runfile (local) :

```
wget https://developer.download.nvidia.com/compute/cuda/11.2.0/local_installers/cuda_11.2.0_460.27.04_linux.run
sudo sh cuda_11.2.0_460.27.04_linux.run
```

If choosing installation by local DEB file, replace last step of CUDA Toolkit installation with:

`sudo apt-get install --no-install-recommends cuda-runtime-11-2 cuda-libraries-11-2 cuda-cudart-dev-11-2`

Then:

`export PATH=$PATH:/usr/local/cuda-11.2/bin/`
`export LD_LIBRARY_PATH=/usr/local/cuda-11.2/lib64:$LD_LIBRARY_PATH`

.
#### 3. **GROMACS installation:**
Download: https://manual.gromacs.org/documentation/2024.3/download.html

```
tar xfz gromacs-2024.3.tar.gz
cd gromacs-2024.3
mkdir build && cd build

# To use GMX with GPU
cmake .. -DGMX_GPU=CUDA -DGMX_BUILD_OWN_FFTW=ON -DREGRESSIONTEST_DOWNLOAD=ON -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda #-DGMX_CUDA_TARGET_COMPUTE=12.0

# To use GMX with CPU
cmake .. -DGMX_BUILD_OWN_FFTW=ON -DREGRESSIONTEST_DOWNLOAD=ON 

make -j$(nproc)
make -j$(nproc) check # likely to give an error, but can proceed with next step anyway

sudo make -j$(nproc) install
source /usr/local/gromacs/bin/GMXRC
```

.
#### 4. **Add to ~/.bashrc**
```
export LD_LIBRARY_PATH=/usr/local/cuda-11.2/lib64:$LD_LIBRARY_PATH # for gpu use
export PATH=$PATH:/usr/local/cuda-11.2/bin/ # for gpu use
export PATH=$PATH:/usr/local/gromacs/bin
source /usr/local/gromacs/bin/GMXRC

```

.
#### Note to self:

- ``My laptop (ASUS ROG Strix G16, 16-Core AMD Ryzen 9 8940HX, GeForce RTX 5070 Ti) comes with CUDA compute capability = 12.0 (-DGMX_CUDA_TARGET_COMPUTE=12.0 during cmake). This level of CUDA's compute capability most likely requires the latest CUDA (v13.x as of Nov 2025) on WSL2. But I can only have CUDA v11.2 installed to ensure compatibility with GCC 9.x to 11.x (latest GCC: v13.x - Nov 2025). An older version of GCC (9.x to 11.x) is required to install GROMACS 2024.3 due to known issues with GCC 12+, as mentioned on installation page (https://manual.gromacs.org/documentation/2024.3/install-guide/index.html). 
- In summary: Gromacs installation recommends GCC 9.x to 11.x (I've installed v9.5) -> compatible with CUDA 11.2 -> CUDA 11.2 incompatible with laptop compute capability. Therefore, use Gromacs 2024.3 with only CPU.