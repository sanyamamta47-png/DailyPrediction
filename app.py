import streamlit as st
import datetime
import razorpay
from supabase import create_client, Client 

# --- CONFIGURATION & SECRETS CONFIG ---
PAYMENT_GATEWAY_URL = "https://rzp.io/rzp/7pdLRmod" 

RAZORPAY_KEY_ID = st.secrets["RAZORPAY_KEY_ID"]
RAZORPAY_KEY_SECRET = st.secrets["RAZORPAY_KEY_SECRET"]

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

# Initialize wide canvas
st.set_page_config(page_title="Divine Aura Portal", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Lato:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Lato', sans-serif; background-color: #FAF9FB; }
    
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1150px !important; 
        margin: 0 auto !important;
    }
    
    h1, h2, h3, h4, h5, h6 { font-family: 'Playfair Display', serif !important; color: #4A1E63 !important; font-weight: 700; }

    .hero-title {
        text-align: center; font-size: 3.2rem; font-weight: 800; font-family: 'Playfair Display', serif;
        background: linear-gradient(45deg, #4A1E63, #E0B1CB);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px;
    }
    .hero-subtitle {
        text-align: center; font-size: 1.1rem; color: #D4AF37; margin-bottom: 35px;
        letter-spacing: 3px; text-transform: uppercase; font-weight: 600;
    }

    .stButton>button { 
        background: linear-gradient(135deg, #6C25A3 0%, #E0B1CB 100%); 
        color: white !important; border: 2px solid #D4AF37; 
        box-shadow: 0 4px 12px rgba(108, 37, 163, 0.15); 
        border-radius: 8px; font-weight: 700; text-transform: uppercase;
        letter-spacing: 1px; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); 
        padding: 12px 0; width: 100%;
    }
    .stButton>button:hover { 
        background: linear-gradient(135deg, #E0B1CB 0%, #6C25A3 100%); 
        transform: translateY(-1px); box-shadow: 0 6px 18px rgba(108, 37, 163, 0.25);
    }
    
    .translate-btn>button {
        background: transparent !important; color: #6C25A3 !important; border: 2px solid #6C25A3 !important;
        box-shadow: none !important; width: auto !important; padding: 5px 20px !important; margin-bottom: 15px;
    }
    .translate-btn>button:hover {
        background: #6C25A3 !important; color: white !important;
    }

    .prediction-card { 
        background-color: #FFFFFF; border-top: 3px solid #D4AF37; border-radius: 8px; 
        padding: 22px; margin-bottom: 20px; box-shadow: 0 5px 15px rgba(93, 42, 130, 0.04); 
        font-size: 1.08em; line-height: 1.65; color: #444444;
    }
    
    .metric-row-box {
        background-color: #FFFFFF; border-left: 5px solid #6C25A3;
        border-right: 1px solid rgba(224, 177, 203, 0.3); border-top: 1px solid rgba(224, 177, 203, 0.3);
        border-bottom: 1px solid rgba(224, 177, 203, 0.3); padding: 18px 22px; border-radius: 6px;
        margin-bottom: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.02); display: flex;
        justify-content: space-between; align-items: center;
    }
    .metric-title-sub { font-size: 0.9rem; color: #8E7C9D; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; }
    .metric-value-large { font-size: 2.8rem; font-family: 'Playfair Display', serif; color: #D4AF37; font-weight: 800; }
    .category-header { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; color: #4A1E63; margin-bottom: 10px; border-bottom: 1px solid rgba(224, 177, 203, 0.3); padding-bottom: 6px; }
    .blockquote-style { background-color: #FFF9FA; border: 1px dashed #E0B1CB; border-left: 5px solid #D4AF37; padding: 22px; border-radius: 4px; font-style: italic; color: #4A1E63; font-size: 1.25rem; font-family: 'Playfair Display', serif; text-align: center; margin: 30px 0; line-height: 1.5; }
    .price-tag { font-family: 'Playfair Display', serif; font-size: 26px; color: #D4AF37; font-weight: 800; margin-bottom: 15px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR LANGUAGE ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'

# --- UI DICTIONARY (Dual Language Support) ---
UI = {
    'EN': {
        'welcome': "Welcome",
        'blueprint_title': "Core Blueprint Matrix",
        'driver': "Mulank (Driver Number)",
        'ruler': "Ruler",
        'traits': "Traits",
        'destiny': "Bhagyank (Destiny Path)",
        'calc': "Calculation",
        'year_cycle': "Personal Year Cycle",
        'focus': "Focus",
        'guide_title': "Personalized Energy Guide",
        'today_title': "Today's Readings (Personal Day",
        'career': "💼 Career & Wealth Outlook",
        'relationship': "💖 Relationship & Harmony",
        'health': "🌱 Health & Vitality Rhythm",
        'matrix_title': "Chart Matrix Plane Alignment",
        'direct_plane': "The Direct Plane",
        'missing_elements': "The Balance Factors (Missing Elements",
        'action_items': "Daily Action Items",
        'close_btn': "Close Secure Session",
        'single_digit_msg': "Since your birth date is a single digit (**{val}**), your core ruling energy is beautifully straightforward and direct.",
        'double_digit_msg': "Since your birth date is a double digit (**{val}**), your driver energy blends to reveal your core foundation path.",
        'lucky_num': "Lucky Numbers",
        'lucky_col': "Lucky Colors",
        'power_dir': "Power Direction",
        'power_hr': "Power Hours Today",
        'avoid': "Avoid",
        'facing': "Facing"
    },
    'HI': {
        'welcome': "स्वागत है",
        'blueprint_title': "आपका मूल ब्लूप्रिंट मैट्रिक्स",
        'driver': "मूलांक (Driver Number)",
        'ruler': "शासक ग्रह",
        'traits': "विशेषताएं",
        'destiny': "भाग्यांक (Destiny Path)",
        'calc': "गणना",
        'year_cycle': "व्यक्तिगत वर्ष चक्र",
        'focus': "मुख्य बिंदु",
        'guide_title': "व्यक्तिगत ऊर्जा गाइड",
        'today_title': "आज की भविष्यवाणी (व्यक्तिगत दिन",
        'career': "💼 करियर और धन",
        'relationship': "💖 रिश्ते और परिवार",
        'health': "🌱 स्वास्थ्य और ऊर्जा",
        'matrix_title': "चार्ट मैट्रिक्स संरेखण",
        'direct_plane': "प्रत्यक्ष तल (Direct Plane)",
        'missing_elements': "संतुलन कारक (लापता अंक",
        'action_items': "आज के कार्य बिंदु",
        'close_btn': "सुरक्षित सत्र बंद करें",
        'single_digit_msg': "चूंकि आपकी जन्मतिथि एक अंक (**{val}**) है, इसलिए आपकी मुख्य ऊर्जा बिल्कुल स्पष्ट और सीधी है।",
        'double_digit_msg': "चूंकि आपकी जन्मतिथि दो अंकों (**{val}**) की है, इसलिए आपकी ऊर्जा आपके मूल पथ को प्रकट करने के लिए मिश्रित होती है।",
        'lucky_num': "शुभ अंक",
        'lucky_col': "शुभ रंग",
        'power_dir': "शुभ दिशा",
        'power_hr': "आज का शुभ समय",
        'avoid': "बचें",
        'facing': "दिशा"
    }
}

# --- ENGLISH PREDICTION MATRIX ---
NUMEROLOGY_DATA_EN = {
    1: {"ruler": "Sun (Surya)", "direction": "East", "colors": "Ruby Red, Gold", "hours": "6:00 AM - 8:30 AM", "numbers": "1, 5, 3", "avoid": "8, 7", "traits": "leadership, unique authority, logic, and independent willpower.", "year_text": "major personal breakthroughs, setting distinct baselines, and fresh initiatives.", "career": "A day for high-impact initiative. Perfect for launching projects, pitching concepts, or asserting your workspace authority. Take the lead on calculated risks.", "relationship": "Focus on setting healthy boundaries while maintaining absolute clarity. Speak your truth directly, but avoid dominating mutual family conversations.", "health": "Surges with vital physical energy. Excellent day to kickstart a workout structure. Keep inflammation levels in check by drinking plenty of water.", "affirmation": "I step confidently into my authentic power, directing my career and life with absolute clarity.", "tips": ["Initiate one foundational routine business habit today.", "Avoid micro-managing administrative tasks."]},
    2: {"ruler": "Moon (Chandra)", "direction": "North-West", "colors": "Cream, White, Soft Sage", "hours": "7:30 AM - 9:30 AM", "numbers": "2, 1, 5", "avoid": "9, 4", "traits": "profound intuition, diplomatic balance, fine detail analysis, and creative sensitivity.", "year_text": "deep patience, stabilizing critical partnerships, and allowing your seeds to root quietly.", "career": "Collaborative efforts yield the best returns today. Work in pairs, refine documentation layouts quietly, and avoid forcing immediate closing agreements.", "relationship": "A beautiful day for gentle harmony and emotional connection. Listen carefully to loved ones; your natural empathy acts as a major healing balm today.", "health": "Mental calm is your priority. Avoid emotional stress loops that could impact your digestion. Unwind near peaceful environments or practice breathwork.", "affirmation": "I ground my power in deep patience, knowing my intuitive choices reveal the perfect direction.", "tips": ["Dedicate 10 minutes to organizing your creative workspace layout.", "Honor a quiet gut instinct over fast-moving logical debates today."]},
    3: {"ruler": "Jupiter (Guru)", "direction": "North-East", "colors": "Yellow, Saffron, Honey Gold", "hours": "9:00 AM - 11:00 AM", "numbers": "3, 5, 7", "avoid": "6, 8", "traits": "higher wisdom, expansive learning, communication mastery, and creative solutions.", "year_text": "creative expansion, social visibility, building brand frameworks, and expressive growth.", "career": "Your expression vector is peak today. Excellent window for writing promotional copy, presenting business plans, and brainstorming scaling strategies.", "relationship": "Joyful, highly expressive energy dominates. Share your dreams with your inner circle. Socializing or group gatherings bring inspiring, supportive vibes.", "health": "Energy levels are excellent, but ensure you do not overindulge in heavy or overly sweet foods. Keep liver function optimized with fresh green drinks.", "affirmation": "My higher wisdom steers my daily execution paths, effortlessly attracting expansive breakthroughs.", "tips": ["Document three major brand expansion thoughts.", "Express your creative designs visually on landing frames today."]},
    4: {"ruler": "Rahu", "direction": "South-West", "colors": "Electric Blue, Deep Charcoal", "hours": "4:00 PM - 6:00 PM", "numbers": "4, 5, 6", "avoid": "2, 9", "traits": "structural system engineering, organizing data, radical breakthroughs, and raw execution discipline.", "year_text": "building stable foundations, clean tracking configurations, and secure data storage systems.", "career": "Focus heavily on organizing backend system structures, fixing bugs, and tackling structural details. Hard work pays off through methodical tracking.", "relationship": "Clear up structural misunderstandings by sticking to objective facts. Avoid making sudden, unpredictable statements to your core connections.", "health": "Pay attention to skeletal structures, posture, or muscle tension. Incorporate regular stretching routines during heavy tech screen time intervals.", "affirmation": "I construct systematic architectures that endure, converting strategies into daily functional realities.", "tips": ["Re-organize old system file data trees or storage directories.", "Break long projects into atomic, executable checklists."]},
    5: {"ruler": "Mercury (Budh)", "direction": "North", "colors": "Emerald Green, Mint, Aqua", "hours": "11:00 AM - 1:00 PM", "numbers": "5, 1, 6", "avoid": "None", "traits": "commercial monetization strategies, speed, analytical agility, and high-frequency communication.", "year_text": "rapid business scaling, flexible adjustments, and major market networking setups.", "career": "A incredibly fast-paced and lucky day for commercial operations. Perfect for finalization, run-time scripts, web deployments, and business communication shifts.", "relationship": "Communication is lively and fun. You easily articulate your ideas, making it a great day for lighthearted social catch-ups or meeting new people.", "health": "Your nervous system might feel a bit overloaded. Take conscious tech-free microbreaks to calm your mind and prevent sleep cycle disruptions.", "affirmation": "I adapt dynamically to all shifts with accurate clarity, processing commercial options with ease.", "tips": ["Run performance diagnostic tests on active applications.", "Connect with an active partner regarding digital asset trends."]},
    6: {"ruler": "Venus (Shukra)", "direction": "South-East", "colors": "Bright White, Light Blue, Rose Pink", "hours": "2:00 PM - 4:30 PM", "numbers": "6, 5, 8", "avoid": "3, 4", "traits": "premium aesthetic presentation, luxury brand coordination, family care, and creative symmetry.", "year_text": "investing in home office aesthetics, family bonds, and cultivating beautiful lifestyle comforts.", "career": "Focus heavily on front-end aesthetics, presentation slides, or customer support touchpoints. Visual beauty and balance drive sales metrics today.", "relationship": "A wonderful day for nurturing relationships. Focus on home comfort, resolving past domestic friction, and treating your partner to an upscale experience.", "health": "Focus on skincare and maintaining a clean diet. Enhance your physical vitality by introducing pleasant, comforting items like botanical essential oils.", "affirmation": "I attract abundance, symmetry, and premium aesthetics into my secure workspace and home.", "tips": ["Review user interface color balancing points on layouts.", "Nurture close connections by showing genuine appreciation."]},
    7: {"ruler": "Ketu", "direction": "North-East", "colors": "Pastel Shades, Light Yellow", "hours": "12:00 PM - 2:00 PM", "numbers": "7, 3, 5", "avoid": "1, 8", "traits": "deep pattern analysis, research methodologies, spiritual discovery, and internal logic auditing.", "year_text": "strategic data analysis, studying alternative sciences, and deliberate isolation loops.", "career": "Ideal day for quiet deep work, data pattern auditing, or algorithmic optimization. Keep your head down and let your analytical focus shine.", "relationship": "You may feel quiet and introverted today. Communicate your need for space gently to your family to avoid giving off an impression of distance.", "health": "Excellent for mental well-being and meditation. Align your body's rhythm through relaxing sound frequencies or quiet, mindful walks.", "affirmation": "I trust my deep inner perspective to solve complex problems, aligning with absolute universal truths.", "tips": ["Step away from screens completely during your assigned power hour.", "Audit system patterns methodically to ensure error-free logic."]},
    8: {"ruler": "Saturn (Shani)", "direction": "West", "colors": "Dark Blue, Royal Purple, Deep Teal", "hours": "5:00 PM - 7:00 PM", "numbers": "8, 5, 6", "avoid": "1, 4", "traits": "administrative authority, long-term resource scaling, justice, and heavy karmic execution templates.", "year_text": "high-stakes material realization, investment control, scale, and exercising structural authority.", "career": "A major execution day. Align your metrics, optimize business financial records, and make big moves. Your capacity to materialise visions is at an all-time high.", "relationship": "Focus on stability and long-term security. Simple, reliable commitments go a long way in strengthening family trust right now.", "health": "Pay close attention to your joints, knees, and teeth. Support your physical endurance by keeping your calcium levels optimized and staying active.", "affirmation": "I am the deliberate architect of my abundance. I ground my power in consistent execution metrics.", "tips": ["Audit weekly resource budgets to optimize your business runway.", "Commit directly to completing your highest friction milestone today."]},
    9: {"ruler": "Mars (Mangal)", "direction": "South", "colors": "Crimson Red, Rich Coral", "hours": "8:30 AM - 10:30 AM", "numbers": "9, 1, 3", "avoid": "2, 4", "traits": "finish-line determination, courageous leadership, clearing technical debts, and humanitarian problem-solving.", "year_text": "wrapping up old legacy dependencies, full system cleaning, and freeing up storage structures.", "career": "A powerful day for clearing outstanding queues. Complete pending code scripts, close legacy deals, and clear away outdated system methods.", "relationship": "High passion but watch out for short tempers. Channel any intense energy into productive creative tasks instead of minor arguments.", "health": "Excellent physical vitality. Great day for intense cardio, yoga, or martial art drills. Avoid burns, cuts, or sharp instruments by staying present.", "affirmation": "I complete pending cycles cleanly with absolute power, stepping forward into a fresh chapter with grace.", "tips": ["Purge expired storage files and clean out your workspace clutter.", "Safeguard personal boundaries from low-vibration debates."]}
}

# --- HINDI PREDICTION MATRIX ---
NUMEROLOGY_DATA_HI = {
    1: {"ruler": "सूर्य (Sun)", "direction": "पूर्व (East)", "colors": "रूबी लाल, सुनहरा", "hours": "सुबह 6:00 - सुबह 8:30", "numbers": "1, 5, 3", "avoid": "8, 7", "traits": "नेतृत्व, अद्वितीय अधिकार, तार्किक क्षमता और स्वतंत्र इच्छाशक्ति।", "year_text": "व्यक्तिगत सफलता, नए प्रतिमान स्थापित करने और नई शुरुआत का समय।", "career": "उच्च प्रभाव वाली पहल के लिए आज का दिन बेहतरीन है। प्रोजेक्ट लॉन्च करने या अपने विचारों को आत्मविश्वास के साथ प्रस्तुत करने के लिए आदर्श दिन है।", "relationship": "पूर्ण स्पष्टता बनाए रखते हुए स्वस्थ सीमाएँ निर्धारित करने पर ध्यान दें। अपनी बात सीधे कहें, लेकिन परिवार पर हावी होने से बचें।", "health": "शारीरिक ऊर्जा उच्च रहेगी। व्यायाम शुरू करने के लिए उत्कृष्ट दिन है। खूब पानी पीकर शरीर को हाइड्रेटेड रखें।", "affirmation": "मैं पूर्ण स्पष्टता और आत्मविश्वास के साथ अपने जीवन और करियर को आगे बढ़ाता हूँ।", "tips": ["आज एक नई व्यावसायिक दिनचर्या शुरू करें।", "प्रशासनिक कार्यों में बहुत ज्यादा उलझने से बचें।"]},
    2: {"ruler": "चंद्रमा (Moon)", "direction": "उत्तर-पश्चिम", "colors": "क्रीम, सफेद, हल्का हरा", "hours": "सुबह 7:30 - सुबह 9:30", "numbers": "2, 1, 5", "avoid": "9, 4", "traits": "गहरी अंतर्ज्ञान, कूटनीतिक संतुलन, और रचनात्मक संवेदनशीलता।", "year_text": "धैर्य, महत्वपूर्ण साझेदारियों को स्थिर करना और अपने विचारों को पनपने देना।", "career": "सहयोगात्मक कार्य आज सर्वोत्तम परिणाम देंगे। टीम के साथ काम करें, योजनाओं को परिष्कृत करें और तुरंत निर्णय लेने से बचें।", "relationship": "सौम्य सद्भाव और भावनात्मक जुड़ाव के लिए एक सुंदर दिन। प्रियजनों की बात ध्यान से सुनें; आपकी सहानुभूति आज बहुत काम आएगी।", "health": "मानसिक शांति आपकी प्राथमिकता है। तनाव से बचें जो आपके पाचन को प्रभावित कर सकता है। शांतिपूर्ण वातावरण में रहें या ध्यान करें।", "affirmation": "मैं ब्रह्मांडीय समय पर भरोसा करता हूँ और धैर्य के साथ अपनी शक्ति स्थापित करता हूँ।", "tips": ["अपने रचनात्मक कार्यक्षेत्र को व्यवस्थित करने के लिए 10 मिनट निकालें।", "आज तार्किक बहस के बजाय अपनी सहज वृत्ति (intuition) का सम्मान करें।"]},
    3: {"ruler": "गुरु (Jupiter)", "direction": "उत्तर-पूर्व", "colors": "पीला, केसरिया, सुनहरा", "hours": "सुबह 9:00 - सुबह 11:00", "numbers": "3, 5, 7", "avoid": "6, 8", "traits": "उच्च ज्ञान, संचार में महारत, और रचनात्मक समाधान।", "year_text": "रचनात्मक विस्तार, सामाजिक दृश्यता, ब्रांड संरचना का निर्माण और विकास।", "career": "विचारों को व्यक्त करने के लिए आज का दिन चरम पर है। प्रचार सामग्री लिखने, व्यवसाय योजना प्रस्तुत करने और नई रणनीतियों के लिए बेहतरीन समय है।", "relationship": "आनंददायक और अत्यधिक अभिव्यंजक ऊर्जा हावी है। अपने सपनों को अपने करीबियों के साथ साझा करें। सामाजिक मेलजोल से प्रेरणा मिलेगी।", "health": "ऊर्जा का स्तर उत्कृष्ट है, लेकिन बहुत अधिक मीठे या भारी भोजन से बचें। हरी सब्जियों के साथ लिवर के कार्य को अनुकूलित करें।", "affirmation": "मेरा उच्च ज्ञान मेरे दैनिक कार्यों का मार्गदर्शन करता है और आसानी से सफलताओं को आकर्षित करता है।", "tips": ["अपने ब्रांड के विस्तार के तीन प्रमुख विचार लिखें।", "आज अपने रचनात्मक विचारों को दृश्य रूप (visually) में व्यक्त करें।"]},
    4: {"ruler": "राहु (Rahu)", "direction": "दक्षिण-पश्चिम", "colors": "इलेक्ट्रिक ब्लू, गहरा स्लेटी", "hours": "शाम 4:00 - शाम 6:00", "numbers": "4, 5, 6", "avoid": "2, 9", "traits": "संरचनात्मक प्रणाली इंजीनियरिंग, डेटा व्यवस्थित करना, और निष्पादन अनुशासन।", "year_text": "स्थिर नींव का निर्माण, साफ़ ट्रैकिंग कॉन्फ़िगरेशन, और सुरक्षित डेटा सिस्टम।", "career": "बैकएंड सिस्टम संरचनाओं को व्यवस्थित करने, बग फिक्सिंग और संरचनात्मक विवरणों पर भारी ध्यान दें। कड़ी मेहनत का फल आज मिलेगा।", "relationship": "तथ्यों पर टिके रहकर संरचनात्मक गलतफहमियों को दूर करें। अपने करीबियों से अचानक या अप्रत्याशित बयान देने से बचें।", "health": "हड्डियों की संरचना, मुद्रा (posture) या मांसपेशियों के तनाव पर ध्यान दें। स्क्रीन टाइम के बीच नियमित स्ट्रेचिंग करें।", "affirmation": "मैं व्यवस्थित वास्तुकला का निर्माण करता हूँ जो लंबे समय तक चलती है।", "tips": ["पुरानी डेटा फ़ाइलों या स्टोरेज को पुनर्व्यवस्थित करें।", "लंबे प्रोजेक्ट्स को छोटे और निष्पादन योग्य (executable) कार्यों में विभाजित करें।"]},
    5: {"ruler": "बुध (Mercury)", "direction": "उत्तर (North)", "colors": "पन्ना हरा, एक्वा", "hours": "सुबह 11:00 - दोपहर 1:00", "numbers": "5, 1, 6", "avoid": "कोई नहीं", "traits": "व्यावसायिक मुद्रीकरण रणनीतियाँ, गति, विश्लेषणात्मक चपलता, और उच्च संचार।", "year_text": "तेजी से व्यापार विस्तार, लचीले समायोजन, और प्रमुख बाजार नेटवर्किंग।", "career": "व्यावसायिक कार्यों के लिए अविश्वसनीय रूप से तेज और भाग्यशाली दिन। स्क्रिप्ट परिनियोजन (deployments) और व्यावसायिक सौदों के लिए बिल्कुल सही।", "relationship": "संचार जीवंत और मजेदार है। आप आसानी से अपने विचारों को स्पष्ट कर सकते हैं; नए लोगों से मिलने के लिए बहुत अच्छा दिन है।", "health": "आपके तंत्रिका तंत्र (nervous system) पर दबाव पड़ सकता है। अपने दिमाग को शांत करने के लिए जानबूझकर टेक-फ्री ब्रेक लें।", "affirmation": "मैं सटीक स्पष्टता के साथ सभी बदलावों को अपनाता हूँ और आसानी से व्यावसायिक विकल्पों को संसाधित करता हूँ।", "tips": ["सक्रिय एप्लिकेशन पर प्रदर्शन डायग्नोस्टिक परीक्षण चलाएं।", "डिजिटल रुझानों (trends) के संबंध में एक सक्रिय भागीदार से जुड़ें।"]},
    6: {"ruler": "शुक्र (Venus)", "direction": "दक्षिण-पूर्व", "colors": "चमकीला सफेद, हल्का नीला, गुलाबी", "hours": "दोपहर 2:00 - शाम 4:30", "numbers": "6, 5, 8", "avoid": "3, 4", "traits": "प्रीमियम सौंदर्य प्रस्तुति, लक्जरी ब्रांड समन्वय, पारिवारिक देखभाल, और समरूपता।", "year_text": "घर के एस्थेटिक्स में निवेश, पारिवारिक बंधन, और जीवन शैली को सुंदर बनाना।", "career": "फ्रंट-एंड एस्थेटिक्स, प्रेजेंटेशन स्लाइड या कस्टमर सपोर्ट पर पूरा ध्यान दें। दृश्य सौंदर्य (visual beauty) आज बिक्री मेट्रिक्स को बढ़ाएगा।", "relationship": "रिश्तों को संवारने के लिए एक शानदार दिन। घर के आराम पर ध्यान दें, घरेलू घर्षण को हल करें और अपने साथी के साथ अच्छा समय बिताएं।", "health": "त्वचा की देखभाल और साफ आहार पर ध्यान दें। आवश्यक तेलों (essential oils) जैसी सुखद चीजों का उपयोग करके अपनी ऊर्जा बढ़ाएं।", "affirmation": "मैं अपने सुरक्षित कार्यक्षेत्र और घर में प्रचुरता, समरूपता और सौंदर्य को आकर्षित करता हूँ।", "tips": ["लेआउट पर यूजर इंटरफेस और रंग संतुलन (color balance) की समीक्षा करें।", "सच्ची प्रशंसा दिखाकर करीबी रिश्तों को संवारें।"]},
    7: {"ruler": "केतु (Ketu)", "direction": "उत्तर-पूर्व", "colors": "पेस्टल शेड्स, हल्का पीला", "hours": "दोपहर 12:00 - दोपहर 2:00", "numbers": "7, 3, 5", "avoid": "1, 8", "traits": "गहन पैटर्न विश्लेषण, अनुसंधान के तरीके, आध्यात्मिक खोज, और तार्किक ऑडिटिंग।", "year_text": "रणनीतिक डेटा विश्लेषण, वैकल्पिक विज्ञान का अध्ययन, और जानबूझकर अलगाव।", "career": "गहन कार्य, डेटा पैटर्न ऑडिटिंग या एल्गोरिथम अनुकूलन के लिए आदर्श दिन। अपना सिर नीचे रखें और अपनी विश्लेषणात्मक क्षमता को चमकने दें।", "relationship": "आज आप शांत और अंतर्मुखी महसूस कर सकते हैं। अपनी जगह की आवश्यकता के बारे में परिवार को प्यार से बताएं ताकि वे गलत ना समझें।", "health": "मानसिक भलाई और ध्यान के लिए उत्कृष्ट। शांत संगीत या माइंडफुल वॉक के माध्यम से अपने शरीर की लय को संरेखित करें।", "affirmation": "मैं जटिल समस्याओं को हल करने के लिए अपने गहरे आंतरिक दृष्टिकोण पर भरोसा करता हूँ।", "tips": ["अपने 'पावर आवर' के दौरान स्क्रीन से पूरी तरह दूर रहें।", "त्रुटि-मुक्त तर्क (error-free logic) सुनिश्चित करने के लिए सिस्टम पैटर्न का ऑडिट करें।"]},
    8: {"ruler": "शनि (Saturn)", "direction": "पश्चिम (West)", "colors": "गहरा नीला, शाही बैंगनी", "hours": "शाम 5:00 - शाम 7:00", "numbers": "8, 5, 6", "avoid": "1, 4", "traits": "प्रशासनिक अधिकार, दीर्घकालिक संसाधन स्केलिंग, न्याय, और भारी कर्म निष्पादन।", "year_text": "उच्च-स्तरीय भौतिक प्राप्ति, निवेश नियंत्रण, और संरचनात्मक अधिकार का प्रयोग।", "career": "एक प्रमुख निष्पादन (execution) का दिन। अपने मेट्रिक्स को संरेखित करें, वित्तीय रिकॉर्ड को अनुकूलित करें और बड़े कदम उठाएं।", "relationship": "स्थिरता और दीर्घकालिक सुरक्षा पर ध्यान दें। सरल और विश्वसनीय वादे इस समय परिवार का विश्वास मजबूत करने में बहुत काम आएंगे।", "health": "अपने जोड़ों, घुटनों और दांतों पर पूरा ध्यान दें। कैल्शियम के स्तर को अनुकूलित करके और सक्रिय रहकर अपनी शारीरिक सहनशक्ति का समर्थन करें।", "affirmation": "मैं अपनी प्रचुरता का जानबूझकर वास्तुकार हूँ। मैं अपनी शक्ति को निरंतर निष्पादन में लगाता हूँ।", "tips": ["अपने व्यवसाय को अनुकूलित करने के लिए साप्ताहिक बजट का ऑडिट करें।", "आज अपने सबसे कठिन या लंबित कार्य को पूरा करने के लिए सीधे प्रतिबद्ध हों।"]},
    9: {"ruler": "मंगल (Mars)", "direction": "दक्षिण (South)", "colors": "गहरा लाल, मूंगा (Coral)", "hours": "सुबह 8:30 - सुबह 10:30", "numbers": "9, 1, 3", "avoid": "2, 4", "traits": "फिनिश-लाइन दृढ़ संकल्प, साहसी नेतृत्व, और मानवीय समस्या-समाधान।", "year_text": "पुरानी विरासत निर्भरता को लपेटना, पूर्ण सिस्टम सफाई, और स्टोरेज को खाली करना।", "career": "बकाया कतारों को साफ करने के लिए एक शक्तिशाली दिन। लंबित कोड स्क्रिप्ट को पूरा करें, पुराने सौदों को बंद करें और पुराने तरीकों को हटा दें।", "relationship": "उच्च जुनून लेकिन छोटे गुस्से से सावधान रहें। किसी भी तीव्र ऊर्जा को छोटी-मोटी बहस के बजाय रचनात्मक कार्यों में लगाएं।", "health": "शारीरिक ऊर्जा शानदार रहेगी। गहन कार्डियो, योग या मार्शल आर्ट के लिए बढ़िया दिन है। सावधान रहकर जलने या कटने से बचें।", "affirmation": "मैं पूर्ण शक्ति के साथ लंबित चक्रों को पूरी तरह समाप्त करता हूँ, और अनुग्रह के साथ एक नए अध्याय में कदम रखता हूँ।", "tips": ["समाप्त हो चुकी स्टोरेज फ़ाइलों को हटा दें और अपने कार्यक्षेत्र की अव्यवस्था को साफ़ करें।", "नकारात्मक बहस से अपनी व्यक्तिगत सीमाओं की रक्षा करें।"]}
}

# --- SECURE VERIFICATION ENGINE ---
def is_payment_valid(payment_id):
    if "YOUR_KEY_ID" in RAZORPAY_KEY_ID:
        return True, "Bypass mode active"
    try:
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        payment = client.payment.fetch(payment_id)
        if payment.get("status") == "captured":
            return True, "Payment verified successfully!"
        else:
            return False, f"Payment status is '{payment.get('status')}'. Account can only be activated for successful payments."
    except razorpay.errors.BadRequestError:
        return False, "Invalid Payment ID. This transaction does not exist on Razorpay."
    except Exception as e:
        return False, f"Payment verification system error: {str(e)}"

# --- DATABASE OPERATIONS ---
def verify_db_user(phone, dob_str):
    try:
        response = supabase.table("users").select("name", "subscription_status").eq("phone", phone.strip()).eq("dob", dob_str.strip()).execute()
        if response.data:
            user_record = response.data[0]
            if user_record["subscription_status"] == "Active":
                return True, "Authorized", user_record["name"]
            else:
                return False, "Your subscription plan has expired.", None
        return False, "No active profile found. Check credentials or register a paid account.", None
    except Exception as e:
        return False, f"Supabase sync connection failure: {str(e)}", None

def register_user_account(name, phone, dob_str, tx_id):
    payment_ok, verification_msg = is_payment_valid(tx_id)
    if not payment_ok:
        return False, verification_msg
        
    expiry_date = (datetime.date.today() + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    try:
        new_row = {"name": name.strip(), "phone": phone.strip(), "dob": dob_str.strip(), "subscription_status": "Active", "payment_id": tx_id.strip(), "expiry_date": expiry_date}
        response = supabase.table("users").insert(new_row).execute()
        if response.data:
            return True, "Account registered and subscription activated successfully! Head to the Login tab."
        return False, "Server rejected database entry layout processing parameters."
    except Exception as e:
        error_msg = str(e)
        if "users_phone_key" in error_msg or "duplicate key" in error_msg:
            return False, "This phone number or Transaction ID is already registered to a user account."
        return False, f"Cloud database failure: {error_msg}"

# --- NUMEROLOGY CALCULATION CORE ---
def reduce_with_history(val_str):
    current = val_str
    while len(current) > 1:
        current = str(sum(int(d) for d in current if d.isdigit()))
    return int(current)


# --- GATEWAY USER INTERFACE ---
if 'auth_active' not in st.session_state:
    st.session_state.auth_active = False

st.markdown("<div class='hero-title'>Divine Aura</div>", unsafe_allow_html=True)

if not st.session_state.auth_active:
    st.markdown("<div class='hero-subtitle'>Your Personalized Destiny Portal</div>", unsafe_allow_html=True)
    
    spacer1, center_col, spacer2 = st.columns([1, 1.8, 1])
    
    with center_col:
        tab_login, tab_signup = st.tabs(["🔐 Premium Login", "💎 Purchase & Create Account"])
        
        with tab_login:
            with st.form("user_login_gate"):
                log_phone = st.text_input("Registered Phone Number")
                log_dob = st.date_input("Date of Birth", min_value=datetime.date(1940, 1, 1), key="login_dob")
                login_btn = st.form_submit_button("Access My Portal")
                
                if login_btn:
                    formatted_dob = log_dob.strftime("%d-%m-%Y")
                    valid, msg, name = verify_db_user(log_phone, formatted_dob)
                    if valid:
                        st.session_state.auth_active = True
                        st.session_state.p_name = name
                        st.session_state.p_dob = log_dob
                        st.rerun()
                    else:
                        st.error(msg)
                        
        with tab_signup:
            st.markdown("<div class='price-tag'>Yearly Pass: ₹302 / Month</div>", unsafe_allow_html=True)
            st.write("Get unhindered access to daily mathematical matrix charts, dynamic personal day calculators, planetary tracking, and lucky times.")
            st.markdown(f'<a href="{PAYMENT_GATEWAY_URL}" target="_blank"><button style="width:100%;">💳 Click to Pay on Secure Gateway</button></a>', unsafe_allow_html=True)
            
            st.markdown("<br>### Step 2: Register Your Paid Account", unsafe_allow_html=True)
            with st.form("self_signup_gate"):
                reg_name = st.text_input("Your Full Name")
                reg_phone = st.text_input("Phone Number (Use during checkout)")
                reg_dob = st.date_input("Select Date of Birth", min_value=datetime.date(1940, 1, 1), key="reg_dob")
                reg_tx = st.text_input("Payment / Order Reference ID", placeholder="e.g., pay_Nzk3MzYyNzM")
                signup_btn = st.form_submit_button("Activate My Account")
                
                if signup_btn:
                    if reg_name and reg_phone and reg_tx:
                        formatted_reg_dob = reg_dob.strftime("%d-%m-%Y")
                        ok, res_msg = register_user_account(reg_name, reg_phone, formatted_reg_dob, reg_tx)
                        if ok:
                            st.success(res_msg)
                        else:
                            st.error(res_msg)
                    else:
                        st.warning("Please complete all registration parameters to verify payment authorization credentials.")

else:
    # --- INSIGHTS ENGINE PORTAL VIEW ---
    curr_lang = st.session_state.lang
    T = UI[curr_lang]
    DATA = NUMEROLOGY_DATA_HI if curr_lang == 'HI' else NUMEROLOGY_DATA_EN
    
    user_name = st.session_state.p_name
    user_dob = st.session_state.p_dob
    today = datetime.date.today()
    
    st.markdown(f"<div class='hero-subtitle'>{T['welcome']}, {user_name} ✨ | {today.strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)
    
    # Language Toggle Button
    lang_col1, lang_col2 = st.columns([5, 1])
    with lang_col2:
        st.markdown("<div class='translate-btn'>", unsafe_allow_html=True)
        if st.button("🇮🇳 हिंदी में पढ़ें" if curr_lang == 'EN' else "🇬🇧 Read in English"):
            st.session_state.lang = 'HI' if curr_lang == 'EN' else 'EN'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Engine Calculations
    mulank = reduce_with_history(str(user_dob.day))
    full_dob_digits = user_dob.strftime("%d%m%Y")
    bhagyank = reduce_with_history(full_dob_digits)
    personal_year = reduce_with_history(f"{user_dob.day}{user_dob.month}{today.year}")
    personal_day = reduce_with_history(f"{personal_year}{today.month}{today.day}")
    
    m_assets = DATA[mulank]
    pd_assets = DATA[personal_day]
    
    # 🌟 MACRO-SPLIT CONTAINER
    master_left, master_right = st.columns([1, 1.1], gap="large")
    
    with master_left:
        st.markdown(f"## {T['blueprint_title']}")
        
        # Mulank Row
        st.markdown(f"""
        <div class='metric-row-box'>
            <div>
                <div class='metric-title-sub'>{T['driver']}</div>
                <div style='font-size:0.95rem; color:#555;'>{T['ruler']}: <strong>{m_assets['ruler']}</strong><br>{T['traits']}: {m_assets['traits']}</div>
            </div>
            <div class='metric-value_large'>{mulank}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bhagyank Row
        math_string = " + ".join(list(full_dob_digits))
        total_sum = sum(int(d) for d in full_dob_digits)
        st.markdown(f"""
        <div class='metric-row-box'>
            <div>
                <div class='metric-title-sub'>{T['destiny']}</div>
                <div style='font-size:0.92rem; color:#555;'>{T['calc']}: {math_string} = {total_sum} ➔ {bhagyank}</div>
            </div>
            <div class='metric-value-large'>{bhagyank}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Personal Year Row
        st.markdown(f"""
        <div class='metric-row-box'>
            <div>
                <div class='metric-title-sub'>{T['year_cycle']}</div>
                <div style='font-size:0.95rem; color:#555;'>{T['focus']}: {m_assets['year_text']}</div>
            </div>
            <div class='metric-value-large'>{personal_year}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<br>## {T['guide_title']}", unsafe_allow_html=True)
        guide_matrix = [
            {"Attribute": T['lucky_num'], "Alignment": f"{m_assets['numbers']} ({T['avoid']} {m_assets['avoid']})"},
            {"Attribute": T['lucky_col'], "Alignment": f"{m_assets['colors']}"},
            {"Attribute": T['power_dir'], "Alignment": f"{T['facing']} {m_assets['direction']}"},
            {"Attribute": T['power_hr'], "Alignment": f"{m_assets['hours']}"}
        ]
        st.table(guide_matrix)
        
    with master_right:
        st.markdown(f"## {T['today_title']} {personal_day})")
        
        # Career Card
        st.markdown(f"""
        <div class='prediction-card'>
            <div class='category-header'>{T['career']}</div>
            <div>{pd_assets['career']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Relationship Card
        st.markdown(f"""
        <div class='prediction-card'>
            <div class='category-header'>{T['relationship']}</div>
            <div>{pd_assets['relationship']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Health Card
        st.markdown(f"""
        <div class='prediction-card'>
            <div class='category-header'>{T['health']}</div>
            <div>{pd_assets['health']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # --- LOWER BASE ROW ---
    bottom_left, bottom_right = st.columns(2, gap="large")
    with bottom_left:
        st.markdown(f"### {T['matrix_title']}")
        if user_dob.day <= 9:
            st.markdown(T['single_digit_msg'].format(val=user_dob.day))
        else:
            st.markdown(T['double_digit_msg'].format(val=user_dob.day))
            
        st.markdown(f"* **{T['direct_plane']} ({mulank}):**")
        all_present_numbers = set([int(d) for d in full_dob_digits])
        missing = [str(x) for x in range(1, 10) if x not in all_present_numbers]
        if missing:
            st.markdown(f"* **{T['missing_elements']}: {', '.join(missing)}):**")

    with bottom_right:
        st.markdown(f"### {T['action_items']}")
        for tip in pd_assets['tips']:
            st.markdown(f"* {tip}")

    st.markdown(f"<div class='blockquote-style'>\"{pd_assets['affirmation']}\"</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    exit_spacer1, exit_center, exit_spacer2 = st.columns([1.3, 1, 1.3])
    with exit_center:
        if st.button(T['close_btn']):
            st.session_state.auth_active = False
            st.rerun()