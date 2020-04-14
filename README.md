
# ![logo](meteor.png) Meterite - keep your metrics

A simple microservice to keep pushing in metrics into a timeseries database.

**Why?**

* Needed something for tracking various hourly/weekly/daily etc numbers
* Wanted to write a fun learning project to use [fastapi](https://fastapi.tiangolo.com/).
  Many of the examples online I saw didn't have code explaining master-detail
  schema and usage of async db apis in one project. 
* I wanted to do a useful web-api swith `sqlite`, preferably async.
* Straight-forward to run and debug! Can be put into docker if needed.

**What is with this name**? 

It is an abbreviation of *Meter* + *Write* and not a spelling mistake for
*meteorite*.

## Design

* Metric has a code, name some limits and belongs to an org
* Org is identified by a authentication key. Note that keys and orgs are only
  in config and not manageable by APIs.
rendered by mrindoc is a good place to start
* Meters are recorded to a Metric.

[API Spec](https://mrin9.github.io/OpenAPI-Viewer/#/load/https%3A%2F%2Fraw.githubusercontent.com%2Fvsbabu%2Fmeterite%2Fmaster%2Fopenapi.json)

Best way to peruse those is to clone repo and deploy this and test it with auto generated docs.

## Setup

```sh
conda create -n py82 python=3.8.2
conda activate py82
pip install -r requirements.txt
```

## API

Create a settings file named `.env` in this folder. Sample contents
are below.

```
database_url="sqlite:////tmp/meterite.db"
api_key_name="x-auth-token"
cookie_domain="localtest.me"
api_tokens={"123456": "org_01", "567890": "org_02"}
```

Then, start uvicorn as below.
```sh
uvicorn app.main:app --reload
``` 

And now navigate to http://localtest.me:8000/docs?x-auth-token=123456

An *org* is a group of metrics; think of it like a company in a multi-tenanted
design. You can have multiple auth tokens pointing to same org (if you fancy).

You can load sample data by running
```sh
scripts/load_sample.sh
```


## TODO

* [ ] Raise events or background tasks when meters are recorded with values outside of
      min/max settings. We should've some mechanism to plugin handlers outside
      the repo to this.
* [ ] Add separate background tasks to mark readings as anomalies; [fbprophet](https://facebook.github.io/prophet/) is pretty neet for that.
* [ ] Provide a UI for configuration. Seriously? No!
* [ ] Setup with gunicorn as well.

## Thanks

<div>Icon made by <a href="https://www.flaticon.com/authors/nikita-golubev" title="Nikita Golubev">Nikita Golubev</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
