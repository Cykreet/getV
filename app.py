import requests

from sanic import Sanic
from sanic.response import json

from sanic_limiter import Limiter, get_remote_address
from bs4 import BeautifulSoup

async def ratelimit_handler(request, exception):
    return json({"error": f"Ratelimit exceeded {exception}."}, status=429)

app = Sanic()
app.error_handler.add(Exception, ratelimit_handler)

limiter = Limiter(app, global_limits=["1 per 3 seconds", "50 per hour"], key_func=get_remote_address)

@app.route("/")
async def main(request):
    if not (bot := request.args.get("bot")):
        return json({"error": "Bot query is required. Example: ?bot=atlas"})

    soup = BeautifulSoup((response := requests.get(f"https://top.gg/bot/{bot}")).content, "html.parser")

    if (status := response.status_code) not in [200, 204]:
        return json({"status": status, "error": f"Failed to get info on \"{bot}\"."})

    try:
        votes = int(soup.find(id="points").string.strip())
    except:
        return json({"status": status, "error": "Was unable to parse bot votes."})

    return json({"status": status, "name": soup.find("span", {"class": "bot-name"}).string.strip() if soup.find("span", {"class": "bot-name"}) else bot, "votes": votes})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9500)