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
In order to run the application you need to create a new Python 3.10 enviroment 
```
--note conda must be installed beforehand, go to https://conda.io/projects/conda/en/stable/user-guide/install/linux.html
conda create --name py10 python=3.10
conda activate py10
```
Install dispel4py 
```
git clone https://github.com/dispel4py2-0/dispel4py.git
cd dispel4py
pip install -r requirements.txt
python setup.py install
cd ..
```
Test dispel4py 
```
dispel4py simple dispel4py.examples.graph_testing.word_count -i 10
```
Install client modules
```
pip install -r requirements_client.txt
```
Run test client 
```
python CLIENT_EXAMPLES\<file>
```





