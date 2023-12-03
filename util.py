import json

def quickchart(c_type, data):
    url="https://quickchart.io/chart"
    chart = {
        "type": c_type,
        "data": data,
    }

    encoded = json.dumps(chart, separators=(",", ":"))

    return f"{url}?c={encoded}"

def slack_text_block(text, text_type="plain_text"):
    return {
        "type": "section",
        "text": {
            "type": text_type,
            "text": text,
        },
    }

def slack_image_block(title, url):
    return {
        "type": "image",
        "title": {
            "type": "plain_text",
            "text": title,
        },
        "image_url": url,
        "alt_text": title,
    }
