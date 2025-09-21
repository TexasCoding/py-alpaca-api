# Company Logos

The logos module provides access to company logo images for stocks and cryptocurrencies.

## Overview

The logos module allows you to:
- Retrieve company logos as binary image data
- Get direct URLs to logo resources
- Save logos to files
- Convert logos to base64 for embedding
- Batch retrieve logos for multiple symbols

## Usage

### Get Logo URL

```python
from py_alpaca_api import PyAlpacaAPI

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key"
)

# Get the URL for a company logo
logo_url = api.stock.logos.get_logo_url("AAPL")
print(f"Logo URL: {logo_url}")
# Output: https://data.alpaca.markets/v1beta1/logos/AAPL

# Use in HTML
html = f'<img src="{logo_url}" alt="AAPL logo">'
```

### Get Logo Data

```python
# Get logo as binary data
logo_data = api.stock.logos.get_logo("AAPL")

# Save to a file manually
with open("aapl_logo.png", "wb") as f:
    f.write(logo_data)
```

### Save Logo to File

```python
# Direct save to file
api.stock.logos.save_logo("AAPL", "logos/aapl.png")

# Save with placeholder if logo not found
api.stock.logos.save_logo(
    "UNKNOWN",
    "logos/unknown.png",
    placeholder=True
)
```

### Get Logo as Base64

```python
# Get logo as base64 for embedding
logo_base64 = api.stock.logos.get_logo_base64("AAPL")

# Use in HTML with data URI
html = f'<img src="data:image/png;base64,{logo_base64}" alt="AAPL logo">'

# Use in JSON response
response = {
    "symbol": "AAPL",
    "logo": logo_base64,
    "name": "Apple Inc."
}
```

### Multiple Logos

```python
# Get logos for multiple symbols
symbols = ["AAPL", "MSFT", "GOOGL", "INVALID"]
logos = api.stock.logos.get_multiple_logos(symbols)

# Process results
for symbol, logo_data in logos.items():
    if logo_data:
        print(f"{symbol}: Logo retrieved ({len(logo_data)} bytes)")
        # Save the logo
        with open(f"logos/{symbol}.png", "wb") as f:
            f.write(logo_data)
    else:
        print(f"{symbol}: No logo available")

# Get with placeholders for missing logos
logos = api.stock.logos.get_multiple_logos(
    symbols,
    placeholder=True  # Returns placeholder for missing logos
)
```

## Parameters

### get_logo()

- **symbol**: The stock symbol to get the logo for
- **placeholder**: If True, returns a placeholder image when logo is not available

### get_logo_url()

- **symbol**: The stock symbol to get the logo URL for
- **placeholder**: If True, includes placeholder parameter in URL

### save_logo()

- **symbol**: The stock symbol to get the logo for
- **filepath**: The path where the logo should be saved
- **placeholder**: If True, saves a placeholder image when logo is not available

### get_logo_base64()

- **symbol**: The stock symbol to get the logo for
- **placeholder**: If True, returns a placeholder image when logo is not available

### get_multiple_logos()

- **symbols**: List of stock symbols to get logos for
- **placeholder**: If True, returns placeholder images when logos are not available

## Placeholder Images

When a logo is not available, you can request a placeholder:

```python
# Request with placeholder
logo_url = api.stock.logos.get_logo_url("INVALID", placeholder=True)

# The API will return a generic placeholder image
logo_data = api.stock.logos.get_logo("INVALID", placeholder=True)
```

## Use Cases

### Website Display

```python
# Generate HTML for stock display
def create_stock_card(symbol):
    logo_url = api.stock.logos.get_logo_url(symbol, placeholder=True)
    quote = api.stock.latest_quote.get(symbol)

    return f"""
    <div class="stock-card">
        <img src="{logo_url}" alt="{symbol} logo" width="50">
        <h3>{symbol}</h3>
        <p>Price: ${quote.ask_price}</p>
    </div>
    """
```

### Report Generation

```python
# Include logos in PDF reports
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def add_logo_to_pdf(c, symbol, x, y):
    logo_data = api.stock.logos.get_logo(symbol, placeholder=True)

    # Save temporarily
    temp_file = f"/tmp/{symbol}_logo.png"
    with open(temp_file, "wb") as f:
        f.write(logo_data)

    # Add to PDF
    c.drawImage(temp_file, x, y, width=50, height=50)
```

### API Responses

```python
# Include logos in API responses
def get_stock_info(symbols):
    results = []
    for symbol in symbols:
        logo_base64 = api.stock.logos.get_logo_base64(symbol, placeholder=True)
        quote = api.stock.latest_quote.get(symbol)

        results.append({
            "symbol": symbol,
            "logo": logo_base64,
            "price": float(quote.ask_price),
            "timestamp": quote.timestamp.isoformat()
        })

    return results
```

## Error Handling

```python
from py_alpaca_api.exceptions import ValidationError

try:
    # Invalid symbol
    logo = api.stock.logos.get_logo("")
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    # Logo not found without placeholder
    logo = api.stock.logos.get_logo("INVALID_SYMBOL")
except Exception as e:
    print(f"Logo not found: {e}")

    # Retry with placeholder
    logo = api.stock.logos.get_logo("INVALID_SYMBOL", placeholder=True)
```

## Notes

- The logos endpoint is in beta (v1beta1)
- Logos are available for select stock and crypto symbols
- Image format is typically PNG
- For pricing details on the Logo API, contact sales@alpaca.markets
