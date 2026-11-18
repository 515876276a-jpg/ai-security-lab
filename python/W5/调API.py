import os
import json
import requests

key = os.environ.get("DEEPSEEK_API_KEY")
if not key:
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as reg:
        key = winreg.QueryValueEx(reg, "DEEPSEEK_API_KEY")[0]

resp = requests.post(
    "https://api.deepseek.com/chat/completions",
    headers={"Authorization": "Bearer " + key},
    json={"model": "deepseek-flash",
          "messages": [{"role": "user", "content": "用一句话说明什么是哈希函数"}],
          "stream": False},
    timeout=60,
)
print(resp.status_code)
data = resp.json()
print(data["choices"][0]["message"]["content"])
print(json.dumps(data["usage"], ensure_ascii=False))
