# This is the node image on a debian base
FROM node:22-slim

# Set working directory
WORKDIR /app

# Install deps first to cache them unless package.json changes
COPY package*.json ./
RUN npm install

# Copy the rest of the project files
COPY . .

# Expose Vite default port
EXPOSE 5173

# Default command
# -- --host ensures that the port is available outside the container
CMD ["npm", "run", "dev", "--", "--host"]