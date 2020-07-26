# backend

> A Python Flask project

## Prerequisites

* python3
* virtualenv

``` bash
$ pip install virtualenv
$ virtualenv --no-site-packages venv -p python3
# source venv/Scripts/activate
$ source venv/bin/activate
# deactivate
```

``` bash
$ source venv/bin/activate
$ pip install numpy==1.17.0
$ pip install PyMySQL==0.9.3
$ pip install SQLAlchemy==1.3.5
$ pip install scipy==1.3.0
$ pip install scikit-learn==0.21.3
$ pip install Flask==1.0.3
$ pip install Flask-Cors==3.0.8
```

## Build Setup

#### Example 1: Create DataBase from original test result (No DataBase exists)

backend/build_database.py
```python
if __name__ == '__main__':
    init_db()
    test_result_rootdir = '../../../data/emon_result'
    load_data_from_rootdir(test_result_rootdir)
    update_tb_config()
```

```bash
$ source venv/bin/activate
$ cd backend
$ python build_database.py                   #create 'data.db'
$ python views.py                            #run
```

#### Example 2: Use the existed DataBase ('data.db' exists)

```bash
$ source venv/bin/activate
$ cd backend
$ python views.py
```
