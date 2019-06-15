Steps To Get This App Working : <br /> <br />

1 - Make sure you have the following items installed on your machine : <br />
    php 7, laravel 5, composer, elasticsearch 6, php-curl, memcached, php-memcached, redis-server <br /> <br />

2 - Clone the project.<br />
3 - Run composer update in your terminal.<br />
4 - Create a mysql database on your machine with the following configurations :<br />
    user : seller<br />
    password : seller<br />
    database : showcase<br />
    grant all accesses for showcase database to seller user<br /><br />
    
5 - Make sure mysql and elasticsearch services are on.<br />
6 - Run php artisan migrate --seed in your terminal.<br />
7 - Enter localhost:8000/api/ui in your favorite browser and enjoy.<br />
