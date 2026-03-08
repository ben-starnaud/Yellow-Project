# Use the slim version of Node 20 for a smaller, faster image
FROM node:20-slim

# Install Quasar CLI globally so we can use the 'quasar' command
RUN npm install -g @quasar/cli

# Create the app directory
WORKDIR /app

# Copy only the dependency files first
# This allows Docker to cache your 'npm install' layer
COPY package*.json ./

# Install dependencies
# We use --ignore-scripts to prevent 'quasar prepare' from running 
# before we have copied our source code.
RUN npm install --ignore-scripts

# Now copy the rest of your project files (src, quasar.config.js, etc.)
COPY . .

# Expose the port Quasar uses for development
EXPOSE 9000

# Start the dev server
# --host 0.0.0.0 is required so you can access it from your laptop's browser
CMD ["quasar", "dev", "-m", "spa", "--host", "0.0.0.0"]