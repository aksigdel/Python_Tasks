# Python_Fusemachines

*master branch*

A brief run thorugh of python bascis.

*advpython branch*

Advance python topics pratice notebook.

*codewars branch*

Few of the Codewars problems solved. 5 Kyu reached with 253 points.

*api_flask branch*

created CRUD api for <https://jsonplaceholder.typicode.com/users> json data.


###### Endpoints

| Parameter | Type     | 
| :-------- | :------- | 
| `id`      | `int`    | 

```
  GET /api/users/<int:id>
```
    returns  name, address( street | suite | city), website based on user id.


```
  PUT /api/upper_users/<int:id>
```
    updates name and username to upper case based on user id and return updated data.


```
  DELETE /app/delete_users/<int:id>
```
    delete record and display response message based on user id.


```
  POST /api/insert_user
```
    insert new record and display response message along with inserted data.


```
  GET /api/city_count
```
    return  city count and status in JSON format.
