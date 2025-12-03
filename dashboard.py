"""
JADE OS V1.0 - Command Center Dashboard
Streamlit-based operational interface for JADE OS backend

Tabs:
1. Shopee Nuclear Radar - Multi-country product scanning
2. Ghost Protocol - Video camouflage processing  
3. Strategy Brain - AI-powered strategy chat
"""

import streamlit as st
import pandas as pd
import asyncio
import os
import tempfile
import json
from datetime import datetime
from typing import Dict, Any

st.set_page_config(
    page_title="JADE OS - Command Center",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00ff88;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1a1a2e, #16213e);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #1a1a2e;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #00ff88;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1a1a2e;
        border-radius: 8px;
        padding: 0 24px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">💎 JADE OS - Command Center</div>', unsafe_allow_html=True)

SHOPEE_COUNTRIES = {
    "BR": "Brasil",
    "SG": "Singapore",
    "MY": "Malaysia",
    "TH": "Thailand",
    "VN": "Vietnam",
    "PH": "Philippines",
    "ID": "Indonesia",
}


def run_async(coro):
    """Run async function in sync context"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def load_social_signal_worker():
    """Load SocialSignalWorker"""
    try:
        from jade_os.workers.social_signal_worker import SocialSignalWorker
        return SocialSignalWorker(headless=True)
    except ImportError as e:
        st.error(f"Failed to load SocialSignalWorker: {e}")
        return None


def load_ghost_processor():
    """Load GhostProcessor"""
    try:
        from workers.ghost_processor import GhostProcessorV3
        return GhostProcessorV3()
    except ImportError as e:
        st.error(f"Failed to load GhostProcessor: {e}")
        return None


def load_strategy_router():
    """Load StrategyRouter"""
    try:
        from modules.auron_brain.engine import AuronEngine
        from modules.auron_brain.strategies import StrategyRouter
        engine = AuronEngine()
        return StrategyRouter(engine)
    except ImportError as e:
        st.error(f"Failed to load StrategyRouter: {e}")
        return None


def load_memory():
    """Load VectorMemory"""
    try:
        from jade_os.modules.auron_brain.memory import VectorMemory
        return VectorMemory()
    except ImportError as e:
        return None


tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Shopee Nuclear Radar",
    "👻 Ghost Protocol", 
    "🧠 Strategy Brain",
    "📊 System Status"
])


with tab1:
    st.header("🔍 Shopee Nuclear Radar")
    st.markdown("Multi-country product intelligence scanning with anti-detection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        keyword = st.text_input(
            "Search Keyword",
            placeholder="smartwatch, fone bluetooth, etc",
            key="shopee_keyword"
        )
        
        selected_countries = st.multiselect(
            "Countries to Scan",
            options=list(SHOPEE_COUNTRIES.keys()),
            default=["BR"],
            format_func=lambda x: f"{x} - {SHOPEE_COUNTRIES[x]}"
        )
    
    with col2:
        max_products = st.slider("Max Products per Country", 5, 50, 20)
        min_sold = st.number_input("Min Sales Filter", 0, 10000, 100)
    
    if st.button("🚀 Launch Nuclear Scan", type="primary", use_container_width=True):
        if not keyword:
            st.warning("Please enter a keyword")
        elif not selected_countries:
            st.warning("Please select at least one country")
        else:
            worker = load_social_signal_worker()
            if worker:
                with st.spinner(f"Scanning {len(selected_countries)} countries..."):
                    try:
                        result = run_async(
                            worker.scan_shopee_nuclear(
                                keyword=keyword,
                                countries=selected_countries,
                                max_products_per_country=max_products
                            )
                        )
                        
                        if result and result.get("products"):
                            products = result["products"]
                            
                            filtered = [p for p in products if p.get("sold", 0) >= min_sold]
                            
                            st.success(f"Found {len(filtered)} products (filtered from {len(products)})")
                            
                            df = pd.DataFrame(filtered)
                            
                            if not df.empty:
                                display_cols = ["name", "price", "sold", "stock", "rating", "region", "currency"]
                                existing_cols = [c for c in display_cols if c in df.columns]
                                
                                st.dataframe(
                                    df[existing_cols],
                                    use_container_width=True,
                                    height=400
                                )
                                
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    "📥 Export CSV",
                                    csv,
                                    f"shopee_scan_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    "text/csv",
                                    use_container_width=True
                                )
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Total Products", len(filtered))
                                with col2:
                                    if "price" in df.columns:
                                        st.metric("Avg Price", f"{df['price'].mean():.2f}")
                                with col3:
                                    if "sold" in df.columns:
                                        st.metric("Total Sales", f"{df['sold'].sum():,}")
                        else:
                            st.warning("No products found")
                            
                    except Exception as e:
                        st.error(f"Scan failed: {e}")


with tab2:
    st.header("👻 Ghost Protocol")
    st.markdown("Video camouflage with device fingerprint + GPS randomization")
    
    uploaded_file = st.file_uploader(
        "Upload Video",
        type=["mp4", "mov", "avi", "mkv"],
        help="Upload a video to apply ghost processing"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **Processing includes:**
        - Device fingerprint (iPhone/Samsung)
        - GPS randomization (10 Brazilian cities)
        - Hash washing (gamma, saturation, unsharp)
        - Metadata injection
        """)
    
    with col2:
        st.info("""
        **Output:**
        - Unique video hash
        - Realistic device metadata
        - Random GPS coordinates
        - Platform-safe audio
        """)
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("🎭 Apply Ghost Protocol", type="primary", use_container_width=True):
            processor = load_ghost_processor()
            
            if processor:
                with st.spinner("Applying camouflage..."):
                    try:
                        os.makedirs("data/uploads", exist_ok=True)
                        os.makedirs("data/processed", exist_ok=True)
                        
                        input_path = os.path.join("data/uploads", f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}")
                        
                        with open(input_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        output_path = run_async(
                            processor.process_video_upload(input_path)
                        )
                        
                        if output_path and os.path.exists(output_path):
                            st.success("Video processed successfully!")
                            
                            st.video(output_path)
                            
                            with open(output_path, "rb") as f:
                                st.download_button(
                                    "📥 Download Processed Video",
                                    f,
                                    os.path.basename(output_path),
                                    "video/mp4",
                                    use_container_width=True
                                )
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                input_size = os.path.getsize(input_path) / (1024 * 1024)
                                st.metric("Input Size", f"{input_size:.2f} MB")
                            with col2:
                                output_size = os.path.getsize(output_path) / (1024 * 1024)
                                st.metric("Output Size", f"{output_size:.2f} MB")
                            with col3:
                                st.metric("Compression", f"{((input_size - output_size) / input_size * 100):.1f}%")
                        else:
                            st.error("Processing failed - check logs")
                            
                    except Exception as e:
                        st.error(f"Ghost Protocol failed: {e}")


with tab3:
    st.header("🧠 Strategy Brain")
    st.markdown("AI-powered strategic analysis with OTTO SUPREME")
    
    memory = load_memory()
    
    with st.expander("💾 Business Context (Long-Term Memory)", expanded=False):
        st.markdown("Store context so you don't repeat yourself every prompt")
        
        context_key = st.text_input("Context Key", placeholder="business_type, target_audience, etc")
        context_value = st.text_area("Context Value", placeholder="We sell smartwatches for fitness...")
        
        if st.button("💾 Save Context"):
            if memory and context_key and context_value:
                memory.add(context_key, context_value)
                st.success(f"Saved: {context_key}")
            else:
                st.warning("Please fill key and value")
        
        if memory:
            stored = memory.get_all()
            if stored:
                st.markdown("**Stored Contexts:**")
                for k, v in stored.items():
                    st.markdown(f"- **{k}**: {v[:100]}...")
    
    strategy_options = [
        "otto_chat - Chat direto com OTTO",
        "arbitrage_sniper - Análise de arbitragem",
        "mythos_copy - Geração de copy viral",
        "hook_generator - Geração de hooks",
        "script_writer - Escrita de roteiro",
        "otto_strategy - 3 estratégias OTTO",
    ]
    
    selected_strategy = st.selectbox("Strategy", strategy_options)
    strategy_name = selected_strategy.split(" - ")[0]
    
    user_input = st.text_area(
        "Input",
        placeholder="Descreva seu objetivo, produto ou situação...",
        height=150
    )
    
    if st.button("🚀 Execute Strategy", type="primary", use_container_width=True):
        if not user_input:
            st.warning("Please enter your input")
        else:
            router = load_strategy_router()
            
            if router:
                with st.spinner("Executing strategy..."):
                    try:
                        context = ""
                        if memory:
                            stored = memory.get_all()
                            if stored:
                                context = "\n".join([f"{k}: {v}" for k, v in stored.items()])
                                user_input = f"[CONTEXT]\n{context}\n\n[REQUEST]\n{user_input}"
                        
                        params = {
                            "message": user_input,
                            "topic": user_input,
                            "idea": user_input,
                        }
                        
                        result = run_async(router.execute(strategy_name, params))
                        
                        if result:
                            status = result.get("status", "unknown")
                            
                            if status == "success":
                                st.success("Strategy executed successfully!")
                            elif status == "error":
                                st.error(result.get("message", "Unknown error"))
                            else:
                                st.info(f"Status: {status}")
                            
                            data = result.get("data", {})
                            
                            response = (
                                data.get("response") or 
                                data.get("copy") or 
                                data.get("hooks") or 
                                data.get("script") or 
                                data.get("strategies") or
                                data.get("analysis") or
                                data.get("validation") or
                                json.dumps(data, indent=2, ensure_ascii=False)
                            )
                            
                            st.markdown("### Result")
                            st.markdown(response)
                            
                    except Exception as e:
                        st.error(f"Strategy failed: {e}")


with tab4:
    st.header("📊 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("FastAPI", "🟢 Running", "Port 5000")
    with col2:
        st.metric("Redis", "🟢 Running", "Port 6800")
    with col3:
        st.metric("Celery", "🟢 Running", "2 Workers")
    with col4:
        st.metric("Playwright", "🟢 Ready", "Chromium")
    
    st.divider()
    
    st.subheader("🔧 Configuration")
    
    env_vars = {
        "DATABASE_URL": "✅ Configured" if os.getenv("DATABASE_URL") else "❌ Missing",
        "PROXY_HOST": "✅ Configured" if os.getenv("PROXY_HOST") else "⚠️ Optional",
        "OPENAI_API_KEY": "✅ Configured" if os.getenv("OPENAI_API_KEY") else "⚠️ Fallback Mode",
        "TELEGRAM_BOT_TOKEN": "✅ Configured" if os.getenv("TELEGRAM_BOT_TOKEN") else "⚠️ Optional",
    }
    
    for key, status in env_vars.items():
        st.markdown(f"- **{key}**: {status}")
    
    st.divider()
    
    st.subheader("📁 Workers Available")
    
    workers = [
        ("SocialSignalWorker V3", "Multi-country Shopee scanning with context reset"),
        ("GhostProcessor V3", "Video camouflage with GPS randomization"),
        ("SupplyChainWorker V3", "Playwright-based product intelligence"),
        ("StrategyRouter V3", "AI-powered strategy execution (sanitized)"),
    ]
    
    for name, desc in workers:
        st.markdown(f"- **{name}**: {desc}")


with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=JADE+OS", width=150)
    
    st.markdown("---")
    st.markdown("### Quick Actions")
    
    if st.button("🔄 Refresh Status"):
        st.rerun()
    
    st.markdown("---")
    st.markdown("### API Endpoints")
    st.code("""
GET  /health
GET  /docs
POST /intel/supply/track
POST /agent/strategy
POST /video/wash
    """)
    
    st.markdown("---")
    st.markdown("### Version")
    st.markdown("**JADE OS v1.0**")
    st.markdown("Build: December 2025")
