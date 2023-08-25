from setuptools import setup


long_desc = """# TrifectaDB - Multiplatform, Multilanguage Support, Lightweight Database

TrifectaDB is a lightweight and versatile database system that combines the power of SQL, NoSQL, and a storage system, making it a comprehensive solution for a wide range of data storage and retrieval needs. This database is designed to provide developers with a flexible and efficient platform for managing structured and unstructured data across various platforms and programming languages. TrifectaDB is available, empowering developers with an accessible and powerful database solution that doesn't weigh down your applications.

## Features

- **Lightweight:** TrifectaDB is designed with a focus on efficiency and minimal resource consumption, making it an excellent choice for applications where a lightweight database solution is crucial.

- **Multiplatform:** TrifectaDB works seamlessly across multiple platforms, including Windows, macOS, Linux, and more. This ensures that your applications can run on different operating systems without any compatibility issues.

- **Multilanguage Support:** With support for a variety of programming languages such as Python, Java, C#, JavaScript, and more, TrifectaDB makes it easy to integrate and interact with your database using the language of your choice.

- **SQL Capabilities:** TrifectaDB offers robust SQL capabilities, enabling you to define schemas, create relational structures, and perform complex queries for structured data.

- **NoSQL Flexibility:** For unstructured or semi-structured data, TrifectaDB provides NoSQL capabilities, allowing you to store, retrieve, and manipulate data without the constraints of a rigid schema.

- **Storage System Integration:** TrifectaDB includes a storage system that facilitates efficient management of large-scale data, making it an ideal choice for applications that require high-performance storage and retrieval.

## Use Cases

TrifectaDB's lightweight nature and versatility make it suitable for a wide range of use cases, including but not limited to:

1. **Web Applications:** TrifectaDB can serve as the backend database for lightweight web applications, handling both structured user data (user profiles, settings, etc.) and unstructured data (user-generated content, images, files).

2. **E-Commerce:** Manage product catalog information, user shopping carts, order history, and customer reviews using TrifectaDB's relational and NoSQL features.

3. **Data Warehousing:** Utilize TrifectaDB's storage system for efficient storage and retrieval of moderate-sized datasets in data warehousing applications, where a lightweight footprint is important.

4. **Internet of Things (IoT):** Store sensor data, device information, and real-time telemetry data using TrifectaDB's flexible schema design and NoSQL capabilities.

5. **Content Management Systems (CMS):** TrifectaDB can store both structured content metadata and unstructured media files, making it a versatile choice for lightweight CMS platforms.

6. **Analytics and Reporting:** Leverage TrifectaDB to store and analyze data for generating insightful reports and visualizations, benefiting from both SQL querying and NoSQL document storage.

## Getting Started

To get started with TrifectaDB, please refer to the official documentation availabe in the software for installation instructions, API reference, and code samples in various programming languages.

## Contributing

We welcome contributions from the open-source community. If you're interested in improving TrifectaDB or adding new features, please check out our [contributing guidelines](CONTRIBUTING.md).

## License

TrifectaDB is released under the [GNU LPGL License](LICENSE).

## Downloads:

As TrifectaDB is in Alpha phase, we allow only specific users to use. If you want to use it, you can [contact us](mailto:dev.i7apps@gmail.com)


**Full Changelog**: https://github.com/Ojas1024/i7api/commits/v0.0.1


# Examples

Though, this library is **multi-language supported**, this is a minimal example of the use cases using python **requests**.

Any language, supporting HTTP requests can be used for API purposes


## Table of contents

* [Pre-requisites](#Pre-requisites)
* [Authentication Operations](#Authentication-Operations)
* [Tree Operations](#Tree-Operations)
  * [Branch Operations](#Branch-Operations)
  * [Leaf Operations](#Leaf-Operations)
  * [Fruit Operations](#Fruit-Operations)
  * [Flower Operations](#Flower-Operations)

## Pre-requisites

Installation of [python](https://www.python.org/downloads/)

After installation, you can install **requests** via ```pip install requests```

## Authentication Operations

1. Signup
```python
import requests

data = {"email":"someone@example.com", "password": "someRandomPass123"}
r = requests.post("localhost:2728/signup", json=data)

print(r.json())
```
Returns ```{"svid": ..., "password": ...}``` or ```{"error": ...}```


<br>

2. Signin

```python
import requests

data = {"email":"someone@example.com", "password": "someRandomPass123"}
r = requests.post("localhost:2728/signin", json=data)

print(r.json())
```
Returns ```{"svid": ..., "password": ...}``` or ```{"error": ...}```

<br><br>

## Tree Operations

### Branch Operations

1. Plant Tree

Before Working on the tree, you must plant a tree, by _Tree Name_ and _Tree Password_ in following way:

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ..., "type":"plant_tree","tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true"}``` or ```{"error": ...}```

This request plants a tree in your main garden.

_Make sure to wait for atleast 1 minute for the completion of resource provision_


<br>

2. Tree

_Lists all the branches, fruits, flowers in branch ```path``` (optional)_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ...,"tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"tree", "path":"/some/branch/path/"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true", "content": [...list of all the branches, fruits, flowers...]}``` or ```{"error": ...}```

<br>

3. Add Branch

_Adds a (sub) branch in branch ```path``` (optional) with branch name as ```branch```(required)_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ..., "tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"add_branch", "path":"/some/branch/path/", "branch":"branch_name"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true"}``` or ```{"error": ...}```

<br>

4. Remove Branch

_Removes a (sub) branch which is located in branch```path``` (optional) with branch name as ```branch```(required)_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ...,"tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"remove_branch", "path":"/some/branch/path/", "branch":"branch_name"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true"}``` or ```{"error": ...}```

<br>



### Leaf Operations
A leaf is the end entity which stores data.
<br>
Maximum size of a leaf is 9*1024 kilobytes
<br>

1. Add Leaf

_Adds a leaf in branch```path``` (optional) with leaf name as ```leaf```(required) with ```data```_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ...,"tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"add_leaf", "path":"/some/branch/path/", "leaf":"leaf_name", "data": "some-data"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true"}``` or ```{"error": ...}```

<br>
2. Remove Leaf

_Removes a leaf in branch```path``` (optional) with leaf name as ```leaf```(required)_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ...,"tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"remove_leaf", "path":"/some/branch/path/", "leaf":"leaf_name"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true"}``` or ```{"error": ...}```

<br>

3. Get Leaf data

_Retrieves the data of leaf in branch```path``` (optional) with leaf name as ```leaf```(required)_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ...,"tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"get_leaf", "path":"/some/branch/path/", "leaf":"leaf_name"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true", "content": "...leaf content..."}``` or ```{"error": ...}```

<br>


### Fruit Operations
A fruit is an end entity, which is SQL in type. 
<br>
Maximum number of fruits in a tree is: 400
<br>

1. Add Fruit

_Adds a fruit in branch```path``` (optional) with fruit name as ```fruit```(required)_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ...,"tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"add_fruit", "path":"/some/branch/path/", "fruit": "FRUIT NAME"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true"}``` or ```{"error": ...}```

<br>
2. Execute Query

_Executes a SQL ```query```(required) in fruit name ```fruit```(required) stored in branch```path``` (optional)_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ...,"tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"execute_query", "path":"/some/branch/path/", "fruit": "FRUIT NAME", "query": "SELCT * FROM ..."}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
<br>

### Flower Operations

A flower is an end entity, which can store **blob** data in base64 type
<br>Maximum size is 1.5 GB
<br>

1. Add Flower

_Adds a flower in branch```path``` (optional) with flower name as ```flower```(required) with ```b64``` data(required)_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ...,"tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"add_flower", "path":"/some/branch/path/", "flower":"FLOWER NAME", "b64": "BASE 64 DATA"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true"}``` or ```{"error": ...}```

<br>
2. Remove Flower

_Removes a flower in branch```path``` (optional) with flower name as ```flower```(required)_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ...,"tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"remove_flower", "path":"/some/branch/path/", "flower":"FLOWER NAME"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true"}``` or ```{"error": ...}```

<br>

3. Download flower

_Downloads the data of flower which is stored in branch```path``` (optional) with flower name as ```flower```(required)_

```python
import requests

# Authentication parameters svid and password are MUST
data = {"svid": ..., "password": ...,"tree_name": "YOUR TREE NAME", "tree_password": "YOUR TREE PASSWORD", "type":"download_flower", "path":"/some/branch/path/", "flower":"FLOWER NAME"}
r = requests.post("localhost:2728/tree", json=data)

print(r.json())
```
Returns ```{"success":"true", "b64": "...BASE 64 STRING..."}``` or ```{"error": ...}```

<br>


## Try Them
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Ojas1024/i7api/)

"""


setup(
    name='trifectadb',
    version='3.0',
    description="""TrifectaDB - A Multiplatform, Multilanguage Database Solution
""",
    author='Ojas Gupta',
    author_email='dev.i7apps@gmail.com',
    packages=['trifectadb'],
    long_description=long_desc,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests"
    ],
)
