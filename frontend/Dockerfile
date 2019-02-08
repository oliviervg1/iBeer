FROM node:11
WORKDIR /opt/ibeer
COPY package*.json ./
RUN npm install --only=production
COPY ./src ./
EXPOSE 8000
CMD ["nodejs", "server.js"]
