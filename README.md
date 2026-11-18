# Sabina’s Personal AI

Sabina’s Personal AI হলো বাংলা ও English-এ কথা বলতে পারা একটি personal profile chatbot। এটি Sabina-র অনুমোদিত profile ও knowledge থেকে তাঁর শিক্ষা, পেশাগত অভিজ্ঞতা, বর্তমান পড়াশোনা, career goals, আগ্রহ এবং নির্বাচিত ব্যক্তিগত তথ্য সম্পর্কে প্রশ্নের উত্তর দেয়।

## কী জানতে পারবেন

- Sabina-র academic background ও professional experience and family information
- Cybersecurity, cloud security এবং AI engineering-এ তাঁর আগ্রহ ও শেখার লক্ষ্য
- তাঁর লেখা, creative work, cooking এবং অন্যান্য অনুমোদিত আগ্রহ
- Sabina-র profile বা Knowledge Training Studio-তে যোগ করা প্রশ্ন–উত্তর

বাংলায় প্রশ্ন করলে bot বাংলায়, English-এ প্রশ্ন করলে English-এ উত্তর দেওয়ার জন্য তৈরি। কোনো তথ্য approved profile বা knowledge-এ না থাকলে এটি অনুমান না করে জানায় যে তথ্যটি দেওয়া নেই।

## এটি কী করে না

এটি Sabina-র ব্যক্তিগত ফাইল বা বাইরের account-এ প্রবেশ করে না এবং calendar, email বা অন্য কাজ পরিচালনা করে না। এটি profile-ভিত্তিক প্রশ্নের উত্তর দেয়।

## চালানোর পদ্ধতি

এই সংস্করণটি আপনার কম্পিউটারে Streamlit ও Ollama দিয়ে চলে। নির্বাচিত Ollama model আগে কম্পিউটারে ইনস্টল থাকতে হবে। চালানোর ধাপের জন্য `README_BN.md`-এর Local Setup অংশ দেখুন।

## Privacy

Chat history browser session-এ থাকে। Admin dashboard থেকে যোগ করা knowledge এই কম্পিউটারে সংরক্ষিত হয়। GitHub-এ `secrets.toml`, password, `.venv` বা ব্যক্তিগতভাবে গোপন রাখতে চান এমন তথ্য যোগ করবেন না। কোনো তথ্য public profile-এ রাখার আগে সেটি দর্শকদের সঙ্গে শেয়ার করতে চান কি না যাচাই করুন।
