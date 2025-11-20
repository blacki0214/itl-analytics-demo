# ITL Logistics Analytics Dashboard

A Streamlit-based predictive fleet maintenance dashboard for proactive fleet management and maintenance optimization.

## Overview

This application provides advanced analytics for fleet management, helping identify high-risk vehicles and optimize maintenance schedules. It features interactive visualizations, risk assessment algorithms, and real-time filtering capabilities to support data-driven decision-making in logistics operations.

## Features

### Key Performance Indicators
- Total vehicle count
- High-risk vehicle identification
- Average days since last service
- Total breakdown statistics (6-month period)

### Interactive Visualizations
- **Risk Analysis Bar Chart**: Top vehicles by days since last service, color-coded by risk level
- **Risk Distribution Pie Chart**: Fleet-wide risk level breakdown
- **Breakdown Rate Histogram**: Distribution of breakdown rates across the fleet
- **Depot-wise Analysis**: Stacked bar chart showing risk levels by depot location
- **Correlation Scatter Plot**: Engine hours vs. breakdowns with risk level indicators
- **Service Timeline**: Gantt-style visualization of vehicle service status
- **Box Plots**: Breakdown distribution analysis by depot
- **Violin Plots**: Engine hours distribution by risk level

### Advanced Features
- Real-time filtering by depot and risk level
- Vehicle ID search functionality
- Color-coded data tables for easy risk identification
- CSV export with filtered data
- Responsive design for various screen sizes

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/blacki0214/itl-analytics-demo.git
cd itl-analytics-demo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate sample fleet data:
```bash
python generate_fleet_data.py
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser and navigate to:
```
http://localhost:8501
```

## 🐳 Docker Deployment

Build and run using Docker:

```bash
# Build the image
docker build -t itl-analytics .

# Run the container
docker run -p 8501:8501 itl-analytics
```

Access the application at `http://localhost:8501`

## Data Schema

The fleet data includes the following fields:

| Field | Description |
|-------|-------------|
| `vehicle_id` | Unique vehicle identifier (e.g., T001) |
| `mileage_km` | Total kilometers driven |
| `engine_hours` | Total engine operating hours |
| `last_service_date` | Date of most recent service |
| `breakdowns_last_6m` | Number of breakdowns in last 6 months |
| `fuel_efficiency` | Fuel efficiency (L/100km) |
| `depot` | Assigned depot location |
| `days_since_service` | Calculated: days since last service |
| `breakdown_rate` | Calculated: breakdowns per engine hour |
| `risk_level` | Calculated: High/Medium/Low risk classification |

## Risk Assessment Logic

The application categorizes vehicles into risk levels based on:

- **High Risk**: 
  - Days since service > 90 days, OR
  - Breakdown rate > 0.002
- **Medium Risk**: 
  - Days since service > 60 days
- **Low Risk**: 
  - All other vehicles

## Project Structure

```
itl-analytics-demo/
├── app.py                      # Main Streamlit application
├── generate_fleet_data.py      # Data generation script
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── data/
│   └── fleet_data_large.csv   # Generated fleet data
├── docs/                       # Documentation (if any)
└── tests/
    └── test_data.py           # Unit tests
```

## Technologies Used

- **Streamlit** (1.38.0) - Web application framework
- **Pandas** (2.2.2) - Data manipulation and analysis
- **Plotly** (5.24.1) - Interactive visualizations
- **NumPy** (1.26.4) - Numerical computing
- **Faker** (25.3.0) - Synthetic data generation
- **Pytest** (8.3.3) - Testing framework

## Usage Guide

### Filtering Data
1. Use the sidebar to select a specific depot or view all depots
2. Filter by risk levels (High, Medium, Low) using the multi-select dropdown
3. Search for specific vehicles using the Vehicle ID search box

### Exporting Data
- Click the "📥 Download Filtered Data as CSV" button to export the currently filtered dataset
- The exported file will be named with the current date for easy tracking

### Analyzing Trends
- Navigate between tabs to view different analytical perspectives
- Hover over charts for detailed information
- Use the interactive visualizations to identify patterns and correlations

## Testing

Run the test suite:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is part of the SWE4006 course project.

## 👤 Author

**blacki0214**
- GitHub: [@blacki0214](https://github.com/blacki0214)

## 📧 Support

For questions or issues, please open an issue on the GitHub repository.

---

**ITL Logistics Analytics** 
