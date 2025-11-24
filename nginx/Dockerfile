FROM nginx:alpine

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./featurehub.conf /etc/nginx/conf.d/featurehub.conf

COPY ./front/index.html /var/www/featurehub/index.html
COPY ./front/static /var/www/featurehub/static

EXPOSE 80