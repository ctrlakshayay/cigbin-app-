import streamlit as st
import pandas as pd

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(page_title="EcoButt App", layout="wide", initial_sidebar_state="expanded")

# ---------- PROFESSIONAL UI STYLE (SAGE GREEN & WHITE) ----------
def load_custom_css():
    st.markdown("""
    <style>
    /* 1. Import Professional App Font (Inter) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* 2. Global Typography & Background */
    html, body, [class*="css"], .stMarkdown p, .stText {
        font-family: 'Inter', sans-serif !important;
        color: #FFFFFF !important; /* Pure White text for high contrast */
    }

    /* Main App Background - Sage Green */
    .stApp {
        background-color: #7A9A82 !important; 
    }

    /* Sidebar Styling - Darker Sage for depth */
    [data-testid="stSidebar"] {
        background-color: #5A7B61 !important;
        border-right: 1px solid #4D6B53 !important;
    }

    /* 3. Typography Formatting */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important; 
        font-weight: 600 !important;
        letter-spacing: -0.5px !important;
    }

    /* Ensure all labels (radio, inputs) are white */
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] div {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    /* 4. Button Styling - White buttons with Sage text */
    .stButton>button {
        background-color: #FFFFFF !important; 
        color: #5A7B61 !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        border: 1px solid #FFFFFF !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #F0F4F1 !important; 
        color: #4D6B53 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        border-color: #F0F4F1 !important;
        transform: translateY(-1px) !important;
    }

    .stButton>button:active {
        transform: translateY(0px) !important;
    }

    /* 5. Input Fields & Dropdowns */
    .stTextInput>div>div>input {
        border-radius: 6px !important;
        border: 1px solid #8EAD96 !important;
        padding: 12px 14px !important;
        background-color: #65856D !important;
        color: #FFFFFF !important;
        transition: border-color 0.2s;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #FFFFFF !important;
        box-shadow: 0 0 0 1px #FFFFFF !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #C2D4C6 !important;
        opacity: 0.9 !important;
    }

    /* 6. Static Text Cards (HTML injections) */
    .custom-card {
        background-color: #65856D;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #72947A;
        margin-bottom: 24px;
        line-height: 1.6;
        color: #FFFFFF !important;
    }
    .custom-card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #FFFFFF !important;
        margin-bottom: 12px;
        border-bottom: 1px solid #72947A;
        padding-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* 7. Streamlit Metric Cards */
    [data-testid="metric-container"] {
        background-color: #65856D !important;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #72947A !important;
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 2.25rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #C2D4C6 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* 8. DataFrames & Tables */
    [data-testid="stTable"], [data-testid="stDataFrame"] {
        border-radius: 8px !important;
        overflow: hidden !important;
        border: 1px solid #72947A !important;
        background-color: #65856D !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }
    th {
        background-color: #5A7B61 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border-bottom: 1px solid #72947A !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    td {
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
        border-bottom: 1px solid #72947A !important;
        background-color: #65856D !important;
    }
    
    /* 9. Image Styling */
    [data-testid="stImage"] img {
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
        border: 1px solid #72947A !important;
    }

    /* 10. Hide default UI clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Ensure Header background matches */
    [data-testid="stHeader"] {
        background-color: rgba(122, 154, 130, 0.98) !important;
    }

    /* Dividers */
    hr {
        border-top: 1px solid #72947A !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# ---------- SESSION STATE ----------
if "points" not in st.session_state:
    st.session_state.points = 0

if "butts" not in st.session_state:
    st.session_state.butts = 0

if "redeemed_rewards" not in st.session_state:
    st.session_state.redeemed_rewards = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# Track the last scanned image to avoid double-awarding points on reruns
if "last_processed_pic" not in st.session_state:
    st.session_state.last_processed_pic = None

# ---------- SIDEBAR ----------
st.sidebar.title("Main Menu")

# Show greeting if logged in
if st.session_state.logged_in:
    st.sidebar.markdown(f"<h3 style='color: #FFFFFF; font-weight: 500; font-size: 1.2rem; margin-bottom: 0;'>Welcome, {st.session_state.user_name}</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='margin-top: 10px; margin-bottom: 15px; border-top: 1px solid #72947A;'>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["Login", "Dashboard", "Scan QR", "Rewards", "Impact Tracker", "Leaderboard", "Disposal Bin Map"]
)

st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div style='font-size: 0.75rem; color: #C2D4C6; text-align: center; text-transform: uppercase; letter-spacing: 0.5px;'>EcoButt Platform v1.4</div>", 
    unsafe_allow_html=True
)

# ---------- LOGIN PAGE ----------
if page == "Login":
    
    # Use columns to center the login form on wide screens
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.title("EcoButt Portal")
        
        if st.session_state.logged_in:
            st.success(f"Secure session active. User: **{st.session_state.user_name}**")
            if st.button("Secure Logout"):
                st.session_state.logged_in = False
                st.session_state.user_name = ""
                st.rerun()
        else:
            st.write("Please authenticate your credentials to access the system.")
            
            # Professional hero image for login
            st.image("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800&q=80", use_container_width=True)
            st.write("") # Spacer
            
            # Native form fields wrapped in standard container
            with st.container():
                name = st.text_input("Full Name")
                email = st.text_input("Corporate Email or Phone")
                password = st.text_input("Password", type="password")
                
                st.write("") # Spacer
                if st.button("Secure Login"):
                    if name and email and password:
                        st.session_state.logged_in = True
                        st.session_state.user_name = name
                        st.success("Authentication successful. Initializing dashboard...")
                        st.rerun() # Refresh app to update the sidebar greeting immediately
                    else:
                        st.warning("All fields are required for authentication.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Informational Card
        st.markdown('''
        <div class="custom-card">
            <div class="custom-card-title">System Overview</div>
            EcoButt facilitates responsible corporate and community cigarette waste disposal through a centralized incentive protocol.<br><br>
            Authorized personnel may dispose of waste in designated smart receptacles, utilize the embedded QR verification, 
            and accrue reward points redeemable across our certified partner network.
        </div>
        ''', unsafe_allow_html=True)


# ---------- DASHBOARD ----------
elif page == "Dashboard":
    st.title("Executive Dashboard")
    st.write("Real-time overview of your environmental contributions and asset ledger.")
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Points Available", st.session_state.points)
    with col2:
        st.metric("Total Units Recycled", st.session_state.butts)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns([2, 1])
    
    with col3:
        st.markdown('''
        <div class="custom-card">
            <div class="custom-card-title">Contribution Summary</div>
            You have successfully verified and recycled <b>{} units</b> of cigarette waste.<br><br>
            Through adherence to designated disposal protocols, you are actively mitigating toxic microplastic contamination and chemical runoff within municipal infrastructure.
        </div>
        '''.format(st.session_state.butts), unsafe_allow_html=True)
        
    with col4:
        st.markdown('''
        <div class="custom-card">
            <div class="custom-card-title">Reward Ledger</div>
        ''', unsafe_allow_html=True)
        
        if len(st.session_state.redeemed_rewards) == 0:
            st.write("No transactions recorded.")
        else:
            for item in st.session_state.redeemed_rewards:
                st.markdown(f"- **{item}**")
                
        st.markdown('</div>', unsafe_allow_html=True)


# ---------- QR SCAN ----------
elif page == "Scan QR":
    st.title("Hardware Verification")
    st.write("Utilize your device camera to register responsible disposal and update your ledger.")
    st.write("")

    st.markdown('''
    <div class="custom-card">
        <div class="custom-card-title">Standard Operating Procedure</div>
        1. Grant camera permissions when prompted by your browser.<br>
        2. Point your camera at the QR identifier matrix on the authorized EcoButt hardware.<br>
        3. Capture the image to automatically verify your geographic coordinates and credit your account.
    </div>
    ''', unsafe_allow_html=True)
    
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Streamlit's built-in camera input widget
        picture = st.camera_input("Capture QR Matrix")
        
        if picture:
            # Check if this exact picture has already been processed to prevent point duplication
            if st.session_state.last_processed_pic != picture.size:
                st.session_state.points += 5
                st.session_state.butts += 1
                st.session_state.last_processed_pic = picture.size
                st.success("Image processed. Verification confirmed. Ledger updated successfully.")
            else:
                # Picture is in memory, but already processed
                st.success("This scan has already been verified and credited.")
                
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        
        # Fallback manual button
        st.write("Camera unavailable? Use manual override:")
        if st.button("Simulate Manual Verification"):
            st.session_state.points += 5
            st.session_state.butts += 1
            st.success("Manual Verification confirmed. Ledger updated successfully.")

# ---------- REWARDS ----------
elif page == "Rewards":
    st.title("Partner Network")
    st.write("Allocate your accumulated points toward partner incentives.")
    
    col_bal, col_hist = st.columns([2, 1])
    
    with col_bal:
        st.markdown(f"### **Ledger Balance:** {st.session_state.points} Points")
        st.write("")

        rewards = {
            "Artisan Coffee Voucher": 20,
            "Premium Tea Voucher": 15,
            "Local Grocer Discount": 30,
            "Food Delivery Credit": 40
        }

        st.markdown("### Available Incentives")
        
        for reward, cost in rewards.items():
            with st.container():
                rc1, rc2 = st.columns([3, 1])
                with rc1:
                    st.markdown(f"<span style='font-weight: 600; font-size: 1.1rem; color: #FFFFFF;'>{reward}</span><br><span style='color: #C2D4C6;'>Required: {cost} points</span>", unsafe_allow_html=True)
                with rc2:
                    if st.button("Authorize Transfer", key=reward):
                        if st.session_state.points >= cost:
                            st.session_state.points -= cost
                            st.session_state.redeemed_rewards.append(reward)
                            st.success(f"Transfer successful: {reward}")
                        else:
                            st.error("Transaction failed: Insufficient ledger balance.")
                st.divider()
                
    with col_hist:
        st.markdown('''
        <div class="custom-card">
            <div class="custom-card-title">Transaction History</div>
        ''', unsafe_allow_html=True)
        
        if len(st.session_state.redeemed_rewards) == 0:
            st.write("No prior transactions.")
        else:
            for item in reversed(st.session_state.redeemed_rewards):
                st.markdown(f"- {item}")
                
        st.markdown('</div>', unsafe_allow_html=True)


# ---------- IMPACT TRACKER ----------
elif page == "Impact Tracker":
    st.title("Global Analytics")
    st.write("Real-time telemetry on environmental preservation efforts.")
    st.write("")

    data = pd.DataFrame({
        "Metric Classification": [
            "Total Units Processed",
            "Estimated Toxin Mitigation",
            "Active Network Nodes (Users)"
        ],
        "Recorded Value": [
            f"{st.session_state.butts} units",
            f"{st.session_state.butts * 0.03:.2f} grams",
            "1,250 active"
        ]
    })

    st.dataframe(data, use_container_width=True, hide_index=True)


# ---------- LEADERBOARD ----------
elif page == "Leaderboard":
    st.title("Network Rankings")
    st.write("Top contributing nodes within your regional sector.")
    st.write("")

    leaderboard = pd.DataFrame({
        "Participant ID": ["Arjun", "Priya", "Rahul", "Ananya", "Current Session"],
        "Verified Points": [120, 110, 95, 80, st.session_state.points]
    })
    
    leaderboard = leaderboard.sort_values(by="Verified Points", ascending=False).reset_index(drop=True)

    st.dataframe(leaderboard, use_container_width=True, hide_index=True)


# ---------- MAP ----------
elif page == "Disposal Bin Map":
    st.title("Infrastructure Telemetry")
    st.write("Geographic mapping of deployed disposal hardware assets.")
    st.write("")

    # Map coordinates
    map_data = pd.DataFrame({
        "lat": [12.8231, 12.8250, 12.8272],
        "lon": [80.0444, 80.0460, 80.0431]
    })

    # Darker map dots for contrast on light map tiles
    st.map(map_data, color="#2A3B30")
