cd ..
git clone git@github.com:mkorpela/RoboMachine.git robomachinerelease
cd robomachinerelease
python setup.py sdist
sudo twine upload dist/*.*
