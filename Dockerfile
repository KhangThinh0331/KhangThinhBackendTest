FROM node:18-bullseye

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y python3 python3-pip git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

RUN pip3 install --no-cache-dir -r python/requirements.txt

CMD ["node", "index.js"]
