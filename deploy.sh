#!/bin/bash

# LinkedIn Scraper Deployment Script
# Usage: ./deploy.sh [build|start|stop|restart|logs|clean]

set -e

PROJECT_NAME="linkedin-scraper"
COMPOSE_FILE="docker-compose.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}================================${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

print_info() {
    echo -e "${YELLOW}[INFO] $1${NC}"
}

# Check if docker-compose file exists
check_compose_file() {
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_error "File $COMPOSE_FILE tidak ditemukan!"
        exit 1
    fi
}

# Check if .env file exists
check_env_file() {
    if [ ! -f ".env" ]; then
        print_error "File .env tidak ditemukan!"
        print_info "Silakan copy .env.example ke .env dan isi LINKEDIN_LI_AT"
        exit 1
    fi
}

# Build image
build() {
    print_header "Building Docker Image"
    check_compose_file
    
    print_info "Building image (ini mungkin memakan waktu 10-15 menit)..."
    docker-compose build --no-cache
    
    print_success "Image berhasil di-build!"
}

# Start container
start() {
    print_header "Starting Container"
    check_compose_file
    check_env_file
    
    print_info "Starting container..."
    docker-compose up -d
    
    print_info "Waiting for container to be ready..."
    sleep 5
    
    if docker-compose ps | grep -q "Up"; then
        print_success "Container berhasil dijalankan!"
        print_info "Akses API di: http://localhost:8000/docs"
    else
        print_error "Container gagal dijalankan!"
        docker-compose logs
        exit 1
    fi
}

# Stop container
stop() {
    print_header "Stopping Container"
    check_compose_file
    
    print_info "Stopping container..."
    docker-compose down
    
    print_success "Container berhasil dihentikan!"
}

# Restart container
restart() {
    print_header "Restarting Container"
    check_compose_file
    check_env_file
    
    print_info "Restarting container..."
    docker-compose restart
    
    print_info "Waiting for container to be ready..."
    sleep 5
    
    print_success "Container berhasil di-restart!"
}

# View logs
logs() {
    print_header "Container Logs"
    check_compose_file
    
    docker-compose logs -f --tail=100
}

# Clean up
clean() {
    print_header "Cleaning Up"
    
    print_info "Stopping containers..."
    docker-compose down -v
    
    print_info "Removing unused Docker resources..."
    docker system prune -f
    
    print_success "Cleanup selesai!"
}

# Status
status() {
    print_header "Container Status"
    check_compose_file
    
    docker-compose ps
    
    print_header "Resource Usage"
    docker stats --no-stream $PROJECT_NAME || print_info "Container tidak sedang berjalan"
}

# Health check
health() {
    print_header "Health Check"
    
    if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
        print_success "API is healthy!"
    else
        print_error "API is not responding!"
        exit 1
    fi
}

# Main
case "${1:-help}" in
    build)
        build
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    clean)
        clean
        ;;
    status)
        status
        ;;
    health)
        health
        ;;
    *)
        print_header "LinkedIn Scraper Deployment Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  build      - Build Docker image"
        echo "  start      - Start container"
        echo "  stop       - Stop container"
        echo "  restart    - Restart container"
        echo "  logs       - View container logs"
        echo "  status     - Show container status"
        echo "  health     - Check API health"
        echo "  clean      - Clean up containers and images"
        echo ""
        echo "Examples:"
        echo "  $0 build"
        echo "  $0 start"
        echo "  $0 logs"
        echo ""
        ;;
esac
