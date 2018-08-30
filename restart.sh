echo `sudo cp -f /srv/intra_crawling/.config/nginx/wgp.conf /etc/nginx/sites-available/wgp.conf`
echo `sudo ln -f /srv/intra_crawling//.config/uwsgi/uwsgi.service /etc/systemd/system/uwsgi.service`
echo `sudo systemctl daemon-reload`
echo `sudo systemctl restart nginx uwsgi`
