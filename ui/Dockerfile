FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM httpd:2.4-alpine
RUN rm -rf /usr/local/apache2/htdocs/*
COPY --from:build-stage /app/dist /usr/local/apache2/htdocs/

EXPOSE 80