# Figma UI brief — Sabina's Personal AI

Create two editable desktop web screens with a responsive mobile layout. Keep the interface clear for a nontechnical audience. Use a calm navy/teal palette, warm white backgrounds, readable typography, simple icons, and visible Bengali/English language support.

## Screen 1: Public chat
- Product name: Sabina's Personal AI
- Header subtitle: “Ask about Sabina, AI engineering, cybersecurity, or cloud security.”
- Main area: friendly welcome, four clickable prompt suggestions, chat bubbles, and a clear message box with send button.
- Suggested prompts: “Who owns this assistant?”, “Tell me about Sabina”, “What does she do in cybersecurity?”, “Explain cloud security simply.”
- Small status text: “Runs on this computer” and “Chat clears when refreshed”. Avoid API, model, and terminal jargon in the main experience.
- Privacy: no employer names, no birth year/place, no children's names or birthdays. Family details shown only according to the public profile.

## Screen 2: Admin sign-in and dashboard
- Separate Admin sign-in screen with password field and a clear sign-in button.
- Dashboard header: “Admin Dashboard” with a visible “Private access” badge.
- Navigation: Overview, Profile & Knowledge, Chat appearance, Local model.
- Overview cards: chatbot status, local model status, profile last updated.
- Profile & Knowledge page: editable biography/knowledge text with Save changes and Preview buttons.
- Chat appearance page: edit display name, short description, suggested questions, and language labels.
- Local model page: model name and whether Ollama is connected; do not show secrets or API keys.
- Do not display visitor chat history because this starter app does not store it.

## Interaction / security notes
- Public chat is for anyone. Admin tools are restricted to the owner.
- Use a password-protected admin flow. Do not design public controls that expose profile editing.
- The current local app is a simple Streamlit implementation. This Figma file is a visual prototype; the visual design must later be implemented in app code.
