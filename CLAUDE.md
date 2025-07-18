# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive desktop application for real estate investment analysis and portfolio management built with Python and PyQt6. The system enables tracking properties for purchase analysis, rental comparisons, and portfolio performance monitoring with both list and map views.

## Technology Stack

- **Framework**: PyQt6/PySide6 (Desktop GUI)
- **Database**: SQLite (single-file, zero-configuration)
- **Mapping**: Folium + QtWebEngineWidgets
- **Data Processing**: Pandas, NumPy
- **File Handling**: openpyxl (Excel), csv (CSV imports)

## Development Commands

Based on the project documentation, the following commands are expected:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Testing (framework to be determined during development)
# Will be updated once test framework is chosen
```

## Project Structure

```
real_estate_investment_manager/
├── main.py                         # Application entry point
├── requirements.txt                # Python dependencies
├── real_estate_app/               # Main application package
│   ├── database/                  # Database models and connections
│   ├── gui/                       # User interface components
│   │   ├── property_analysis/     # Property analysis module
│   │   ├── rental_comps/          # Rental comparables module
│   │   ├── portfolio/             # Portfolio management module
│   │   ├── maps/                  # Map visualization component
│   │   └── shared/                # Reusable UI components
│   ├── analytics/                 # Financial calculations
│   ├── data/                      # Import/export handlers
│   └── config/                    # Application configuration
├── tests/                         # Test suite
├── docs/                          # Project documentation
├── assets/                        # Icons, templates, etc.
└── data/                          # Sample data and templates
```

## Core Architecture

### Database Schema
The application uses SQLite with the following main tables:
- `properties` - Main property information
- `price_history` - Property price tracking
- `property_photos` - Photo management
- `rental_comps` - Rental comparables
- `portfolio_performance` - Performance tracking for owned properties
- `investment_analysis` - Financial analysis data
- `four_pillars_analysis` - Comprehensive return analysis
- `property_valuations` - Property valuation history
- `regions` - Geographic regions for filtering

### Key Modules

1. **Property Analysis Module** (`gui/property_analysis/`): Main property tracking with investment calculations and Four Pillars Total Return Analysis
2. **Rental Comparables Module** (`gui/rental_comps/`): Market analysis with proximity-based filtering
3. **Portfolio Management Module** (`gui/portfolio/`): Performance tracking for owned properties
4. **Map Visualization Module** (`gui/maps/`): Interactive Folium-based mapping
5. **Analytics Module** (`analytics/`): Financial calculations and market analysis
6. **Data Import/Export Module** (`data/`): Bulk data operations with Excel/CSV

### Financial Calculations

The system implements comprehensive investment analysis including:
- **Four Pillars Total Return Analysis**:
  - Pillar 1: Cash Flow (rental income - expenses - debt service)
  - Pillar 2: Principal Paydown (annual mortgage principal reduction)
  - Pillar 3: Appreciation (annual property value increase)
  - Pillar 4: Tax Benefits (depreciation + interest + expense deductions)
- Cap Rate calculations
- Cash-on-Cash return
- Mortgage payment calculations with amortization
- Market trend analysis

## Development Status

Currently in **Phase 1: Core Foundation** development. The codebase structure is planned but implementation is just beginning. Future development will follow the phased approach outlined in the development plan.

## Key Implementation Notes

- Use QtWebEngineView to render Folium HTML for interactive maps
- Implement Four Pillars analysis as a key differentiator
- SQLite database path defaults to "real_estate.db"
- Photo storage uses local filesystem with database paths
- Import templates should include validation for required fields (address, city, state)
- Default settings include 27.5 years for residential depreciation
- Map integration requires careful handling of PyQt6 and Folium interaction

## Configuration

Default settings are managed in `config/settings.py` and include:
- Database configuration
- Financial calculation defaults (interest rates, loan terms)
- Map settings and tile layers
- Import validation rules
- Photo storage settings