# Sabina Akter-এর Personal AI chatbot

এই app আপনার কম্পিউটারের Ollama model ব্যবহার করে। OpenAI API key বা API billing লাগে না। প্রথমবার মডেল ডাউনলোডে ইন্টারনেট লাগবে; এরপর উত্তর স্থানীয়ভাবে তৈরি হবে।

## ZIP-এর ফাইল

- `app.py` — Public Chat, Admin sign-in ও dashboard
- `profile.md` — Sabina-র public তথ্য
- `system_prompt.txt` — chatbot-এর উত্তর ও গোপনীয়তার নিয়ম
- `Figma_UI_Brief_BN.md` — UI design brief
- `requirements.txt` — Python package

## চালানোর ধাপ

1. Ollama ইনস্টল করুন: [Ollama for Windows](https://ollama.com/download/windows)
2. PowerShell-এ চালান:

   ```powershell
   ollama run qwen3:0.6b
   ```

   প্রথমবার প্রায় ৫২৩ MB ডাউনলোড হবে। শেষ হলে `/bye` লিখে Enter দিন।
3. ZIP extract করে ফোল্ডারটি PyCharm-এ Open করুন।
4. PyCharm-এর Terminal-এ চালান:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```
5. Browser-এ `http://localhost:8501` খুলুন। বন্ধ করতে Terminal-এ `Ctrl+C` চাপুন।

## Admin password সেট করা

Admin page password দিয়ে বন্ধ থাকবে। ZIP-এ `.streamlit/secrets.toml.example` দেওয়া আছে। নিজের project-এ সেটি copy করে একই folder-এ `secrets.toml` নামে রাখুন, তারপর নিজের password লিখে save করুন:

```toml
ADMIN_USERNAME = "sabina"
ADMIN_PASSWORD = "নিজের-দীর্ঘ-পাসওয়ার্ড-এখানে"
```

নিজের password বসিয়ে save করুন, তারপর app বন্ধ করে আবার চালান। Public chat-এর উপরের **Admin** button চাপুন, sign in করলে dashboard খুলবে। আসল password ZIP-এ বা public GitHub-এ রাখবেন না। এই local login public website-এর production নিরাপত্তা নয়; internet-এ প্রকাশের আগে আলাদা secure hosting ও authentication লাগবে.

## Figma UI

App-এ Public Chat, Admin sign-in এবং ব্যক্তিগত Admin Dashboard আছে। বাম পাশের **Biography**, **Family History**, **Knowledge Training Studio**, **Chat Appearance**, এবং **Local Model** অংশ থেকে তথ্য ও সেটিংস সামলাতে পারবেন। Knowledge Training Studio-তে এক পাশে নতুন knowledge যোগ এবং অন্য পাশে saved entry খোঁজা, সম্পাদনা ও মুছে ফেলা যায়। Visitor chat history রাখা হয় না।

Figma-তে মূল design ও code-এর মধ্যে সব পরিবর্তন স্বয়ংক্রিয়ভাবে sync হয় না; code-এর পরিবর্তন app-এ দেখা যায়, Figma file-এ নয়।

## Chat ও privacy

- Chat history শুধু browser session-এ থাকে; page refresh বা session শেষ হলে মুছে যায়।
- প্রশ্ন Ollama-তে আপনার কম্পিউটারের local connection দিয়ে যায়; OpenAI API-তে যায় না।
- Local model live web search করে না; চলতি তথ্য আলাদা করে যাচাই করুন।
- `profile.md`-তে public তথ্য বদলাতে পারেন। নিয়োগকর্তার নাম যোগ করবেন না।

## AI-কে নতুন উত্তর শেখানো

এখানে “শেখানো” বলতে model-এর ভিতরের weight বদলানো নয়। Admin dashboard-এর **Knowledge Training Studio** খুলুন। বাম দিকের ফর্মে Category, Question variations (প্রতি লাইনে একটি), বাংলা উত্তর এবং English উত্তর দিন; **Save knowledge** চাপুন। ডান পাশে saved entry খুঁজে **Edit** বা **Delete** করতে পারবেন। তথ্য `knowledge.json`-এ এই কম্পিউটারে save হয় এবং মিলে যাওয়া প্রশ্নে অনুমোদিত উত্তর দেয়। Sabina-র কোনো ব্যক্তিগত তথ্য profile বা knowledge-এ না থাকলে assistant ভদ্রভাবে বলবে যে অনুমোদিত profile-এ তথ্যটি নেই; অনুমান করবে না। নতুন তথ্য যোগের পর public chat-এ **New chat** খুলে চেষ্টা করুন। গোপন তথ্য বা নিয়োগকর্তার নাম public knowledge-এ যোগ করবেন না।
