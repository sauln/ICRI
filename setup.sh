# Setup for ICRI repo
apt-get install python3-pip
pip3 install virtualenv
cd ICRI
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py

