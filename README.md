# Estimate and Remove Background, and Tracking Objects from Video Stream

The code can be used for simple cases. For example, tracking objects on a conveyor.

### Build BGS Library from source

Now everything is ready to build BGS Library.

1. Download the source code:

```bash
cd work_dir
git clone --recursive https://github.com/andrewssobral/bgslibrary.git
```

2. Make `build` folder and navigate to it:

```bash
cd bgslibrary
mkdir build && cd build
```

3. Run CMake to configure the build. Don't forget to set `PYTHON_EXECUTABLE` to your virtual environment python.

```bash
cmake -D BGS_PYTHON_SUPPORT=ON\
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D PYTHON_EXECUTABLE=~/myenv/bin/python  ..
```

4. Check the output. Pay attention to the `Python library status` section. It should look similar to this:

```bash
-- Python library status:
--     executable: ~/env/bin/python
--     library: ~/.pyenv/versions/3.7.5/lib/libpython3.7m.so
--     include path: ~/.pyenv/versions/3.7.5/include/python3.7m
```


Make sure, that your python library is build as a shared library (.so file), not as a static (.a file). That might cause
an error if you are using [pyenv](https://github.com/pyenv/pyenv), that builds python library as a static library by
default. 

5. Build the BGS Library:

```bash
make -j4
sudo make install
sudo ldconfig
```
Then copy installed package to your virtual enviroment.
```bash
cp /usr/local/lib/python3.8/site-packages/pybgs.cpython-38-x86_64-linux-gnu.so /home/ericchen/myenv/lib/python3.8/site-packages/
```

6. Make sure, you didn't get any errors. You can check, that everything is working by running the demo script:

```bash
cd ..
python3 demo.py
```

### Install Dependencies

1. Setup up python virtual environment (Suggested). Follow this [link](https://linuxize.com/post/how-to-create-python-virtual-environments-on-ubuntu-18-04/) to set up and activate your virtual env.
2. Install python dependencies in your virtual env:
   
   `pip install -r requirements.txt`

### How to run
1. Estimating background from video file or camera stream
```bash
python app/utils/background.py --video video.mp4 --n_frames 25
```

2. Get foreground mask, run the following script:
```bash
python app/utils/foreground.py
```

3. Run the centroid tracker:
```bash
python app/centroid_tracking.py --video video.mp4 --n_frames 25
```

4. Run OpenCV trackers:
```bash
python app/cv_tracking.py --video video.mp4 --n_frames 25 --tracker KCF
```

5. Run unit tests:
```bash
python -m pytest
```
