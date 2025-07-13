# Solana Token Scanner Telegram Bot 🤖

A comprehensive Telegram bot that provides detailed analysis and information about Solana tokens, including tokens from PumpFun, Moonshot, and DEX platforms.

## 🌟 Features

### Token Analysis
- **Multi-Platform Support**: Analyzes tokens from PumpFun, Moonshot, and traditional DEX platforms
- **Comprehensive Token Data**: 
  - Price, market cap, and liquidity information
  - Token age and creation details
  - All-time high (ATH) tracking
  - Volume metrics (1h/24h)
  - Price change indicators

### Security Analysis
- **Mint/Freeze Authority Check**: Identifies if tokens can be minted or frozen
- **LP Burn Analysis**: Calculates liquidity pool burn percentage
- **Developer Analysis**:
  - Developer wallet balance tracking
  - Developer token holdings percentage
  - Snipe percentage calculation
- **Top Holders Analysis**: Shows concentration of top wallets

### Social & External Links
- **Social Media Integration**: Links to Twitter, Telegram, and websites
- **Chart Links**: Direct links to DexScreener, Photon, and Birdeye
- **Holder Information**: Links to Solscan for detailed holder analysis

## 📁 Project Structure

```
sol-scanner-13-07/
├── bot.py                 # Main Telegram bot entry point
├── birdeye_entry.py       # Birdeye API integration (primary entry)
├── entry.py              # Alternative entry point with Solscan integration
├── dexscreener.py        # DexScreener API integration
├── moonshot.py           # Moonshot platform specific logic
├── my_types.py           # Type definitions and data classes
├── API_KEYS.py           # API configuration file
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment configuration
├── runtime.txt          # Python runtime version
│
├── modules/             # Core functionality modules
│   ├── birdeye.py       # Birdeye API functions
│   ├── data_processing.py # Data formatting utilities
│   ├── largest_accounts.py # Top wallet analysis
│   ├── raydium.py       # Raydium DEX integration
│   └── rugcheck.py      # Rugcheck API integration
│
├── pump/                # PumpFun specific modules
│   ├── pump_creation_time.py # Token creation time tracking
│   └── pump_metadata.py     # Pump metadata retrieval
│
└── todo/                # Development and testing scripts
    ├── beach.py         # Solana Beach API testing
    ├── bird.py          # Birdeye API testing
    ├── burn.py          # LP burn testing
    └── find.py          # Token discovery utilities
```

## 📋 Usage

### Basic Commands
1. **Start the bot**: Send `/start` to get a welcome message
2. **Get help**: Send `/help` for assistance
3. **Analyze token**: Send any valid Solana token address (44 characters, Base58)

### Example Token Addresses
- PumpFun token: `9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump`
- Moonshot token: `BNu5McPaw1YUfLcsxKoQtiurvM33rA7jsW1rdYM2moon`
- DEX token: Any standard Solana token address

### Sample Output
The bot returns formatted messages with:
- Token name, symbol, and icon
- Security indicators (mint/freeze authority)
- Price and market data
- Developer information
- Holder statistics
- Chart and analysis links

## 🔌 API Integrations

### Primary APIs
- **Birdeye**: Token metadata, pricing, security analysis
- **DexScreener**: Trading data, social links, volume metrics
- **Raydium**: Liquidity pool analysis and burn percentages
- **Helius**: Solana blockchain RPC access
- **RugCheck**: Token security scoring (optional)

### Data Sources
- **Solscan**: Holder analysis and transaction history
- **Photon**: Advanced trading interface links
- **Pump.fun**: PumpFun specific token data

