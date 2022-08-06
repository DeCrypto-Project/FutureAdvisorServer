# Welcome to my api flask app



## :globe_with_meridians: Overview

This is api service, base on python api-restfull, Dockerfile and swagger.



In the service the next routes:

* GET  /v1/api/checkCurrentWeather
* POST /v1/api/driveStatus
* GET  /v1/api/driveStatus?status=<drive_status>
* GET  /v1/api/consulCluster/systemInfo


### :electric_plug: Quickstart


1. clone the repositories 


2. navigate to this folder via terminal

```
cd /path...
```


```
docker build --tag <your tag> .
```


```
docker run --publish 5000:5010 <your tag>
```






### :electric_plug: access *** UI swagger*** at http://127.0.0.1:5000/swagger-ui/ in your local browser.



