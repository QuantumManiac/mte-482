
cd ui/ 
yarn install
yarn build

cd ..

cd compute/zeromq/
source venv/bin/activate
pip install -r requirements.txt
deactivate

cd ../..

cd localization/
source venv/bin/activate
pip install -r requirements.txt
deactivate

cd ..

cd navigation/
source venv/bin/activate
pip install -r requirements.txt
deactivate

cd ..
