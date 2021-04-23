# TakaFlask
![alt text](https://i.imgur.com/eMpdPSu.png)
# Setup instructions
Install docker dashboard https://docs.docker.com/desktop/dashboard/
```
git clone https://github.com/randyfan/TakaFlask
```

# Initialize MySQL database
```
docker run --name some-mysql-taka -e MYSQL_ROOT_PASSWORD=my-secret-pw --network my-network -e MYSQL_DATABASE=demo -dit mysql:latest --default-authentication-plugin=mysql_native_password

winpty docker exec -it some-mysql-taka bash

mysql -uroot --password=my-secret-pw

show databases;

use demo;

CREATE TABLE takatable(
   this_id INT PRIMARY KEY,
   this_curr_cum_utterances VARCHAR(1000) NOT NULL
);

```

# Open new terminal and CD into Taka Flask directory
```
docker build -t taka .
docker run -dit --name=taka-container -e FLASK_APP=views.py -p 5000:5000 --network my-network taka
docker logs -f taka-container
```




Go to http://127.0.0.1:5000/

