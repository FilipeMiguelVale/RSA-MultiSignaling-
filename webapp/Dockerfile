# Use an official Node.js runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
RUN mkdir /app && chown node:node /app
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./
# Alternatively, if you use Yarn, copy yarn.lock as well
# COPY package.json yarn.lock ./
USER node
COPY --chown=node:node package.json package-lock.json* ./
# Install any dependencies, including those necessary for building the app
RUN npm install
# Or use yarn
# RUN yarn install

# Copy the rest of your application's code
COPY --chown=node:node . .

# Build your React app
RUN npm run build

COPY --chown=node:node . .

# Serve the application using serve package for demonstration purposes
# For production, consider using Nginx or another web server
#RUN npm install -g serve
#CMD ["serve", "-s", "build", "-l", "3000"]
CMD ["npm", "start"]
# Expose the port the app runs on
EXPOSE 3000
