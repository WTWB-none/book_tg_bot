#!/bin/bash

# Build script for Book Bot project
# This script builds the Vue webapp and prepares it for deployment

set -e

echo "🚀 Building Book Bot project..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "📦 Installing webapp dependencies..."
cd webapp
npm install

echo "🔨 Building Vue webapp..."
npm run build

echo "✅ Build completed successfully!"
echo "📁 Built files are in: webapp/dist/"
echo ""
echo "🚀 To run the bot:"
echo "   cd .. && python -m bot.main"
echo ""
echo "🌐 To serve the webapp in development:"
echo "   cd webapp && npm run dev"