import streamlit as st
import requests
import time
import math
from streamlit_autorefresh import st_autorefresh

# Streamlit Page configuration
st.set_page_config(page_title="Crypto Luxury Scanner", layout="wide")

# ১ ঘণ্টা (৩৬০০ সেকেন্ড) পর পর অটোমেটিক পেজ রিফ্রেশ ও স্ক্যান করার জন্য অটো-রিফ্রেশার
# key সেট করা হয়েছে যাতে প্রতি রিফ্রেশে লুপটি নতুন করে ফ্রেশ রান নেয়
st_autorefresh(interval=3600 * 1000, key="crypto_scanner_refresh")

# টেলিগ্রাম কনফিগারেশন
TELEGRAM_BOT_TOKEN = "8957518460:AAE_9HaugsNNYfjOzCpbHi2nJAEKf4GSiKs"
TELEGRAM_CHAT_ID = "6166836299"

# কয়েন লিস্ট (CoinGecko IDs)
coingecko_coin_ids = [
    # ১. মেগা ও লার্জ ক্যাপ অল্টকয়েন
    "bitcoin", "ethereum", "binancecoin", "solana", "ripple", 
    "cardano", "polkadot", "avalanche-2", "chainlink", "litecoin", 
    "dogecoin", "shiba-inu", "matic-network", "cosmos", "bitcoin-cash", 
    "ethereum-classic", "stellar", "near", "tron", "uniswap",
    # ২. লেয়ার ১ এবং লেয়ার ২ ইকোসিস্টেম
    "sui", "aptos", "toncoin", "injective-protocol", "sei-network", 
    "fantom", "algorand", "elrond-erd-2", "celestia", "mina-protocol", 
    "flow", "internet-computer", "eos", "kava", "astar", 
    "harmony", "hedera-hashgraph", "iota", "neo", "qtum", 
    "vechain", "zilliqa", "waves", "theta-token", "stratisevm",
    "arbitrum", "optimism", "starknet", "metis-token", "manta-network", 
    "skale", "celo", "loopring", "immutable-x", "omg", "oasis",
    # ৩. মিম কয়েন
    "pepe", "dogwifhat", "bonk", "floki", "book-of-meme", 
    "memecoin", "myro", "1000sats", "corgiai", "coq-inu", 
    "turbo", "baby-doge-coin", "constitutiondao", "wen", "ai-doge", 
    "milady-meme-coin", "rats", "notcoin", "popcat", "cat-in-a-dogs-world", 
    "brett", "mog-coin", "first-neiro-on-ethereum", "moodeng", "goatseus-maximus", 
    "peanut-the-squirrel", "act-i-the-ai-prophecy", "comedian", "fartcoin", "pudgy-penguins", 
    "degen-base", "puffer-finned", "aixbt", "cheems", "sundog", 
    "official-trumpet", "chillguy",
    # ৪. AI, DePIN এবং বিগ ডেটা
    "fetch-ai", "render-token", "the-graph", "bittensor", "akash-network", 
    "singularitynet", "ocean-protocol", "phoenix-global", "arkham", "worldcoin", 
    "nfprompt", "sleepless-ai", "livepeer", "filecoin", "arweave", 
    "jasmycoin", "storj", "bluzelle", "ankr", "io-net", 
    "speculative-token", "nosana", "clore-ai", "golem", "ordinals", 
    "measurable-data-token", "cortex", "everipedia", "gitcoin", "clover-finance",
    # ৫. ডেফি, আরডব্লিউএ এবং ওয়েব৩ প্রজেক্টস
    "aave", "pendle", "maker", "curve-dao-token", "lido-dao", 
    "jupiter-exchange-solana", "thorchain", "dydx-chain", "ethereum-name-service", "compound-governance-token", 
    "synthetix-network-token", "sushi", "yearn-finance", "pancakeswap-token", "bakerytoken", 
    "raydium", "joe", "jito-governance-token", "orca", "cow-protocol", 
    "1inch", "balancer", "badger-dao", "alpha-finance", "recurrent-value",
    "ethena", "zero1-labs", "drift-protocol", "safe", "decentralized-usd", 
    "pyth-network", "axelar", "ondo-finance", "truefi", "alpaca-finance", 
    "bella-protocol", "bounce-token", "troy", "quickswap", "stafi", 
    "unifi-protocol-dao", "ether-fi", "renzo", "omni-network", "tensor", 
    "saga", "bounce-bit", "district0x", "wazirx", "scroll", 
    "hyperliquid", "magic-eden", "vethor-token", "chronobank", "system-omega",
    "celer-network", "combo-token", "huma-finance", "zora", "cetus-protocol", "kite-network",
    # ৬. গেমিং এবং মেটাভার্স (GameFi)
    "gala", "axie-infinity", "the-sandbox", "decentraland", "pixel", 
    "beam", "yield-guide-games", "illuvium", "my-neighbor-alice", "enjincoin", 
    "magic", "portal", "xai", "chiliz", "superfarm", 
    "voxel", "mines-of-dalarnia", "alien-worlds", "ghost-token", "bigtime", 
    "token-fi", "vanarchain", "mbox", "revolution-games", "highstreet",
    # ৭. ইনফ্রাস্ট্রাকচার ও ক্রস-চেইন (Oracle)
    "wormhole", "stargate-finance", "synapse", "moonbeam", "moonriver", 
    "kusama", "icon", "band-protocol", "tellor", "dia",
    # ৮. ওল্ড-স্কুল অল্টকয়েন ও ট্রেন্ডিং লো-ক্যাপ
    "zcash", "monero", "dash", "horizen", "ontology", 
    "iotex", "ravencoin", "holotoken", "basic-attention-token", "kyber-network-crystal", 
    "0x", "ren", "woo-network", "stepn", "space-id", 
    "open-campus", "hooked-protocol", "cyberconnect", "maverick-protocol", "ark", 
    "polymath", "loom-network", "barnbridge", "voyager-token", "stratisevm", 
    "radicle", "mubarak"
]

# --- UI Custom CSS ---
st.markdown("""
    <style>
    /* Main Theme - ডার্ক লাক্সারি ব্যাকগ্রাউন্ড */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 100%);
        color: #f8fafc;
    }
    
    /* Glowing Title */
    h1 {
        color: #00d2ff !important;
        background: linear-gradient(to right, #00ffff, #0088ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 900 !important;
        text-shadow: 0px 0px 20px rgba(0, 255, 255, 0.3);
    }
    
    /* Live Scanning Card Styling */
    .scanning-box {
        background: rgba(17, 24, 39, 0.85);
        border: 2px solid #38bdf8;
        box-shadow: 0px 0px 25px rgba(56, 189, 248, 0.4);
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin: 20px 0;
        animation: pulse 1.5s infinite alternate;
    }
    
    /* Glowing Scanning Coin */
    .scanning-coin {
        font-size: 3rem !important;
        font-weight: 800;
        color: #ff007f !important;
        text-shadow: 0 0 15px rgba(255, 0, 127, 0.6);
        letter-spacing: 2px;
    }
    
    @keyframes pulse {
        0% { transform: scale(0.99); box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }
        100% { transform: scale(1.01); box-shadow: 0 0 30px rgba(56, 189, 248, 0.6); }
    }
    
    /* Signal Output Box Styles */
    .signal-card {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-family: monospace;
    }
    .buy-card {
        background-color: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #10b981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
    }
    .sell-card {
        background-color: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        color: #ef4444;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Luxury Crypto Auto-Scanner (H1 Frame)")
st.write("স্বয়ংক্রিয় ১ ঘণ্টার স্বাধীন রেডিও স্ক্যানার। এটি প্রতি ১ ঘণ্টা পর পর সচল হবে।")

# টেলিগ্রাম ফাংশন
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass

# কাস্টম পিওর পাইথন ইন্ডিকেটর ক্যালকুলেটর (Pandas ছাড়া)
def calculate_ema(prices, period=200):
    if len(prices) < period:
        return [0] * len(prices)
    ema = []
    k = 2 / (period + 1)
    # প্রথম SMA দিয়ে শুরু
    sma = sum(prices[:period]) / period
    ema.append(sma)
    for price in prices[period:]:
        next_ema = (price * k) + (ema[-1] * (1 - k))
        ema.append(next_ema)
    # ফ্রন্ট প্যাডিং ব্যালেন্স করা হচ্ছে
    return [0] * (period - 1) + ema

def calculate_macd(prices, slow=26, fast=12, signal_period=9):
    if len(prices) < slow:
        return [], []
    
    # Fast EMA
    k_fast = 2 / (fast + 1)
    ema_fast = [prices[0]]
    for p in prices[1:]:
        ema_fast.append((p * k_fast) + (ema_fast[-1] * (1 - k_fast)))
        
    # Slow EMA
    k_slow = 2 / (slow + 1)
    ema_slow = [prices[0]]
    for p in prices[1:]:
        ema_slow.append((p * k_slow) + (ema_slow[-1] * (1 - k_slow)))
        
    # MACD Line
    macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
    
    # Signal Line (EMA of MACD Line)
    if len(macd_line) < signal_period:
        return [], []
    k_sig = 2 / (signal_period + 1)
    signal_line = [macd_line[0]]
    for m in macd_line[1:]:
        signal_line.append((m * k_sig) + (signal_line[-1] * (1 - k_sig)))
        
    return macd_line, signal_line

# ডাটা ফেচিং এবং লজিক অ্যানালাইসিস
def fetch_and_analyze(coin_id):
    # CoinGecko OHLC API ব্যবহার (H1 টাইমফ্রেমের জন্য ১ বা ৩০ দিনের উইন্ডো পারফেক্ট)
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=usd&days=30"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return None
        data = response.json() # [timestamp, open, high, low, close]
        if len(data) < 210: # ২০০ EMA এবং লুকব্যাকের জন্য পর্যাপ্ত ডাটা দরকার
            return None
        
        closes = [candle[4] for candle in data]
        highs = [candle[2] for candle in data]
        lows = [candle[3] for candle in data]
        
        current_close = closes[-1]
        
        # ১. EMA 200 ক্যালকুলেশন
        ema200_list = calculate_ema(closes, 200)
        current_ema200 = ema200_list[-1]
        
        # ২. MACD Divergence Lookback=30
        macd_line, signal_line = calculate_macd(closes)
        if not macd_line or not signal_line:
            return None
            
        # উইন্ডো ম্যাচ করার জন্য শেষ ৩০টি ভ্যালু নেওয়া
        m_lookback = macd_line[-30:]
        s_lookback = signal_line[-30:]
        
        # ডাইভারজেন্স ট্র্যাকিং লজিক
        macd_divergence_bullish = False
        macd_divergence_bearish = False
        if len(m_lookback) >= 2:
            # সিম্পল ডাইভারজেন্স ট্র্যাকিং: প্রাইস এবং ম্যাকডি লাইনের শেষ প্রান্তের ট্রেন্ড বিপরীত কিনা
            price_trend = closes[-1] - closes[-15]
            macd_trend = m_lookback[-1] - m_lookback[-15]
            if price_trend < 0 and macd_trend > 0:
                macd_divergence_bullish = True
            elif price_trend > 0 and macd_trend < 0:
                macd_divergence_bearish = True

        # ৩. Equal Low / High (Swing Prominence=5, Buffer=0.0025)
        # শেষ ৩০ ক্যান্ডেলে লোকাল সুইং হাই/লো বের করা
        buffer = 0.0025
        is_equal_low = False
        is_equal_high = False
        
        # শেষ ক্যান্ডেলের লো/হাই এর সাথে পূর্ববর্তী লোকাল সুইং ম্যাচিং
        curr_low = lows[-1]
        curr_high = highs[-1]
        
        # সুইং প্রমিনেন্স চেক (৫টি ক্যান্ডেলের উইন্ডো)
        for j in range(-25, -5):
            # Equal Low Check
            if abs(lows[j] - curr_low) <= buffer:
                # আশেপাশের ক্যান্ডেলের চেয়ে লো কিনা ভেরিফাই করা
                if lows[j] == min(lows[j-2:j+3]):
                    is_equal_low = True
            # Equal High Check
            if abs(highs[j] - curr_high) <= buffer:
                if highs[j] == max(highs[j-2:j+3]):
                    is_equal_high = True

        # ৪. সিগন্যাল ট্রিগার স্টেটমেন্ট
        # Buy Signal: Price < EMA200 + Equal Low + Bullish Divergence
        if current_close < current_ema200 and is_equal_low and macd_divergence_bullish:
            return {"type": "BUY", "price": current_close}
            
        # Sell Signal: Price > EMA200 + Equal High + Bearish Divergence
        if current_close > current_ema200 and is_equal_high and macd_divergence_bearish:
            return {"type": "SELL", "price": current_close}
            
        return None
    except Exception:
        return None

# --- UI Layout ২ ভাগে বিভক্ত ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 Buy Signals (Green Output)")
    buy_container = st.container()

with col2:
    st.subheader("🔴 Sell Signals (Red Output)")
    sell_container = st.container()

# লাইভ স্ট্যাটাস বক্স কন্টেইনার (এটি টপে স্লাইড হবে)
live_status_box = st.empty()

# মেইন প্রসেসিং লুপ
total_coins = len(coingecko_coin_ids)

for i, coin in enumerate(coingecko_coin_ids):
    progress_perc = int(((i + 1) / total_coins) * 100)
    
    # আপনার দেওয়া চমৎকার লাইভ পপ-আপ অ্যানিমেশন বক্স
    live_status_box.markdown(f"""
        <div class="scanning-box">
            <p style="color: #38bdf8; font-size: 1.2rem; margin-bottom: 5px; font-weight: 600;">
                🔍 বর্তমান স্ক্যানিং প্রোগ্রেস: {progress_perc}% ({i+1}/{total_coins})
            </p>
            <div class="scanning-coin">{coin.upper()}</div>
            <p style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">
                কয়েনগেকো সার্ভার রেট-লিমিট কূলডাউন বিরতি চলমান...
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # অ্যানালাইসিস শুরু
    result = fetch_and_analyze(coin)
    
    if result:
        if result["type"] == "BUY":
            # ব্রাউজার আউটপুট (সবুজ থিম)
            with buy_container:
                st.markdown(f"""
                    <div class="signal-card buy-card">
                        <h3>🟢 {coin.upper()} - BUY SIGNAL</h3>
                        <p>Price: ${result['price']}</p>
                        <small>Timeframe: H1 | Condition Matrix Match</small>
                    </div>
                """, unsafe_allow_html=True)
            # টেলিগ্রাম নোটিফিকেশন প্রেরণ
            send_telegram_message(f"🟢 *BUY SIGNAL DETECTED*\n\nCoin: {coin.upper()}\nPrice: ${result['price']}\nTF: 1 Hour\nStatus: 200 EMA Down + Equal Low + MACD Divergence")
            
        elif result["type"] == "SELL":
            # ব্রাউজার আউটপুট (লাল থিম)
            with sell_container:
                st.markdown(f"""
                    <div class="signal-card sell-card">
                        <h3>🔴 {coin.upper()} - SELL SIGNAL</h3>
                        <p>Price: ${result['price']}</p>
                        <small>Timeframe: H1 | Condition Matrix Match</small>
                    </div>
                """, unsafe_allow_html=True)
            # টেলিগ্রাম নোটিফিকেশন প্রেরণ
            send_telegram_message(f"🔴 *SELL SIGNAL DETECTED*\n\nCoin: {coin.upper()}\nPrice: ${result['price']}\nTF: 1 Hour\nStatus: 200 EMA Up + Equal High + MACD Divergence")

    # CoinGecko Public API Rate Limit (প্রতি মিনিটে ১০-৩০ রিকোয়েস্ট) এড়াতে হালকা ইন্টারভাল গ্যাপ
    time.sleep(1.8)

# স্ক্যান শেষ হলে পপ-আপ বক্সটি সফল বার্তা দেখাবে
live_status_box.success("✅ ১ ঘণ্টার এই রাউন্ডের স্ক্যানিং সফলভাবে সম্পন্ন হয়েছে! পরবর্তী স্ক্যান অটোমেটিক শুরু হবে।")
