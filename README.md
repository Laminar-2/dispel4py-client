# Client Instructions 

The following instructions will allow you to run the client application to run dispel4py workflows 

Clone repository 
```
git clone https://github.com/dispel4pyserverless/dispel4py-client.git
```
Then enter directory by 
```
cd dispel4py-client
```
Download the dispel4py.tar file into directory (If you have already created a conda enviroment then `conda activate py37` and skip to `Test dispel4py`)
```
https://drive.google.com/file/d/1rvgJSkCdiK-yEzmnHsw_RkW8B1dBewa5/view
```
In order to run the application you need to creatre a new Python 3.7 enviroment 
```
--note conda must be installed beforehand, go to https://conda.io/projects/conda/en/stable/user-guide/install/linux.html
conda create --name py37 python=3.7
conda activate py37
```
Install dispel4py 
```
tar -zxvf dispel4py.tar
cd dispel4py
python setup.py install
cp ../requirements_d4py.txt .
pip install -r requirements_d4py.txt
cd ..
```
Test dispel4py 
```
dispel4py simple dispel4py.examples.graph_testing.word_count -i 10
```
Install client modules
```
pip install requirements_client.txt
```
Run test client 
```
python CLIENT_EXAMPLES\<file>
```





