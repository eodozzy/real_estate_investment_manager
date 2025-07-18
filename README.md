# Real Estate Investment Management System

A comprehensive desktop application for real estate investment analysis and portfolio management built with Python and PyQt6.

## Overview

This system enables tracking properties for purchase analysis, rental comparisons, and portfolio performance monitoring with both list and map views. Features include Four Pillars Total Return Analysis, interactive mapping, rental comparable analysis, and comprehensive portfolio management.

## Key Features

- **Property Analysis**: Track properties in analysis pipeline with investment calculations
- **Four Pillars Analysis**: Cash Flow, Principal Paydown, Appreciation, and Tax Benefits
- **Interactive Maps**: Folium-based mapping with property markers and filtering
- **Rental Comparables**: Market analysis with proximity-based filtering
- **Portfolio Management**: Performance tracking for owned properties
- **Data Import/Export**: Excel/CSV bulk operations with validation

## Technology Stack

- **Framework**: PyQt6/PySide6 (Desktop GUI)
- **Database**: SQLite (single-file, zero-configuration)
- **Mapping**: Folium + QtWebEngineWidgets
- **Data Processing**: Pandas, NumPy
- **File Handling**: openpyxl (Excel), csv (CSV imports)

## Project Structure

```
real_estate_investment_manager/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── main.py                            # Application entry point
├── real_estate_app/                   # Main application package
│   ├── __init__.py
│   ├── database/                      # Database models and connections
│   ├── gui/                          # User interface components
│   ├── analytics/                    # Financial calculations
│   ├── data/                         # Import/export handlers
│   └── config/                       # Application configuration
├── tests/                            # Test suite
├── docs/                             # Project documentation
│   ├── technical_specifications.md   # Detailed technical specifications
│   ├── development_plan.md          # Phase-by-phase development plan
│   ├── requirements_traceability_matrix.md # Requirements tracking
│   └── user_guide.md                # End-user documentation
├── assets/                           # Icons, templates, etc.
└── data/                            # Sample data and templates
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application**
   ```bash
   python main.py
   ```

## Documentation

- [Technical Specifications](docs/technical_specifications.md) - Detailed system architecture and requirements
- [Development Plan](docs/development_plan.md) - Phase-by-phase implementation guide  
- [Requirements Matrix](docs/requirements_traceability_matrix.md) - Requirements tracking and testing
- [User Guide](docs/user_guide.md) - End-user documentation (coming soon)

## Development Status

This project is currently in **Phase 1: Core Foundation** development.

See [Development Plan](docs/development_plan.md) for detailed progress tracking and milestones.

## Contributing

This is a personal project developed using Claude Code for iterative development assistance.

## License

Private project - All rights reserved.
