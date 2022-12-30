cd ..
git clone git@github.com:mkorpela/RoboMachine.git robomachinerelease
cd robomachinerelease
python setup.py sdist
twine upload -r RoboMachine dist/*.*
