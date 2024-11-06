# Stage 1: Build the React application
FROM node:18 AS build
 
# Set the working directory for the React app
WORKDIR /app/frontend
 
# Copy the React app's package.json and package-lock.json
COPY client/package.json client/package-lock.json ./
 
# Install the React app dependencies
RUN npm install
 
# Copy the rest of the React app's source code
COPY client/ ./
 
# Build the React application
RUN npm run build
 
# Stage 2: Setup FastAPI with the built React app
FROM python:3.12 AS production
 
# Set the working directory for the FastAPI app
WORKDIR /app/backend    
 
# Copy the FastAPI requirements and install them
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy FastAPI code
COPY server/ ./
 
# Copy the built React app from the previous stage
COPY --from=build /app/frontend/build ./build

# Expose the port that FastAPI runs on
EXPOSE 8000
 
# Command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "main_server:app", "--host", "0.0.0.0", "--port", "8000"]