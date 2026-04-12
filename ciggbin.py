import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import hashlib

# ---------- AI IMPORTS ----------
# ---------- AI IMPORTS & MODEL LOAD ----------
# ---------- AI IMPORTS & MODEL LOAD ----------
import os
import streamlit as st

AI_AVAILABLE = False
MODEL_LOADED = False
model = None

# Step 1: Import YOLO
try:
    from ultralytics import YOLO
    AI_AVAILABLE = True
    st.write("✅ Ultralytics imported successfully")
except Exception as e:
    st.error(f"❌ Ultralytics import error: {e}")

# Step 2: Load model
if AI_AVAILABLE:
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "cigarette_model.pt")

        st.write(f"📁 Looking for model at: {model_path}")

        if not os.path.exists(model_path):
            st.error("❌ Model file NOT found!")
        else:
            st.write("✅ Model file found")

            # 🔥 TEMP TEST (very important)
            # Replace with your model later
           model = YOLO("yolov8n.pt")
            # model = YOLO("yolov8n.pt")  # <-- uncomment this to test if needed

            MODEL_LOADED = True
            st.success("✅ Model loaded successfully!")

    except Exception as e:
        MODEL_LOADED = False
        st.error(f"❌ Model loading error: {e}")


# ---------- CACHED MODEL LOADER (CRITICAL FIX) ----------
@st.cache_resource
def load_model():
    """Loads the YOLO model ONCE and caches it for the entire Streamlit session.
    Without this decorator, the model reloads on every widget interaction,
    causing the blank screen / freeze bug."""
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "cigarette_model.pt")
        return YOLO(model_path)
    except Exception as e:
        print("Model loading error:", e)
        return None


# ---------- PAGE CONFIGURATION ----------
st.set_page_config(page_title="EcoButt App", layout="wide", initial_sidebar_state="expanded")

# ---------- PREMIUM UI STYLE (DRIBBBLE MATCH) ----------
def load_custom_css():
    st.markdown("""
    <style>
    /* 1. Import Premium Font (Plus Jakarta Sans) & Material Icons */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@48,400,0,0');

    /* 2. Global Typography & Background */
    html, body, .stApp, .main, .stMarkdown p, .stText, p, label, h1, h2, h3, h4, h5, h6, li, input {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* 3. CRITICAL FIX: Restore Streamlit Icons */
    header button span,
    header button i,
    header button *,
    [data-testid="collapsedControl"] span,
    [data-testid="collapsedControl"] *,
    [data-testid="stSidebarCollapsedControl"] * {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        color: #151618 !important;
    }

    /* Sidebar close button icon */
    [data-testid="stSidebar"] button span,
    [data-testid="stSidebar"] button * {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        color: #FFFFFF !important;
    }

    /* Main App Background */
    .stApp {
        background-color: #EEF0EC !important; 
    }

    /* Force dark text for main content area */
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label, .stMarkdown p, .stText {
        color: #151618 !important; 
    }

    /* 4. Dark Sidebar */
    [data-testid="stSidebar"] {
        background-color: #131514 !important;
        border-right: none !important;
        padding-top: 2rem !important;
    }
    
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] div {
        color: #E2E4E2 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        padding: 12px 16px !important;
        border-radius: 12px !important;
        margin-bottom: 4px !important;
        transition: background-color 0.2s ease !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: #2A2C2B !important;
    }
    [data-testid="stSidebar"] .st-b5 { 
        display: none !important;
    }

    /* 5. Typography */
    h1, h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.03em !important;
        color: #151618 !important;
    }
    
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 500 !important;
        line-height: 1.1 !important;
        color: #151618 !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.04em !important;
    }
    .hero-highlight {
        color: #151618 !important;
        background-color: #D6F169;
        padding: 0 12px;
        border-radius: 12px;
        display: inline-block;
    }

    /* 6. Button Styling */
    .stButton>button {
        background-color: #131514 !important; 
        color: #FFFFFF !important;
        border-radius: 50px !important;
        padding: 12px 28px !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
    }
    
    .stButton>button p, .stButton>button span {
        color: #FFFFFF !important;
    }

    .stButton>button:hover {
        background-color: #2A2C2B !important; 
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.15) !important;
    }

    /* 7. Input Fields */
    .stTextInput>div>div>input {
        border-radius: 16px !important;
        border: 1px solid #DCE0DA !important;
        padding: 16px !important;
        background-color: #FFFFFF !important;
        color: #151618 !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #D6F169 !important;
        box-shadow: 0 0 0 2px #D6F169 !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #A0A2A0 !important;
    }
    
    [data-testid="stWidgetLabel"] p {
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: #5A5D5A !important;
        margin-bottom: 8px !important;
    }

    /* 8. Static Text Cards */
    .custom-card {
        background-color: #FFFFFF;
        padding: 32px;
        border-radius: 24px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: none;
        margin-bottom: 24px;
        line-height: 1.6;
        color: #151618 !important;
    }
    .custom-card * {
        color: #151618 !important;
    }
    .custom-card-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        color: #151618 !important;
    }
    .custom-card-title::before {
        content: '';
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #D6F169;
        border-radius: 50%;
    }

    /* 9. Streamlit Metric Cards */
    [data-testid="metric-container"] {
        background-color: #FFFFFF !important;
        padding: 24px;
        border-radius: 24px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: none !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] * {
        color: #151618 !important;
        font-weight: 600 !important;
        font-size: 3rem !important;
        letter-spacing: -0.05em !important;
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {
        color: #7A7D7A !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    /* 10. DataFrames & Tables */
    [data-testid="stTable"], [data-testid="stDataFrame"] {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: none !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03) !important;
    }
    th, th * {
        background-color: #F8F9F8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        border-bottom: 1px solid #EEF0EC !important;
        text-transform: uppercase;
        color: #7A7D7A !important;
    }
    td, td * {
        font-size: 0.95rem !important;
        border-bottom: 1px solid #EEF0EC !important;
        background-color: #FFFFFF !important;
        color: #151618 !important;
    }
    
    /* 11. Header overrides */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none !important;}
    [data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 99999 !important;
    }
    hr {
        border-top: 1px solid #DCE0DA !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# ---------- SESSION STATE ----------
if "points" not in st.session_state: st.session_state.points = 0
if "butts" not in st.session_state: st.session_state.butts = 0
if "redeemed_rewards" not in st.session_state: st.session_state.redeemed_rewards = []
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_name" not in st.session_state: st.session_state.user_name = ""
if "last_processed_pic" not in st.session_state: st.session_state.last_processed_pic = None

# ---------- SIDEBAR (DARK THEME) ----------
st.sidebar.markdown('''
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 30px;">
    <div style="width: 30px; height: 30px; background-color: #FFFFFF; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
        <span style="color: #131514; font-weight: 800; font-size: 1.2rem;">E</span>
    </div>
    <span style="font-size: 1.4rem; font-weight: 700; color: #FFFFFF;">EcoButt</span>
</div>
''', unsafe_allow_html=True)

if st.session_state.logged_in:
    st.sidebar.markdown(f'''
    <div style="background-color: #2A2C2B; padding: 12px; border-radius: 12px; margin-bottom: 20px;">
        <div style="font-size: 0.8rem; color: #A0A2A0;">Current Session</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #FFFFFF;">{st.session_state.user_name}</div>
    </div>
    ''', unsafe_allow_html=True)

# Navigation
page = st.sidebar.radio(
    "",
    ["Login", "Dashboard", "AI Verification", "Rewards", "Impact Tracker", "Leaderboard", "Disposal Bin Map"]
)

st.sidebar.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div style='font-size: 0.8rem; color: #7A7D7A; text-align: center;'>v2.3 Build (AI Enhanced)</div>", 
    unsafe_allow_html=True
)

# ---------- LOGIN PAGE ----------
if page == "Login":
    
    st.write("")
    st.write("")
    
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    
    with col2:
        if st.session_state.logged_in:
            st.markdown(f'<div class="hero-title">Welcome back,<br><span class="hero-highlight">{st.session_state.user_name}</span></div>', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="custom-card" style="margin-top: 20px;">
                <div class="custom-card-title">Quick Status</div>
                <div style="display: flex; gap: 40px; margin-top: 15px;">
                    <div>
                        <span style="color: #7A7D7A; font-size: 0.9rem;">Available Points</span><br>
                        <span style="font-size: 2rem; font-weight: 700;">{st.session_state.points}</span>
                    </div>
                    <div>
                        <span style="color: #7A7D7A; font-size: 0.9rem;">Units Processed</span><br>
                        <span style="font-size: 2rem; font-weight: 700;">{st.session_state.butts}</span>
                    </div>
                </div>
                <p style="margin-top: 20px; color: #5A5D5A;">Select <b>Dashboard</b> from the side menu to view detailed analytics.</p>
            </div>
            ''', unsafe_allow_html=True)

            if st.button("End Session"):
                st.session_state.logged_in = False
                st.session_state.user_name = ""
                st.rerun()
        else:
            st.markdown('''
            <div class="hero-title">
                Managing <span class="hero-highlight">Your Waste</span><br>
                and Eco Rewards
            </div>
            ''', unsafe_allow_html=True)
            
            st.write("Access your dashboard to verify disposals and manage incentives.")
            st.write("") 
            
            with st.container():
                name = st.text_input("Full Name", placeholder="Enter your full name")
                email = st.text_input("Work Email", placeholder="name@company.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                
                st.write("") 
                if st.button("Sign In to Dashboard"):
                    if name and email and password:
                        st.session_state.logged_in = True
                        st.session_state.user_name = name
                        st.rerun() 
                    else:
                        st.warning("Please complete all fields to continue.")

            st.write("")
            st.markdown('''
            <div class="custom-card">
                <div class="custom-card-title">Platform Operations</div>
                EcoButt facilitates responsible corporate and community cigarette waste disposal. 
                Utilize our advanced AI verification system to scan your disposal and accrue reward points instantly.
            </div>
            ''', unsafe_allow_html=True)

# ---------- DASHBOARD ----------
elif page == "Dashboard":
    
    st.markdown('''
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <div class="hero-title" style="margin-bottom: 0 !important; font-size: 2.5rem !important;">Overview</div>
        <button style="background-color: #FFFFFF; border: 1px solid #DCE0DA; border-radius: 50px; padding: 10px 20px; font-weight: 500; color: #151618;">Download Report</button>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1: 
        st.metric("Total Points Earned", f"{st.session_state.points}")
    with col2: 
        st.metric("Units Processed", f"{st.session_state.butts}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns([1.5, 1])
    with col3:
        st.markdown(f'''
        <div class="custom-card" style="height: 100%;">
            <div class="custom-card-title">Operations Statistics</div>
            You have successfully verified <b>{st.session_state.butts} units</b> of waste.<br><br>
            <div style="background-color: #F8F9F8; padding: 20px; border-radius: 16px; margin-top: 15px;">
                <span style="font-size: 0.9rem; color: #7A7D7A;">Environmental Impact</span><br>
                <span style="font-size: 1.5rem; font-weight: 600;">{st.session_state.butts * 0.03:.2f}g Toxins Prevented</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="custom-card" style="height: 100%;"><div class="custom-card-title">Recent Activity</div>', unsafe_allow_html=True)
        if len(st.session_state.redeemed_rewards) == 0:
            st.markdown("<span style='color: #7A7D7A;'>No operations logged.</span>", unsafe_allow_html=True)
        else:
            for item in st.session_state.redeemed_rewards[-4:]:
                st.markdown(f'''
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px; border-bottom: 1px solid #F0F2ED; padding-bottom: 10px;">
                    <div style="width: 8px; height: 8px; background-color: #D6F169; border-radius: 50%;"></div>
                    <span style="font-weight: 500;">{item}</span>
                </div>
                ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- AI VERIFICATION (FULLY FIXED) ----------
elif page == "AI Verification":
    st.markdown('<div class="hero-title" style="font-size: 2.5rem !important;">Data Transfer & Scan</div>', unsafe_allow_html=True)
    st.write("Utilize your device camera for AI analysis.")
    st.write("")

    st.markdown('''
    <div class="custom-card">
        <div class="custom-card-title">Verification Protocol</div>
        Place the waste material clearly in the camera frame. The YOLO AI engine will process the image data and update your statistics upon successful verification.
    </div>
    ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        picture = st.camera_input("Scan Cigarette Bud")

        if picture:
            if not AI_AVAILABLE:
                st.error("Ultralytics is not installed. Run: pip install ultralytics")
            else:
                # Fetch cached model — does NOT reload on rerun
                model = load_model()

                if model is None:
                    st.error("AI Model could not be loaded. Ensure 'cigarette_model.pt' is in the app directory.")
                else:
                    # --- Anti-cheat: MD5 hash of raw image bytes (more reliable than picture.size) ---
                    # picture.size returns the FILE SIZE IN BYTES (not image dimensions),
                    # which can collide across different photos of similar file sizes.
                    # MD5 of the raw bytes is unique per image content.
                    pic_hash = hashlib.md5(picture.getvalue()).hexdigest()

                    image = Image.open(picture)
                    image_np = np.array(image)

                    # Run YOLO inference
                    results = model(image_np)

                    detected = False
                    confidence = 0.0

                    for r in results:
                        for box in r.boxes:
                            class_id = int(box.cls[0])
                            # Class 0 = cigarette butt
                            if class_id == 0:
                                detected = True
                                confidence = float(box.conf[0])
                                break
                        if detected:
                            break

                    # Always render annotated bounding-box image
                    annotated = results[0].plot()
                    st.image(annotated, caption="AI Detection Result", use_container_width=True)

                    if detected:
                        if st.session_state.last_processed_pic != pic_hash:
                            # New unique photo — award points
                            st.session_state.points += 5
                            st.session_state.butts += 1
                            st.session_state.last_processed_pic = pic_hash
                            st.success(f"AI verification successful! Cigarette bud detected (confidence: {confidence:.2f})")
                        else:
                            # Same photo submitted again
                            st.info("Operation already processed.")
                    else:
                        st.error("Verification failed — cigarette bud not detected.")

        st.markdown("<br><hr style='border-top: 1px solid #DCE0DA !important;'><br>", unsafe_allow_html=True)

        if st.button("Run Manual Scenario"):
            st.session_state.points += 5
            st.session_state.butts += 1
            st.success("Manual operation successful.")

# ---------- REWARDS ----------
elif page == "Rewards":
    st.markdown('<div class="hero-title" style="font-size: 2.5rem !important;">Variables & Rewards</div>', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div style="background-color: #D6F169; padding: 24px; border-radius: 24px; margin-bottom: 30px; display: inline-block;">
        <span style="font-size: 1rem; color: #131514; font-weight: 600;">Available Operations</span><br>
        <span style="font-size: 2.5rem; font-weight: 700; color: #131514;">{st.session_state.points} Points</span>
    </div>
    ''', unsafe_allow_html=True)

    rewards = {"Artisan Coffee": 20, "Premium Tea": 15, "Local Grocer": 30, "Food Delivery": 40}
    
    col1, col2 = st.columns([2, 1])
    with col1:
        for reward, cost in rewards.items():
            st.markdown(f'''
            <div class="custom-card" style="padding: 20px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-weight: 600; font-size: 1.1rem; color: #151618;">{reward}</span><br>
                        <span style="color: #7A7D7A; font-size: 0.9rem;">Cost: {cost} points</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            if st.button(f"Upgrade {reward}", key=reward):
                if st.session_state.points >= cost:
                    st.session_state.points -= cost
                    st.session_state.redeemed_rewards.append(reward)
                    st.success(f"Successfully applied: {reward}")
                    st.rerun()
                else:
                    st.error("Insufficient variables.")
    
# ---------- IMPACT TRACKER, LEADERBOARD, DISPOSAL BIN MAP ----------
elif page in ["Impact Tracker", "Leaderboard", "Disposal Bin Map"]:
    st.markdown(f'<div class="hero-title" style="font-size: 2.5rem !important;">{page}</div>', unsafe_allow_html=True)
    
    if page == "Impact Tracker":
        data = pd.DataFrame({
            "Operation Type": ["Units Processed", "Toxin Mitigation", "Active Users"],
            "Data Value": [f"{st.session_state.butts} units", f"{st.session_state.butts * 0.03:.2f}g", "1,250"]
        })
        st.dataframe(data, use_container_width=True, hide_index=True)
        
    elif page == "Leaderboard":
        leaderboard = pd.DataFrame({
            "Team Member": ["Arjun", "Priya", "Rahul", "Ananya", "You"],
            "Operations Score": [120, 110, 95, 80, st.session_state.points]
        })
        st.dataframe(
            leaderboard.sort_values(by="Operations Score", ascending=False).reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )
        
    elif page == "Disposal Bin Map":
        st.write("Installed hardware locations.")
        map_data = pd.DataFrame({
            "lat": [12.8231, 12.8250, 12.8272],
            "lon": [80.0444, 80.0460, 80.0431]
        })
        st.map(map_data, color="#D6F169")
