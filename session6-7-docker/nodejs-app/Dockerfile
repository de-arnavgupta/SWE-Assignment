FROM node:20-alpine
WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev

COPY . .

# Non-root user execution
USER node
EXPOSE 3000

CMD ["node", "server.js"]
