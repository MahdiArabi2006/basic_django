FROM node:20 AS frontend-builder

WORKDIR /app

RUN npm config set registry https://mirror-npm.runflare.com

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build
	

FROM nginx:alpine

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=frontend-builder /app/dist /usr/share/nginx/html

