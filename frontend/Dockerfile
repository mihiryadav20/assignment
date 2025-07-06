FROM node:20-slim

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy project files
COPY . .

# Build the app (uncomment for production build)
# RUN npm run build

# Expose port
EXPOSE 5173

# Command to run dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
