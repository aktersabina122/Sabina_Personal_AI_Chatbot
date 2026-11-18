from __future__ import annotations

import hmac
import json
import urllib.error
import urllib.request
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
PROFILE_PATH = APP_DIR / "profile.md"
SETTINGS_PATH = APP_DIR / "local_settings.json"
KNOWLEDGE_PATH = APP_DIR / "knowledge.json"
OLLAMA_BASE = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen3:0.6b"
KNOWLEDGE_CATEGORIES = ["Biography", "Family History", "Education", "Career", "Interests", "Other"]

DEFAULT_FAQS = [
    {
        "question_en": "Where was Sabina raised?",
        "question_bn": "সাবিনা কোথায় বড় হয়েছেন?",
        "answer_en": "Sabina was raised in Mymensingh, Bangladesh.",
        "answer_bn": "সাবিনা বাংলাদেশের ময়মনসিংহে বড় হয়েছেন।",
    },
    {
        "question_en": "Where does Sabina live?",
        "question_bn": "সাবিনা কোথায় থাকেন?",
        "answer_en": "Sabina lives on Long Island, New York, and has lived in New York since 2013.",
        "answer_bn": "সাবিনা নিউ ইয়র্কের লং আইল্যান্ডে থাকেন। তিনি ২০১৩ সাল থেকে নিউ ইয়র্কে আছেন।",
    },
    {
        "question_en": "Where was Sabina born?",
        "question_bn": "সাবিনার জন্মস্থান কোথায়?",
        "answer_en": "Sabina has not chosen to share her birthplace publicly.",
        "answer_bn": "সাবিনা তাঁর জন্মস্থান প্রকাশ্যে জানানোর সিদ্ধান্ত নেননি।",
    },
    {
        "question_en": "What is Sabina learning?",
        "question_bn": "সাবিনা এখন কী শিখছেন?",
        "answer_en": "She is pursuing a master’s in cybersecurity and taking the Professional AI Engineering course through ICT BD Bangladesh.",
        "answer_bn": "তিনি সাইবার সিকিউরিটিতে মাস্টার্স করছেন এবং ICT BD Bangladesh-এর Professional AI Engineering কোর্স করছেন।",
    },
    {
        "question_en": "What are Sabina’s career goals?",
        "question_bn": "সাবিনার ক্যারিয়ারের লক্ষ্য কী?",
        "answer_en": "She wants to build a career integrating cloud security, cybersecurity, and AI engineering.",
        "answer_bn": "তিনি cloud security, cybersecurity ও AI engineering একসঙ্গে কাজে লাগিয়ে ক্যারিয়ার গড়তে চান।",
    },
    {
        "question_en": "What are Sabina’s interests?",
        "question_bn": "সাবিনার আগ্রহ কী কী?",
        "answer_en": "She enjoys Bengali cooking, travel, creative crafts, and writing.",
        "answer_bn": "তিনি বাংলা রান্না, ভ্রমণ, সৃজনশীল craft ও লেখালেখি পছন্দ করেন।",
    },
    {
        "question_en": "What are her sons’ names?",
        "question_bn": "সাবিনার ছেলেদের নাম কী?",
        "answer_en": "Her older son is Zayan, last reported age 11 in 2026; her younger son is Shayan, last reported age 7 in 2026.",
        "answer_bn": "সাবিনার বড় ছেলে Zayan, ২০২৬ সালে সর্বশেষ জানানো বয়স ১১; ছোট ছেলে Shayan, বয়স ৭।",
    },
    {
        "question_en": "How many sons does Sabina have?",
        "question_bn": "সাবিনার কয়জন ছেলে?",
        "answer_en": "Sabina has two sons. Their last reported ages in 2026 were 11 and 7.",
        "answer_bn": "সাবিনার দুই ছেলে আছে। ২০২৬ সালে সর্বশেষ জানানো বয়স ছিল ১১ ও ৭ বছর।",
    },
    {
        "question_en": "What is Sabina’s education?",
        "question_bn": "সাবিনার শিক্ষাগত যোগ্যতা কী?",
        "answer_en": "She is pursuing a master’s in cybersecurity, has a bachelor’s in computer science, and earlier studied Agricultural Economics, completed an MBA, and earned a master’s in Social Welfare.",
        "answer_bn": "তিনি সাইবার সিকিউরিটিতে মাস্টার্স করছেন; কম্পিউটার সায়েন্সে ব্যাচেলর এবং আগে Agricultural Economics, MBA ও Social Welfare-এ মাস্টার্স করেছেন।",
    },
    {
        "question_en": "What did Sabina do in Bangladesh?",
        "question_bn": "বাংলাদেশে সাবিনা কী কাজ করতেন?",
        "answer_en": "She worked in banking for 3.5 years and at another employer for 2 years. Employer names are not shared.",
        "answer_bn": "তিনি বাংলাদেশে ব্যাংকিংয়ে ৩.৫ বছর এবং আরেক প্রতিষ্ঠানে ২ বছর কাজ করেছেন। প্রতিষ্ঠানের নাম প্রকাশ করা হয় না।",
    },
    {
        "question_en": "What are Sabina’s sons’ birthdays?",
        "question_bn": "সাবিনার ছেলেদের জন্মদিন কবে?",
        "answer_en": "I don’t have their birthdays in Sabina’s approved profile.",
        "answer_bn": "সাবিনার অনুমোদিত প্রোফাইলে তাঁদের জন্মদিনের তথ্য নেই।",
    },
]

COLORS = {
    "navy": "#142e3a",
    "teal": "#176b63",
    "paper": "#f9f8f4",
    "pale": "#eaf2ed",
    "border": "#dce4df",
    "muted": "#5b6e72",
}

DEFAULT_SETTINGS = {
    "display_name": "Sabina",
    "public_title": "Curious learner & creative thinker",
    "intro_en": "I’m Sabina. I enjoy learning, thoughtful conversations, and finding inspiration in everyday life.",
    "intro_bn": "আমি সাবিনা। নতুন কিছু শেখা ও সৃজনশীল কাজ করতে ভালোবাসি।",
    "interests": "Reading, lifelong learning, creativity",
    "welcome_en": "Hi, I’m Sabina’s personal AI. What would you like to know?",
    "welcome_bn": "হ্যালো! আমি সাবিনার ব্যক্তিগত এআই। আপনি কী জানতে চান?",
    "model": DEFAULT_MODEL,
    "language": "English",
    "suggestions": [
        ("Tell me about Sabina", "সাবিনা সম্পর্কে বলুন"),
        ("What are her interests?", "তার আগ্রহ কী কী?"),
        ("What is she learning?", "তিনি কী শিখছেন?"),
        ("How can I get in touch?", "কীভাবে যোগাযোগ করব?"),
    ],
}

st.set_page_config(page_title="Sabina’s Personal AI", page_icon="✦", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
    :root { --navy:#142e3a; --teal:#176b63; --paper:#f9f8f4; --pale:#eaf2ed; --border:#dce4df; --muted:#5b6e72; }
    .stApp, [data-testid="stAppViewContainer"] { background:var(--paper); color:var(--navy); }
    [data-testid="stHeader"] { background:transparent; }
    [data-testid="stSidebar"] { display:none; }
    .block-container { max-width:1440px; padding:1.2rem 4vw 1.5rem; }
    h1,h2,h3 { color:var(--navy); font-family:Manrope,Inter,system-ui,sans-serif; letter-spacing:-.025em; }
    p, label, input, textarea, button { font-family:Inter,"Noto Sans Bengali",system-ui,sans-serif; }
    .brand { font-size:1.2rem; font-weight:650; color:var(--navy); }
    .tag { display:inline-block; margin-left:.5rem; padding:.25rem .55rem; border-radius:999px; background:var(--pale); color:var(--teal); font-size:.68rem; font-weight:700; vertical-align:middle; }
    .eyebrow { color:var(--teal); font-size:.68rem; font-weight:700; letter-spacing:.07em; text-transform:uppercase; }
    .muted { color:var(--muted); }
    .local-pill { display:inline-block; padding:.38rem .7rem; border-radius:999px; background:var(--pale); color:var(--teal); font-size:.75rem; }
    .stButton>button, .stFormSubmitButton>button { border-radius:9px; border:1px solid var(--border); color:var(--navy); background:white; min-height:2.55rem; }
    .stButton>button[kind="primary"], .stFormSubmitButton>button[kind="primary"] { color:white; background:var(--teal); border-color:var(--teal); }
    [data-testid="stChatMessage"] { border:1px solid var(--border); border-radius:14px; background:white; }
    [data-testid="stChatInput"] { border-color:var(--border); }
    [data-testid="stVerticalBlockBorderWrapper"] { border-color:var(--border); border-radius:14px; background:white; }
    .admin-nav { background:var(--navy); border-radius:14px; color:white; padding:1.25rem; }
    .status-card { background:white; border:1px solid var(--border); border-radius:10px; padding:1rem; min-height:92px; }
    .footer-note { color:var(--muted); font-size:.74rem; }
    @media (max-width: 850px) {
      .block-container { padding:.8rem 1rem 1rem; }
      h1 { font-size:2rem !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_settings() -> dict:
    settings = DEFAULT_SETTINGS.copy()
    if SETTINGS_PATH.exists():
        try:
            saved = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
            settings.update({k: v for k, v in saved.items() if k in settings})
        except (OSError, json.JSONDecodeError):
            pass
    return settings


def save_settings(settings: dict) -> None:
    SETTINGS_PATH.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")


def load_knowledge() -> list[dict]:
    if KNOWLEDGE_PATH.exists():
        try:
            data = json.loads(KNOWLEDGE_PATH.read_text(encoding="utf-8"))
            return [item for item in data if isinstance(item, dict)] if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []
    return [item.copy() for item in DEFAULT_FAQS]


def save_knowledge(items: list[dict]) -> None:
    KNOWLEDGE_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def variants_for(item: dict) -> list[str]:
    raw = item.get("question_variants", [])
    if isinstance(raw, str):
        variants = [line.strip() for line in raw.splitlines() if line.strip()]
    elif isinstance(raw, list):
        variants = [str(line).strip() for line in raw if str(line).strip()]
    else:
        variants = []
    variants.extend([item.get("question_en", ""), item.get("question_bn", "")])
    return list(dict.fromkeys(value.strip() for value in variants if isinstance(value, str) and value.strip()))


def _question_terms(value: str) -> set[str]:
    import re
    words = re.findall(r"[a-z0-9\u0980-\u09ff]+", value.casefold())
    stop_words = {"the", "is", "a", "an", "of", "to", "where", "was", "were", "does", "do", "did", "she", "her", "he", "his", "কি", "কী", "হয়", "হয়েছেন", "কোথায়", "সাবিনা", "তার"}
    return {word for word in words if word not in stop_words}


def find_faq_answer(question: str, items: list[dict]) -> str | None:
    is_bengali = any("\u0980" <= char <= "\u09ff" for char in question)
    query_terms = _question_terms(question)
    best_item, best_score = None, 0.0
    for item in items:
        if item.get("visibility", "Public") != "Public":
            continue
        variants = variants_for(item)
        if not query_terms or not variants:
            continue
        score = max((len(query_terms & terms) / len(query_terms | terms) for variant in variants if (terms := _question_terms(variant))), default=0.0)
        if score > best_score:
            best_item, best_score = item, score
    if best_item and best_score >= 0.28:
        answer = best_item.get("answer_bn" if is_bengali else "answer_en", "").strip()
        return answer or None
    return None


def get_admin_credentials() -> tuple[str, str]:
    try:
        return str(st.secrets.get("ADMIN_USERNAME", "")), str(st.secrets.get("ADMIN_PASSWORD", ""))
    except Exception:
        return "", ""


def check_local_model(model: str) -> tuple[bool, str]:
    request = urllib.request.Request(f"{OLLAMA_BASE}/api/tags", method="GET")
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
        installed = [entry.get("name", "") for entry in payload.get("models", [])]
        exact = model in installed or any(item.split(":")[0] == model.split(":")[0] for item in installed)
        if exact:
            return True, "Ollama is connected and the selected model is installed."
        return True, "Ollama is connected. Download the selected model in PowerShell before using it."
    except Exception:
        return False, "Ollama is not responding on this computer."


def direct_profile_answer(question: str, knowledge: list[dict] | None = None) -> str | None:
    q = question.casefold()
    is_bengali = any("\u0980" <= char <= "\u09ff" for char in question)
    if any(phrase in q for phrase in ("tell me about sabina", "about sabina", "who is sabina", "সাবিনা সম্পর্কে", "সাবিনা কে", "সাবিনার পরিচয়", "সাবিনার পরিচয়")):
        return (
            "সাবিনা আক্তার সাইবার সিকিউরিটিতে মাস্টার্স করছেন এবং Professional AI Engineering শিখছেন। তাঁর লক্ষ্য ক্লাউড সিকিউরিটি, সাইবার সিকিউরিটি ও AI-কে একসঙ্গে কাজে লাগানো। তিনি Long Island, New York-এ থাকেন এবং লেখালেখি ও সৃজনশীল কাজ পছন্দ করেন।"
            if is_bengali else
            "Sabina Akter is pursuing a master’s in cybersecurity and studying Professional AI Engineering. Her goal is to bring cloud security, cybersecurity, and AI together. She lives on Long Island, New York, and enjoys writing and creative work."
        )
    if knowledge:
        faq_answer = find_faq_answer(question, knowledge)
        if faq_answer:
            return faq_answer
    asks_names = any(word in q for word in ("name", "names", "নাম"))
    about_sons = any(word in q for word in ("son", "sons", "children", "child", "kids", "ছেলে", "সন্তান", "পুত্র"))
    refers_to_their_names = any(phrase in q for phrase in ("their name", "their names", "what are their", "ওদের নাম", "তাদের নাম", "ছেলেদের নাম"))
    if (asks_names and about_sons) or refers_to_their_names:
        return "সাবিনার বড় ছেলে Zayan, বয়স ১১; ছোট ছেলে Shayan, বয়স ৭ (সর্বশেষ জানানো বয়স, ২০২৬)।" if is_bengali else "Sabina’s older son is Zayan, age 11, and her younger son is Shayan, age 7 (last reported in 2026)."
    if any(word in q for word in ("born", "birthplace", "জন্মস্থান", "জন্ম কোথায়", "জন্ম কোথায়", "কোথায় জন্ম", "কোথায় জন্ম")):
        return "সাবিনা তাঁর জন্মস্থান প্রকাশ্যে জানানোর সিদ্ধান্ত নেননি।" if is_bengali else "Sabina has not chosen to share her birthplace publicly."
    if any(word in q for word in ("raised", "grew up", "hometown", "বড় হয়েছেন", "বড় হয়েছেন", "বড় হয়েছি", "বড় হয়েছি", "শৈশব", "শৈশবে")):
        return "সাবিনা বাংলাদেশের ময়মনসিংহে বড় হয়েছেন।" if is_bengali else "Sabina was raised in Mymensingh, Bangladesh."
    if any(word in q for word in ("where is she from", "where is sabina from", "from where", "কোথা থেকে", "কোথাকার")):
        return "সাবিনা বাংলাদেশের ময়মনসিংহে বড় হয়েছেন।" if is_bengali else "Sabina was raised in Mymensingh, Bangladesh."
    if any(word in q for word in ("where does she live", "where she lives", "where does sabina live", "বাসা কোথায়", "বাসা কোথায়", "কোথায় থাকেন", "কোথায় থাকেন", "কোথায় থাকে", "কোথায় থাকে")):
        return "সাবিনা নিউ ইয়র্কের লং আইল্যান্ডে থাকেন।" if is_bengali else "Sabina lives on Long Island, New York."
    if any(word in q for word in ("son", "sons", "children", "child", "boys", "ছেলে", "সন্তান", "পুত্র")):
        return "সাবিনার দুই ছেলে আছে। ২০২৬ সালে সর্বশেষ জানানো বয়স ছিল ১১ ও ৭ বছর।" if is_bengali else "Sabina has two sons. The last reported ages in 2026 were 11 and 7."
    if any(word in q for word in ("father", "dad", "বাবা", "আব্বা", "পিতা")):
        return "সাবিনার বাবার নাম Muhammad Golam Rabbani। তিনি একজন মুক্তিযোদ্ধা ছিলেন এবং ২০১৯ সালে মারা যান।" if is_bengali else "Sabina’s father was Muhammad Golam Rabbani, a freedom fighter who died in 2019."
    if any(word in q for word in ("grandfather", "grandpa", "দাদা", "নানা", "grand father")):
        return "সাবিনার দাদার নাম Muhammad Sohrawardi Fokir।" if is_bengali else "Sabina’s grandfather’s name was Muhammad Sohrawardi Fokir."
    if any(word in q for word in ("sister", "sisters", "বোন")):
        return "সাবিনার দুই ছোট বোন আছে।" if is_bengali else "Sabina has two younger sisters."
    if any(word in q for word in ("education", "degree", "degrees", "studied", "study", "academic", "পড়াশোনা", "পড়াশোনা", "শিক্ষা", "ডিগ্রি", "বিশ্ববিদ্যালয়", "বিশ্ববিদ্যালয়", "কলেজ")):
        return "সাবিনা সাইবার সিকিউরিটিতে মাস্টার্স করছেন (সম্ভাব্য সমাপ্তি ২০২৭)। তাঁর কম্পিউটার সায়েন্সে ব্যাচেলর ডিগ্রি আছে; এর আগে Agricultural Economics, MBA এবং Social Welfare-এও পড়েছেন।" if is_bengali else "Sabina is pursuing a master’s in cybersecurity, expected in 2027. She has a bachelor’s degree in computer science and earlier studied Agricultural Economics, completed an MBA, and earned a master’s in Social Welfare."
    if any(word in q for word in ("learning", "learn", "course", "studying", "শিখছেন", "শিখছে", "কোর্স", "পড়ছেন", "পড়ছেন")):
        return "সাবিনা সাইবার সিকিউরিটিতে মাস্টার্স করছেন এবং ICT BD Bangladesh-এর Professional AI Engineering কোর্স করছেন।" if is_bengali else "Sabina is pursuing a master’s in cybersecurity and taking the Professional AI Engineering course through ICT BD Bangladesh."
    if any(word in q for word in ("interest", "interests", "hobby", "hobbies", "likes", "enjoys", "আগ্রহ", "শখ", "পছন্দ", "ভালোবাসে", "ভালবাসে")):
        return "সাবিনা বাংলা রান্না, ভ্রমণ, সৃজনশীল craft এবং লেখালেখি পছন্দ করেন।" if is_bengali else "Sabina enjoys Bengali cooking, travel, creative crafts, and writing."
    if any(word in q for word in ("career", "profession", "job", "work", "ক্যারিয়ার", "ক্যারিয়ার", "পেশা", "চাকরি", "কাজ")) and "bangladesh" not in q:
        return "সাবিনার cloud infrastructure ও cybersecurity-তে অভিজ্ঞতা আছে। তাঁর লক্ষ্য cloud security, cybersecurity ও AI engineering একসঙ্গে কাজে লাগিয়ে ক্যারিয়ার এগিয়ে নেওয়া।" if is_bengali else "Sabina has experience in cloud infrastructure and cybersecurity. Her career goal is to bring cloud security, cybersecurity, and AI engineering together."
    if "bangladesh" in q and any(word in q for word in ("bank", "work", "job", "profession", "career", "ব্যাংক", "চাকরি", "কাজ", "পেশা")):
        return "সাবিনা বাংলাদেশে ব্যাংকিংয়ে ৩.৫ বছর এবং আরেক প্রতিষ্ঠানে ২ বছর কাজ করেছেন। নিয়োগকর্তার নাম প্রকাশ করা হয় না।" if is_bengali else "Sabina worked in banking in Bangladesh for 3.5 years and at another employer for 2 years. Employer names are not shared."
    import re
    tokens = set(re.findall(r"[a-z0-9]+", q))
    personal_reference = bool(tokens & {"sabina", "she", "her", "hers", "he", "his", "their", "son", "sons", "child", "children", "father", "dad", "mother", "mom", "sister", "brother", "family", "age", "birthday", "born"}) or any(word in q for word in ("সাবিনা", "তিনি", "তার", "তাঁর", "ওর", "ছেলে", "সন্তান", "বাবা", "মা", "বোন", "ভাই", "পরিবার"))
    if personal_reference:
        return "দুঃখিত, এই তথ্যটি সাবিনার অনুমোদিত প্রোফাইলে নেই।" if is_bengali else "Sorry, I don’t have that information in Sabina’s approved profile."
    return None


def ask_local_model(messages: list[dict], settings: dict, knowledge: list[dict]) -> str:
    system_prompt = (APP_DIR / "system_prompt.txt").read_text(encoding="utf-8")
    profile = PROFILE_PATH.read_text(encoding="utf-8")
    faq_context = json.dumps(knowledge, ensure_ascii=False, indent=2)
    context = f"{system_prompt}\n\n# Public profile\n{profile}\n\n# Approved question and answer examples; use these when relevant\n{faq_context}\n\n# Public display settings\n{json.dumps({k: settings[k] for k in ('display_name','public_title','intro_en','intro_bn','interests','welcome_en','welcome_bn')}, ensure_ascii=False)}"
    request_messages = [{"role": "system", "content": context}, *messages[-20:]]
    payload = json.dumps({
        "model": settings.get("model", DEFAULT_MODEL),
        "messages": request_messages,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": 250},
    }).encode("utf-8")
    request = urllib.request.Request(
        f"{OLLAMA_BASE}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.loads(response.read().decode("utf-8"))
    answer = result.get("message", {}).get("content", "").strip()
    if answer:
        return answer
    last_question = messages[-1].get("content", "") if messages else ""
    is_bengali = any("\u0980" <= char <= "\u09ff" for char in last_question)
    return "সাবিনার অনুমোদিত প্রোফাইলে এই তথ্যটি নেই।" if is_bengali else "I don’t have that detail in Sabina’s approved profile."


def set_page(page: str) -> None:
    st.query_params["page"] = page
    st.rerun()


def render_header(settings: dict, admin: bool = False) -> None:
    left, right = st.columns([0.64, 0.36], vertical_alignment="center")
    with left:
        if admin:
            st.markdown("<div class='brand'>Sabina’s Personal AI <span class='tag'>PRIVATE</span></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='brand'>Sabina’s Personal AI <span class='tag'>PERSONAL</span></div>", unsafe_allow_html=True)
    with right:
        if admin:
            if st.button("Sign out", use_container_width=True):
                st.session_state["admin_authenticated"] = False
                set_page("chat")
        else:
            language_col, new_col, admin_col = st.columns([1.05, 1, 0.72], gap="small")
            with language_col:
                st.selectbox("Language", ["English", "বাংলা"], index=0 if settings.get("language") == "English" else 1, label_visibility="collapsed", key="public_language")
            with new_col:
                if st.button("New chat", use_container_width=True):
                    st.session_state["messages"] = []
                    st.rerun()
            with admin_col:
                if st.button("Admin sign-in", use_container_width=True, help="Open the private admin dashboard"):
                    set_page("admin")
    st.divider()


def show_chat(settings: dict) -> None:
    render_header(settings)
    left, right = st.columns([0.4, 1], gap="large")

    with left:
        st.markdown("<div class='eyebrow'>A little closer, one conversation at a time</div>", unsafe_allow_html=True)
        st.markdown("# Hello, I’m<br/>Sabina’s AI.", unsafe_allow_html=True)
        st.markdown("### স্বাগতম! আসুন, কথা বলি।")
        st.write("A friendly way to learn about Sabina, her interests, and what inspires her.")
        st.markdown("<div class='eyebrow'>Not sure where to start?</div>", unsafe_allow_html=True)
        for index, pair in enumerate(settings.get("suggestions", DEFAULT_SETTINGS["suggestions"])):
            en, bn = pair if isinstance(pair, (list, tuple)) and len(pair) == 2 else DEFAULT_SETTINGS["suggestions"][index % 4]
            if st.button(f"{en}\n{bn}   ↗", key=f"suggestion_{index}", use_container_width=True):
                st.session_state["pending_question"] = en
                st.rerun()
        st.success("Your conversation stays on this device.\n\nNo account needed. Just say hello.")
        if st.button("Admin sign-in →", key="admin_signin_sidebar", use_container_width=True, help="Open the private admin dashboard"):
            set_page("admin")

    with right:
        with st.container(border=True):
            top_left, top_right = st.columns([0.75, 0.25], vertical_alignment="center")
            with top_left:
                st.markdown("**A conversation with Sabina’s AI**")
                st.caption("বাংলা বা English—যে ভাষায় স্বচ্ছন্দ।")
            with top_right:
                st.markdown("<div style='text-align:right'><span class='local-pill'>● Runs locally</span></div>", unsafe_allow_html=True)

            for item in st.session_state.get("messages", []):
                with st.chat_message(item["role"]):
                    st.markdown(item["content"])
            if not st.session_state.get("messages"):
                st.info(f"**SABINA’S AI**\n\n{settings['welcome_en']}\n\n{settings['welcome_bn']}")

            st.caption("AI can make mistakes. I use only what Sabina has chosen to share; employer names and sensitive details stay private.")

            with st.form("chat_form", clear_on_submit=True):
                question = st.text_area("Ask a question / প্রশ্ন লিখুন", height=64, label_visibility="collapsed", placeholder="Ask a question / প্রশ্ন লিখুন")
                sent = st.form_submit_button("Send ↑", type="primary", use_container_width=True)
            st.caption("Enter to send · Shift + Enter for a new line                              No API key required")

            pending = st.session_state.pop("pending_question", None)
            if sent and question.strip():
                pending = question.strip()
            if pending:
                st.session_state.setdefault("messages", []).append({"role": "user", "content": pending})
                with st.spinner("উত্তর তৈরি হচ্ছে…"):
                    try:
                        knowledge = load_knowledge()
                        answer = direct_profile_answer(pending, knowledge) or ask_local_model(st.session_state["messages"], settings, knowledge)
                    except urllib.error.URLError:
                        answer = "Ollama is not running or the model is not downloaded. In PowerShell, run `ollama run qwen3:0.6b`."
                    except Exception:
                        answer = "The local model could not answer. Please try again."
                st.session_state["messages"].append({"role": "assistant", "content": answer})
                st.rerun()

    st.divider()
    st.markdown("<span class='footer-note'>Personal, thoughtful, and a little more human.</span>", unsafe_allow_html=True)


def show_login(settings: dict) -> None:
    render_header(settings, admin=True)
    left, right = st.columns([0.76, 1], gap="large", vertical_alignment="center")
    with left:
        st.markdown("<div style='background:#142e3a;color:white;padding:2.5rem;border-radius:14px;min-height:520px'>", unsafe_allow_html=True)
        st.markdown("YOUR PRIVATE CORNER")
        st.markdown("# A little more you.<br/>A little less noise.", unsafe_allow_html=True)
        st.markdown("### আপনার এআই, আপনার নিয়ন্ত্রণে।")
        st.write("Shape what your AI knows, how it welcomes people, and what stays just yours.")
        st.write("01  Runs locally on your device")
        st.write("02  No API key required")
        st.write("03  Only approved knowledge is shared")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='eyebrow'>Admin access</div>", unsafe_allow_html=True)
        st.markdown("## Welcome back, Sabina.")
        st.write("Sign in to your private dashboard. Visitors can chat without signing in.")
        expected_user, expected_password = get_admin_credentials()
        if not expected_user or not expected_password:
            st.warning("Admin sign-in is not set up yet. Add a username and password in `.streamlit/secrets.toml`; see README_BN.md.")
        with st.form("admin_login"):
            username = st.text_input("Username", value="sabina")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign in to dashboard →", type="primary", use_container_width=True)
        if submitted:
            if expected_user and expected_password and hmac.compare_digest(username.encode("utf-8"), expected_user.encode("utf-8")) and hmac.compare_digest(password.encode("utf-8"), expected_password.encode("utf-8")):
                st.session_state["admin_authenticated"] = True
                set_page("admin")
            else:
                st.error("Sign-in didn't work. Check the local admin details and try again.")
        st.caption("Private access. Public conversations stay separate.\n\nLocal credentials only · No external account required")
        if st.button("← Back to public chat"):
            set_page("chat")


def show_admin(settings: dict) -> None:
    render_header(settings, admin=True)
    nav, main = st.columns([0.19, 1], gap="large")
    with nav:
        st.markdown("<div class='admin-nav'><h3 style='color:white'>Sabina’s<br/>Personal AI</h3><small>PRIVATE WORKSPACE</small></div>", unsafe_allow_html=True)
        section = st.radio("Admin sections", ["Admin Dashboard", "AI Chat", "Biography", "Family History", "Knowledge Training Studio", "Chat Appearance", "Local Model"], index=4, key="admin_section", label_visibility="collapsed")
        if section == "AI Chat":
            set_page("chat")
            return
        st.info("A space just for you. Edit what your AI knows; only approved profile content is shared publicly.")
        st.caption("Signed in as Sabina · Local administrator")
    with main:
        title, actions = st.columns([0.76, 0.24], vertical_alignment="center")
        with title:
            st.markdown("<div class='eyebrow'>Admin Control Center</div>", unsafe_allow_html=True)
            st.markdown("## Knowledge Training Studio" if section == "Knowledge Training Studio" else "## Make it feel like you.")
            st.caption("অনুমোদিত তথ্য যোগ, খোঁজা ও সম্পাদনা করুন।" if section == "Knowledge Training Studio" else "Manage your public profile, appearance, and local model.")
        with actions:
            if st.button("Preview chat ↗", use_container_width=True):
                set_page("chat")

        if section == "Admin Dashboard":
            st.markdown("### 01 / Admin Dashboard")
            cards = st.columns(3)
            for column, (label, value, note) in zip(cards, [
                ("Public profile", "Ready to share", "Only approved content"),
                ("Language support", "বাংলা + English", "Bilingual by default"),
                ("Local connection", "Check below", "Runs locally · No API key required"),
            ]):
                with column:
                    st.markdown(f"<div class='status-card'><small>{label}</small><h3 style='color:#176b63'>{value}</h3><small>{note}</small></div>", unsafe_allow_html=True)
            st.write("")
            st.info("প্রশ্ন–উত্তর যোগ করতে বাম পাশের **Knowledge Training Studio** খুলুন।")
            if st.button("＋ Add questions and answers", type="primary"):
                st.session_state["admin_section"] = "Knowledge Training Studio"
                st.rerun()

        elif section == "Biography":
            st.markdown("### 02 / Biography")
            st.caption("এখানে public biography ও পরিচিতির তথ্য সম্পাদনা করুন।")
            st.markdown("#### Public profile")
            with st.form("profile_settings"):
                c1, c2 = st.columns(2)
                with c1:
                    display_name = st.text_input("Display name", value=settings["display_name"])
                with c2:
                    public_title = st.text_input("Public title", value=settings["public_title"])
                intro_en = st.text_area("Public introduction · English", value=settings["intro_en"], height=82)
                intro_bn = st.text_area("Public introduction · বাংলা", value=settings["intro_bn"], height=82)
                interests = st.text_input("Interests", value=settings["interests"])
                public_profile = st.text_area("Approved public knowledge", value=PROFILE_PATH.read_text(encoding="utf-8"), height=300)
                saved = st.form_submit_button("Save changes", type="primary")
            if saved:
                settings.update({"display_name": display_name, "public_title": public_title, "intro_en": intro_en, "intro_bn": intro_bn, "interests": interests})
                save_settings(settings)
                PROFILE_PATH.write_text(public_profile, encoding="utf-8")
                st.success("Changes saved on this computer.")

        elif section == "Family History":
            st.markdown("### 03 / Family History")
            st.caption("পরিবার সম্পর্কে chatbot-এ প্রকাশ করতে চান এমন তথ্য এখানে লিখুন। গোপন তথ্য public profile-এ যোগ করবেন না।")
            profile_text = PROFILE_PATH.read_text(encoding="utf-8")
            family_start = profile_text.find("## Personal life and family")
            family_end = profile_text.find("## Personal interests", family_start + 1) if family_start >= 0 else -1
            if family_start < 0:
                st.info("profile.md-তে ‘## Personal life and family’ শিরোনামটি পাওয়া যায়নি। Biography অংশ থেকে সম্পাদনা করতে পারেন।")
            else:
                old_family = profile_text[family_start:family_end if family_end >= 0 else len(profile_text)].strip()
                with st.form("family_history"):
                    family_text = st.text_area("Approved family information", value=old_family, height=300)
                    family_saved = st.form_submit_button("Save family information", type="primary")
                if family_saved:
                    replacement = family_text.strip()
                    revised = profile_text[:family_start] + replacement + ("\n\n" + profile_text[family_end:] if family_end >= 0 else "")
                    PROFILE_PATH.write_text(revised, encoding="utf-8")
                    st.success("Family information saved on this computer.")

        elif section == "Knowledge Training Studio":
            st.markdown("### 🔐 Knowledge Training Studio")
            st.caption("নতুন প্রশ্ন–উত্তর যোগ করতে বাম পাশের ফর্ম পূরণ করে **Save knowledge** চাপুন। প্রশ্নের অন্যভাবে বলা রূপগুলো আলাদা লাইনে লিখুন। সংরক্ষণ হলেই chatbot ব্যবহার করতে পারবে।")
            st.info("শুধু public-এ শেয়ার করতে চান এমন তথ্য দিন। অজানা তথ্যের ক্ষেত্রে AI বলবে যে তার কাছে তথ্যটি নেই।")
            knowledge = load_knowledge()
            left, right = st.columns([1, 1], gap="large")
            with left:
                st.markdown("#### ＋ Add / Edit Knowledge")
                with st.form("new_faq"):
                    category = st.selectbox("Category", ["Biography", "Family History", "Education", "Career", "Interests", "Other"])
                    new_variants = st.text_area("Question variations · প্রতি লাইনে একটি প্রশ্ন", placeholder="What is Sabina learning?\nসাবিনা এখন কী শিখছেন?\nWhich course is she taking?", height=125)
                    new_a_bn = st.text_area("Answer (বাংলা)", placeholder="অনুমোদিত বাংলা উত্তর লিখুন…", height=100)
                    new_a_en = st.text_area("Answer (English)", placeholder="Write the approved English answer…", height=100)
                    add_faq = st.form_submit_button("Save knowledge", type="primary", use_container_width=True)
                if add_faq:
                    clean_variants = [line.strip() for line in new_variants.splitlines() if line.strip()]
                    if not clean_variants or not (new_a_bn.strip() or new_a_en.strip()):
                        st.error("কমপক্ষে একটি প্রশ্ন এবং বাংলা বা English-এ একটি উত্তর দিন।")
                    else:
                        knowledge.append({"category": category, "visibility": "Public", "question_variants": clean_variants, "answer_bn": new_a_bn.strip(), "answer_en": new_a_en.strip()})
                        save_knowledge(knowledge)
                        st.success("তথ্য সংরক্ষিত হয়েছে।")
                        st.rerun()
                st.caption("উদাহরণ: ‘Where was Sabina raised?’ এবং ‘সাবিনা কোথায় বড় হয়েছেন?’ আলাদা লাইনে লিখুন।")

            with right:
                st.markdown(f"#### Knowledge Entries · {len(knowledge)}")
                search = st.text_input("Search knowledge…", placeholder="Search a question or answer", key="knowledge_search")
                search_term = search.casefold().strip()
                matching = [(i, item) for i, item in enumerate(knowledge) if not search_term or search_term in " ".join(variants_for(item) + [str(item.get("answer_en", "")), str(item.get("answer_bn", "")), str(item.get("category", ""))]).casefold()]
                if not matching:
                    st.caption("কোনো তথ্য মেলেনি।")
                for index, item in matching:
                    variants = variants_for(item)
                    label = variants[0] if variants else f"Knowledge {index + 1}"
                    category_value = item.get("category", "Biography")
                    with st.container(border=True):
                        st.markdown(f"**{category_value}** · Public")
                        st.write(label)
                        st.caption(f"{len(variants)} question variation(s)")
                        with st.expander("Edit"):
                            with st.form(f"edit_faq_{index}"):
                                edit_category = st.selectbox("Category", ["Biography", "Family History", "Education", "Career", "Interests", "Other"], index=["Biography", "Family History", "Education", "Career", "Interests", "Other"].index(category_value) if category_value in ["Biography", "Family History", "Education", "Career", "Interests", "Other"] else 0, key=f"cat_{index}")
                                edit_variants = st.text_area("Question variations · one per line", value="\n".join(variants), height=110, key=f"vars_{index}")
                                edit_bn = st.text_area("Answer (বাংলা)", value=item.get("answer_bn", ""), height=90, key=f"ansbn_{index}")
                                edit_en = st.text_area("Answer (English)", value=item.get("answer_en", ""), height=90, key=f"ansen_{index}")
                                update_faq = st.form_submit_button("Save changes", type="primary")
                            if update_faq:
                                updated_variants = [line.strip() for line in edit_variants.splitlines() if line.strip()]
                                if not updated_variants or not (edit_bn.strip() or edit_en.strip()):
                                    st.error("কমপক্ষে একটি প্রশ্ন এবং একটি উত্তর রাখুন।")
                                else:
                                    knowledge[index] = {"category": edit_category, "visibility": "Public", "question_variants": updated_variants, "answer_bn": edit_bn.strip(), "answer_en": edit_en.strip()}
                                    save_knowledge(knowledge)
                                    st.rerun()
                        if st.button("Delete", key=f"remove_faq_{index}"):
                            knowledge.pop(index)
                            save_knowledge(knowledge)
                            st.rerun()

        elif section == "Chat Appearance":
            st.markdown("### 04 / Chat Appearance")
            with st.form("appearance_settings"):
                welcome_en = st.text_input("Welcome message · English", value=settings["welcome_en"])
                welcome_bn = st.text_input("Welcome message · বাংলা", value=settings["welcome_bn"])
                c1, c2 = st.columns(2)
                with c1:
                    theme = st.selectbox("Theme", ["Navy & teal"], index=0)
                with c2:
                    language = st.selectbox("Default language", ["English", "বাংলা"], index=0 if settings.get("language") == "English" else 1)
                appearance_saved = st.form_submit_button("Save changes", type="primary")
            if appearance_saved:
                settings.update({"welcome_en": welcome_en, "welcome_bn": welcome_bn, "theme": theme, "language": language})
                save_settings(settings)
                st.success("Appearance settings saved on this computer.")

        else:
            st.markdown("### 05 / Local Model")
            st.caption("Your AI runs on this device. No OpenAI API key is used.")
            current = settings.get("model", DEFAULT_MODEL)
            connected, message = check_local_model(current)
            if connected:
                st.success(message)
            else:
                st.warning(message)
            with st.form("model_settings"):
                model = st.text_input("Model name", value=current, help="Use a model already downloaded in Ollama, for example qwen3:0.6b.")
                st.code(f"{OLLAMA_BASE}")
                model_saved = st.form_submit_button("Save model setting", type="primary")
            if model_saved:
                settings["model"] = model.strip() or DEFAULT_MODEL
                save_settings(settings)
                st.success("Model setting saved. Download the selected model in Ollama if needed.")
            if st.button("Test connection"):
                connected, message = check_local_model(settings.get("model", DEFAULT_MODEL))
                st.success(message) if connected else st.error(message)

        st.divider()
        st.caption("Private admin area · Visitor conversations are not stored or displayed.")


def main() -> None:
    settings = load_settings()
    st.session_state.setdefault("messages", [])
    page = st.query_params.get("page", "chat")
    if page == "admin":
        if st.session_state.get("admin_authenticated"):
            show_admin(settings)
        else:
            show_login(settings)
    else:
        show_chat(settings)


if __name__ == "__main__":
    main()

