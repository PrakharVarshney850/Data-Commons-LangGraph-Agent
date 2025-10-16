# Use official Python image
FROM python:3.12-slim

# Install uv package manager (which includes uvx)
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy environment file
COPY .env .env

# Expose MCP server port
EXPOSE 8889

# Set environment variables from .env file
ENV DC_API_KEY=${DC_API_KEY}

# Run the Data Commons MCP server using uvx
CMD ["sh", "-c", "export $(cat .env | xargs) && uvx datacommons-mcp serve http --port 8889 --host 0.0.0.0"]
