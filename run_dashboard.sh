#!/bin/bash

# Add local bin to PATH
export PATH="/home/ubuntu/.local/bin:$PATH"

# Check if data files exist
if [[ ! -f "RFM_Clustered.csv" ]]; then
    echo "❌ Error: RFM_Clustered.csv not found!"
    exit 1
fi

if [[ ! -f "cleaned_data.csv" ]]; then
    echo "❌ Error: cleaned_data.csv not found!"
    exit 1
fi

echo "✅ Data files found"
echo "🚀 Starting Customer Segmentation Dashboard..."
echo "📊 Dashboard will be available at: http://localhost:8501"
echo "🌐 Or access via network at: http://YOUR_IP:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

# Run Streamlit dashboard
streamlit run dashboard.py \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.port 8501 \
    --server.address 0.0.0.0