#!/bin/bash
port=${PORT:-8501}
streamlit run app.py --server.port=$port --server.enableCORS=false
