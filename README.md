# Solana Token Scanner Bot

A comprehensive Telegram bot that provides real-time analysis and risk assessment for Solana blockchain tokens. Users input a token contract address and receive detailed financial metrics, security analysis, and market data.

## System Functionality

**Core Features:**

- Real-time token price, market cap, and trading volume analysis
- Liquidity pool burn percentage calculation for rug-pull detection
- Developer wallet tracking and token distribution analysis
- Social media links extraction and validation
- Multi-platform support (Pump.fun, Moonshot, DEX trading pairs)
- Token holder concentration analysis (top 20 wallets)
- All-time high price tracking and performance metrics
- Mint/freeze authority verification for security assessment

**Risk Assessment:**

- Automatic detection of suspicious token characteristics
- LP burn percentage analysis for liquidity safety
- Developer token holdings and transaction history
- Token authority permissions (mint/freeze capabilities)

## Technologies Used

**Backend & APIs:**

- Python 3.10 with asyncio for concurrent processing
- Solana RPC integration via `solana-py` and `solders`
- REST API integrations (Birdeye, DexScreener, Raydium, RugCheck)
- aiohttp for asynchronous HTTP requests

**Bot Framework:**

- python-telegram-bot for Telegram integration
- Real-time messaging with formatted responses and images

**Data Processing:**

- Custom data structures with dataclasses
- Financial metrics calculation and formatting
- Time-based analysis with datetime processing

**Deployment:**

- Heroku-ready with Procfile configuration
- Environment variable management for API keys

## Key Skills Demonstrated

**Blockchain Development:**

- Solana blockchain interaction and RPC client implementation
- Token metadata extraction and on-chain data analysis
- Smart contract interaction for liquidity and authority verification

**Asynchronous Programming:**

- Concurrent API calls using asyncio.gather()
- Efficient session management with aiohttp
- Non-blocking operations for real-time responsiveness

**API Integration:**

- Multiple third-party API orchestration (Birdeye, DexScreener, Raydium)
- Error handling and fallback mechanisms
- Rate limiting and request optimization

**Financial Analysis:**

- Complex financial metrics calculation
- Risk assessment algorithms
- Market data aggregation and trend analysis

**Bot Development:**

- Telegram Bot API implementation
- User input validation and sanitization
- Rich message formatting with embedded links and emojis

**System Architecture:**

- Modular code organization with separation of concerns
- Type safety with Python dataclasses
- Scalable error handling and logging
