# API Key Configuration Report

All API keys for the Monu-1 project are stored securely in `/data/data/com.termux/files/home/.monu_secrets/`.

## Key Mapping

| Provider/Service | Storage File Path | Required Key Type |
| :--- | :--- | :--- |
| **Gemini** | `/data/data/com.termux/files/home/.monu_secrets/Gemini.json` | Gemini API Key |
| **Cohere** | `/data/data/com.termux/files/home/.monu_secrets/Cohere.json` | Cohere API Key |
| **GitHub** | `/data/data/com.termux/files/home/.monu_secrets/GitHub.json` | GitHub Personal Access Token |

## Instructions
1.  Navigate to `/data/data/com.termux/files/home/.monu_secrets/`.
2.  Open the corresponding `.json` file for the service you wish to configure.
3.  Replace the placeholder `YOUR_..._KEY_HERE` with your actual API key/token.
4.  Ensure the file format remains a valid JSON array: `["your-key-here"]`.
5.  Do **not** commit these files to version control.
