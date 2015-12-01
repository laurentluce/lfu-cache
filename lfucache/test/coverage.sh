coverage run --source=$PYTHONPATH/lfucache --omit=$PYTHONPATH/lfucache/test/* all_tests.py
coverage report --omit=$PYTHONPATH/lfucache/test/* -m
