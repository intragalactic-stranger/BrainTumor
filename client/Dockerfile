# Use the official Node.js image as the base image
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package.json package-lock.json ./

# Install the application dependencies
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]