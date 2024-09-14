IOLander is a pygame written in python.

To run this file you will need to install python and pygame.

If you already have python installed then install pygame:

In case you don't have these libaries you can install them:
pip install pygame
pip install numpy

Clone these files to the folder of your choice (or download and unzip the archive):

git clone https://github.com/totorodad/iolander.git

Run the code in the iolander folder with python.

python main.py

Note that if you are playing on Linux on a Raspberry pi you may need to install the following dependeancy to support numpy:

sudo apt-get install libopenblas-dev

Also the files are windows binary files so you may want to remove the ^M at end of line on each line:
You can google how to do this but I run the REGEX in vi: <ESC>%s/<CTRL-V><CTRL-M>//g to clean them out
