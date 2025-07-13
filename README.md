# simpledatatabletk

This package is designed to meet the needs of having a data table for both manually entering values ​​and obtaining them from databases. Since Tkinter doesn't have a table widget as such, I was forced to create my own to meet the needs of future projects related to CRUD programs and forms that require database connections.

## Package structure
SimpleTable/␣
├── test/␣
│ └── Testdb␣
│   └── Base-de-pruebas.db␣
│   └── __init__.py␣
│   └── simpledatatabledtk_test.py␣
├── utilities␣
│   └── __init__.py␣
│    adapters.py␣
└── __init__.py␣
└── datatable.py␣

## Installation
pip install . #Local installation␣
pip install e . #Local installation in dev mode
