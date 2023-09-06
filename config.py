from dotenv import dotenv_values

COMMENT_LIMIT = 100

values = dotenv_values("../venv/.env")

# TikTok Account MS_TOKEN (paste 'js/ms_token.js' to browser to get token)
ms_token = values.get("MS_TOKEN", None)
