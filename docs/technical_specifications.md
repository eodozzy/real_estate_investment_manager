# Real Estate Investment Management System
## Technical Specifications for Claude Code

### System Overview
A comprehensive desktop application for real estate investment analysis and portfolio management. The system enables tracking properties for purchase analysis, rental comparisons, and portfolio performance monitoring with both list and map views.

---

## Core Technology Stack

**Primary Framework:** PyQt6/PySide6 (Python desktop GUI)
**Database:** SQLite (single-file, zero-configuration)
**Mapping:** Folium + QtWebEngineWidgets (interactive maps in PyQt)
**Data Processing:** Pandas, NumPy
**File Handling:** openpyxl (Excel), csv (CSV imports)
**Image Storage:** Local filesystem with database paths

---

## Database Schema

### Properties Table (Main)
```sql
CREATE TABLE properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    latitude REAL,
    longitude REAL,
    bedrooms INTEGER,
    bathrooms REAL,
    square_footage INTEGER,
    lot_size REAL,
    year_built INTEGER,
    property_type TEXT DEFAULT 'Single Family',
    status TEXT DEFAULT 'analyzing', -- 'analyzing', 'under_contract', 'owned'
    notes TEXT,
    source_url TEXT, -- Link back to Zillow/original source
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Price History Table
```sql
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER REFERENCES properties(id),
    price REAL NOT NULL,
    price_per_sqft REAL,
    listing_date DATE,
    days_on_market INTEGER,
    price_change_amount REAL,
    price_change_percent REAL,
    listing_type TEXT, -- 'for_sale', 'sold', 'rental'
    recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Property Photos Table
```sql
CREATE TABLE property_photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER REFERENCES properties(id),
    file_path TEXT NOT NULL,
    photo_type TEXT, -- 'exterior', 'interior', 'screenshot'
    description TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Rental Comparables Table
```sql
CREATE TABLE rental_comps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER REFERENCES properties(id), -- NULL for standalone comps
    address TEXT NOT NULL,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    latitude REAL,
    longitude REAL,
    bedrooms INTEGER,
    bathrooms REAL,
    square_footage INTEGER,
    monthly_rent REAL,
    rent_per_sqft REAL,
    source TEXT, -- 'zillow', 'apartments.com', 'rent.com', 'manual'
    source_url TEXT,
    listing_date DATE,
    distance_miles REAL, -- Distance from target property
    recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Portfolio Performance Table (for owned properties)
```sql
CREATE TABLE portfolio_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER REFERENCES properties(id),
    month_year TEXT, -- 'YYYY-MM' format
    monthly_rent REAL,
    vacancy_days INTEGER DEFAULT 0,
    maintenance_costs REAL DEFAULT 0,
    other_operating_costs REAL DEFAULT 0,
    property_taxes REAL DEFAULT 0,
    insurance REAL DEFAULT 0,
    hoa_fees REAL DEFAULT 0,
    management_fees REAL DEFAULT 0,
    net_operating_income REAL, -- Calculated field
    mortgage_payment REAL DEFAULT 0,
    cash_flow REAL, -- Calculated field
    recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Investment Analysis Table
```sql
CREATE TABLE investment_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER REFERENCES properties(id),
    purchase_price REAL,
    down_payment REAL,
    loan_amount REAL,
    interest_rate REAL,
    loan_term_years INTEGER,
    closing_costs REAL,
    rehab_costs REAL,
    estimated_monthly_rent REAL,
    estimated_monthly_expenses REAL,
    cap_rate REAL, -- Calculated
    cash_on_cash_return REAL, -- Calculated
    total_cash_invested REAL, -- Calculated
    monthly_cash_flow REAL, -- Calculated
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Four Pillars Analysis Table
```sql
CREATE TABLE four_pillars_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER REFERENCES properties(id),
    analysis_year INTEGER,
    
    -- Pillar 1: Cash Flow
    annual_rental_income REAL,
    annual_operating_expenses REAL,
    annual_debt_service REAL,
    annual_cash_flow REAL, -- Calculated: income - expenses - debt_service
    
    -- Pillar 2: Loan Paydown (Principal Reduction)
    beginning_loan_balance REAL,
    ending_loan_balance REAL,
    annual_principal_paydown REAL, -- Calculated: beginning - ending
    
    -- Pillar 3: Appreciation
    beginning_property_value REAL,
    ending_property_value REAL,
    annual_appreciation REAL, -- Calculated: ending - beginning
    appreciation_rate REAL, -- Calculated: (appreciation / beginning_value) * 100
    
    -- Pillar 4: Tax Benefits
    depreciation_deduction REAL, -- Building value / 27.5 years (residential)
    interest_deduction REAL, -- Annual mortgage interest paid
    operating_expense_deductions REAL, -- Deductible operating expenses
    total_tax_deductions REAL, -- Calculated: sum of above
    estimated_tax_savings REAL, -- total_deductions * marginal_tax_rate
    marginal_tax_rate REAL, -- User's tax bracket
    
    -- Total Return Calculations
    total_annual_return REAL, -- Sum of all four pillars
    total_return_percentage REAL, -- total_return / total_cash_invested * 100
    
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Property Valuation History Table
```sql
CREATE TABLE property_valuations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER REFERENCES properties(id),
    valuation_date DATE,
    estimated_value REAL,
    valuation_method TEXT, -- 'purchase', 'appraisal', 'automated_estimate', 'manual'
    source TEXT, -- 'zillow_zestimate', 'redfin_estimate', 'appraisal', 'manual'
    notes TEXT,
    recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Regions Table
```sql
CREATE TABLE regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    center_latitude REAL,
    center_longitude REAL,
    zoom_level INTEGER DEFAULT 12,
    active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Application Architecture

### Main Application Structure
```
real_estate_app/
├── main.py                 # Application entry point
├── database/
│   ├── __init__.py
│   ├── models.py          # Database models and connections
│   └── migrations.py      # Database setup and migrations
├── gui/
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── property_analysis/
│   │   ├── __init__.py
│   │   ├── analysis_widget.py      # Property analysis module
│   │   ├── property_form.py        # Add/edit property forms
│   │   └── import_dialog.py        # Bulk import functionality
│   ├── rental_comps/
│   │   ├── __init__.py
│   │   ├── comps_widget.py         # Rental comparables module
│   │   └── comp_form.py            # Add/edit rental comp forms
│   ├── portfolio/
│   │   ├── __init__.py
│   │   ├── portfolio_widget.py     # Portfolio management module
│   │   └── performance_dialog.py   # Performance tracking
│   ├── maps/
│   │   ├── __init__.py
│   │   └── map_widget.py           # Map visualization component
│   └── shared/
│       ├── __init__.py
│       ├── base_widgets.py         # Reusable UI components
│       └── utils.py                # Utility functions
├── analytics/
│   ├── __init__.py
│   ├── calculations.py             # Financial calculations
│   └── market_analysis.py          # Market trend analysis
├── data/
│   ├── __init__.py
│   ├── importers.py               # Data import handlers
│   └── exporters.py               # Data export handlers
├── config/
│   ├── __init__.py
│   └── settings.py                # Application configuration
└── assets/
    ├── icons/                     # UI icons
    └── templates/                 # Import templates
```

---

## Module Specifications

### 1. Property Analysis Module (`gui/property_analysis/`)

**Purpose:** Manage properties in the analysis pipeline

**Key Features:**
- Property list view with sortable columns
- Add/edit individual properties
- Bulk import from Excel/CSV
- Price history tracking
- **Four Pillars Total Return Analysis Dashboard**
- Investment calculations display
- Photo management
- Status workflow (analyzing → under_contract → owned)

**Main Components:**
- `AnalysisWidget`: Main container with property list and details
- `PropertyForm`: Add/edit property dialog
- `FourPillarsWidget`: Comprehensive return analysis display
- `ImportDialog`: Bulk import wizard with template download

**Key Calculations:**
- Cap Rate = (Annual NOI / Purchase Price) × 100
- Cash-on-Cash Return = (Annual Cash Flow / Total Cash Invested) × 100
- **Four Pillars Total Return Analysis:**
  - **Pillar 1 - Cash Flow:** Annual rental income - operating expenses - debt service
  - **Pillar 2 - Loan Paydown:** Annual principal reduction on mortgage
  - **Pillar 3 - Appreciation:** Annual property value increase
  - **Pillar 4 - Tax Benefits:** Depreciation + interest + expense deductions × tax rate
  - **Total Return:** Sum of all four pillars as dollar amount and percentage
- Price per square foot trends
- Days on market analysis

### 2. Rental Comparables Module (`gui/rental_comps/`)

**Purpose:** Track rental properties for market analysis

**Key Features:**
- Rental property list with filtering by proximity
- Integration with property analysis (auto-populate comps for target property)
- Multiple source tracking (Zillow, Apartments.com, Rent.com)
- Rent per square foot analysis
- Map view of comps relative to target properties

**Main Components:**
- `CompsWidget`: Main rental comparables interface
- `CompForm`: Add/edit rental comp dialog

### 3. Portfolio Management Module (`gui/portfolio/`)

**Purpose:** Track owned properties and performance

**Key Features:**
- Portfolio overview dashboard
- Monthly performance entry
- KPI tracking (vacancy rates, NOI, cash flow)
- Rent growth analysis
- Operating expense categorization
- Performance reports and charts

**Main Components:**
- `PortfolioWidget`: Portfolio dashboard and property list
- `PerformanceDialog`: Monthly performance data entry

**Key Metrics:**
- Net Operating Income (NOI)
- Cash Flow (NOI - Debt Service)
- Vacancy Rate
- Operating Expense Ratio
- Rent Growth Rate

### 4. Map Visualization Module (`gui/maps/`)

**Purpose:** Interactive map view of all properties

**Key Features:**
- Folium-based interactive maps
- Property markers with popup details
- Color-coded by status (analyzing/under_contract/owned)
- Region-based filtering
- Rental comp overlay
- Click-to-view property details

**Main Components:**
- `MapWidget`: Main map container using QWebEngineView
- Integration with Folium for map generation
- Custom markers and popups for properties

**Technical Implementation:**
- Use QWebEngineView to render Folium HTML
- Dynamic map updates when properties change
- Custom JavaScript callbacks for marker interactions

### 5. Data Import/Export Module (`data/`)

**Purpose:** Handle bulk data operations

**Key Features:**
- Excel/CSV import with validation
- Template generation for imports
- Data export to Excel for analysis
- Error handling and validation reporting

**Import Template Fields:**
- Address (required)
- City, State, ZIP
- Bedrooms, Bathrooms
- Square Footage
- Asking Price
- Notes
- Source URL

### 6. Analytics Module (`analytics/`)

**Purpose:** Financial calculations and market analysis

**Key Financial Functions:**
- Mortgage payment calculations (principal and interest breakdown)
- **Four Pillars Total Return Analysis:**
  - **Cash Flow Analysis:** Monthly/annual cash flow projections
  - **Principal Paydown Calculations:** Amortization schedule tracking
  - **Appreciation Modeling:** Property value growth projections
  - **Tax Benefits Calculator:** Depreciation, interest, and expense deductions
- Investment returns (Cap Rate, Cash-on-Cash, Total Return)
- Market trend analysis
- Comparative market analysis (CMA)

**Four Pillars Implementation Details:**

**Pillar 1 - Cash Flow:**
```python
def calculate_annual_cash_flow(rental_income, operating_expenses, debt_service):
    return rental_income - operating_expenses - debt_service
```

**Pillar 2 - Principal Paydown:**
```python
def calculate_annual_principal_paydown(loan_amount, interest_rate, term_years, year):
    # Calculate principal paid in specific year using amortization
    monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, term_years)
    # Return annual principal reduction for given year
```

**Pillar 3 - Appreciation:**
```python
def calculate_appreciation(beginning_value, ending_value):
    appreciation_amount = ending_value - beginning_value
    appreciation_rate = (appreciation_amount / beginning_value) * 100
    return appreciation_amount, appreciation_rate
```

**Pillar 4 - Tax Benefits:**
```python
def calculate_tax_benefits(building_value, annual_interest, operating_expenses, tax_rate):
    depreciation = building_value / 27.5  # Residential depreciation schedule
    total_deductions = depreciation + annual_interest + operating_expenses
    tax_savings = total_deductions * tax_rate
    return tax_savings
```

**Market Analysis Features:**
- Price per square foot trends
- Days on market analysis
- Price change tracking
- Market velocity calculations

---

## User Interface Specifications

### Main Window Layout
```
┌─────────────────────────────────────────────────────────┐
│ File  Edit  View  Tools  Help                         │
├─────────────────────────────────────────────────────────┤
│ [Analysis] [Rental Comps] [Portfolio] [Map View]       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Module-specific content area                           │
│                                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Property Analysis Tab
```
┌─────────────────────────────────────────────────────────┐
│ [Add Property] [Import] [Export] Region: [Dropdown]  │
├─────────────────────────────────────────────────────────┤
│ Property List (Table)                                   │
│ ├─ Address | Beds/Baths | Sq Ft | Price | Status       │
│ ├─ 123 Main St | 3/2 | 1,500 | $250,000 | Analyzing    │
│ └─ 456 Oak Ave | 4/3 | 2,000 | $320,000 | Under Contract│
├─────────────────────────────────────────────────────────┤
│ Details Panel (when property selected)                  │
│ ├─ Property Info | Price History | Photos | Analysis   │
│ ├─ Four Pillars Analysis:                              │
│ │  ├─ Cash Flow: $X/month | Principal: $Y/year         │
│ │  ├─ Appreciation: $Z/year | Tax Benefits: $A/year    │
│ │  └─ Total Return: $B/year (X.X%)                     │
│ └─ [Edit] [Delete] [Change Status] [View on Map]       │
└─────────────────────────────────────────────────────────┘
```

### Map View Tab
```
┌─────────────────────────────────────────────────────────┐
│ Region: [Dropdown] Show: [☑Analyzing][☑Owned][☑Comps] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│              Interactive Folium Map                     │
│                                                         │
│  • Different colored markers by status                  │
│  • Popup details on click                              │
│  • Rental comps as smaller markers                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Configuration and Settings

### Application Settings (`config/settings.py`)
```python
# Database
DATABASE_PATH = "real_estate.db"

# Default regions
DEFAULT_REGIONS = [
    {"name": "Charlotte Metro", "lat": 35.2271, "lng": -80.8431, "zoom": 10}
]

# Financial defaults
DEFAULT_INTEREST_RATE = 0.07
DEFAULT_LOAN_TERM = 30
DEFAULT_DOWN_PAYMENT_PERCENT = 0.20
DEFAULT_DEPRECIATION_YEARS = 27.5  # Residential real estate
DEFAULT_MARGINAL_TAX_RATE = 0.24  # User's tax bracket for calculations
LAND_TO_BUILDING_RATIO = 0.20  # Default 20% land, 80% depreciable building

# Map settings
DEFAULT_MAP_ZOOM = 12
MAP_TILE_LAYER = "OpenStreetMap"

# Import validation
REQUIRED_FIELDS = ["address", "city", "state"]
MAX_IMPORT_ROWS = 1000

# Photo storage
PHOTOS_DIRECTORY = "photos"
MAX_PHOTO_SIZE_MB = 10
SUPPORTED_PHOTO_FORMATS = [".jpg", ".jpeg", ".png", ".gif"]
```

---

## Development Phases

### Phase 1: Core Foundation (Week 1-2)
1. Database schema implementation
2. Basic PyQt application structure
3. Property analysis module (basic CRUD)
4. Simple list view interface

### Phase 2: Analysis Features (Week 3-4)
5. Investment calculations
6. Price history tracking
7. Excel/CSV import functionality
8. Photo management

### Phase 3: Comparables & Maps (Week 5-6)
9. Rental comparables module
10. Map integration with Folium
11. Interactive map features
12. Region management

### Phase 4: Portfolio Management (Week 7-8)
13. Portfolio module for owned properties
14. Performance tracking
15. KPI dashboard
16. Reporting features

### Phase 5: Polish & Enhancement (Week 9-10)
17. UI refinements
18. Error handling improvements
19. Data validation enhancements
20. Documentation and testing

---

## Dependencies

### Required Python Packages
```
PyQt6==6.6.0
PyQtWebEngine==6.6.0
folium==0.15.1
pandas==2.1.4
numpy==1.25.2
openpyxl==3.1.2
Pillow==10.1.0
sqlite3 (built-in)
```

### Optional Enhancements
- `geopy` for address geocoding
- `plotly` for advanced charts
- `requests` for future API integrations

---

## Future Considerations

### iOS App Companion
- Shared SQLite database via cloud sync
- Photo capture and upload
- Basic property viewing
- Quick property status updates

### API Integrations (Future)
- Zillow API for automated data collection
- Google Maps API for enhanced mapping
- MLS data feeds
- Market data services

### Advanced Features
- Machine learning price predictions
- Automated market analysis reports
- Integration with accounting software
- Multi-user collaboration features

---

This specification provides a comprehensive foundation for building a professional real estate investment management system using Python and PyQt6, with clear development phases and scalable architecture.