
cd ui 
yarn install
yarn build

cd ../compute/zeromq
source venv/bin/activate
pip install -r requirements.txt
deactivate

cd ../..

# TODO Navigation, localization scripts