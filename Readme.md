## SETUP ON SERVER(UBUNTU)

1. Update the server and install python dependencies
    ```shell
    sudo apt update
    ```
   (Note if you are on windows, download python from python.org)

   (On Mac you can install python with https://docs.python-guide.org/starting/install3/osx/)

    ```shell
    sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
    ```


2. Install Virtual Environment

   ```shell
   sudo apt-get install -y python3-venv
   ```

3. Navigate inside the project directory

   ```shell
   cd op_gg_scraper_api
   ```

4. Create the virtual environment
   ```shell
   python3 -m venv .env
   ```

5. Activate virtual environment and install requirements
   ```shell
   source .env/bin/activate
   ```

   ```shell
   pip install -r requirements.txt
   ```

6. Test the script with
   ```shell
   python wsgi.py
   ```

For deployment to server,

Please refer to https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

Here are the predone config file that can be used directly by modifying username

(refer to above dreployment instruction in digital ocean, the files below are just so thaat it will speed up deployment for you)

##### SYSTEMD

```shell
#/etc/systemd/system/op_gg.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
Environment="APP_ENV=PRD"
WorkingDirectory=/home/ubuntu/op_gg_scraper_api
ExecStart=/home/ubuntu/op_gg_scraper_api/.env/bin/gunicorn --access-logfile /home/ubuntu/logs/gunicorn-website-access.log --error-logfile /home/ubuntu/logs/gunicorn-website-error.log   --workers 6 --bind unix:/home/ubuntu/op_gg_scraper_api/op_gg_scraper_api.sock  -m 007 wsgi:application --timeout 20


[Install]
WantedBy=multi-user.target


```

##### NGINX

(You need to change the server IP)

```shell
#/etc/nginx/sites-available/op_gg


server {
    listen 80;
    server_name 18.183.56.10;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/op_gg_scraper_api/op_gg_scraper_api.sock;
    }
}



```