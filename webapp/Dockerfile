# Use an official Node runtime as a parent image
FROM node:16

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./
# Alternatively, if you use Yarn, copy yarn.lock as well
# COPY package.json yarn.lock ./

# Install any dependencies
RUN npm install
# Or use yarn
# RUN yarn install

# Bundle app source inside Docker image
COPY . .

# Build your app
RUN npm run build

# Install serve to serve your app
RUN npm install -g serve

# Command to run your app
CMD ["serve", "-s", "build", "-l", "3000"]

# Expose the port the app runs on
EXPOSE 3000
