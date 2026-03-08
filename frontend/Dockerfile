# Use the slim version of Node 20 
FROM node:20-slim

# Install Quasar CLI globally 
RUN npm install -g @quasar/cli

# Create the app directory
WORKDIR /app

COPY package*.json ./

# Install dependencies
RUN npm install --ignore-scripts

COPY . .

# Expose the port Quasar uses for development
EXPOSE 9000

# Start the dev server
CMD ["quasar", "dev", "-m", "spa", "--host", "0.0.0.0"]