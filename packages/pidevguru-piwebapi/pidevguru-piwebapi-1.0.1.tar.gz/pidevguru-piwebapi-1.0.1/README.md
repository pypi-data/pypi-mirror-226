PI Web API client for Python
===

## Overview
This repository has the source code package of the PI Web API client for Python. PI Web API 2018 swagger specification was used to create this package.


## Requirements

 - PI Web API 2018+ instance available on your domain or a public network.
 
## Installation
### pip install

If the python package is hosted on Github, you can install directly from Github


```sh
pip install pidevguru.piwebapi
```


### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```


## Documentation

All PI Web API server methods are mapped on this client. Please refer to [PI Web API help page](https://docs.aveva.com/bundle/pi-web-api-reference/page/help). 

## Examples

### Create an instance of the PI Web API top level object.

#### Basic Authentication
```python
    from pidevguru.piwebapi.pi_web_api_client import PIWebApiClient
    piwebapi = PIWebApiClient("https://webserver/piwebapi", useKerberos=False, username="username", password="password", verifySsl=true)  
``` 

#### Kerberos Authentication
```python
    from pidevguru.piwebapi.pi_web_api_client import PIWebApiClient
    piwebapi = PIWebApiClient("https://webserver/piwebapi", useKerberos=True, verifySsl=False)  
``` 

### Get the PI Data Archive WebId

```python
    dataServer = piwebapi.dataServer.get_by_path("\\\\PISRV1");
```

### Create a new PI Point

```python
    newPoint = PIPoint()
    newPoint.name  = "SINUSOID_TEST"
    newPoint.descriptor = "Test PI Point for Python PI Web API Client"
    newPoint.point_class = "classic"
    newPoint.point_type = "float32"
    newPoint.future = False
    res = piwebapi.dataServer.create_point_with_http_info(dataServer.web_id, newPoint);         
```

### Get PI Points WebIds

```python
    point1 = piwebapi.point.get_by_path("\\\\PISRV1\\sinusoid");
```


## Licensing
Copyright 2023 PIDevGuru.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
Please see the file named [LICENSE.md](LICENSE.md).