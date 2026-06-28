#!/usr/bin/env python3
"""
IG Story / Feed Poster - Single Source of Truth
Use this instead of inline-writing freeimage + buffer API code (避免打錯 API key)

Usage:
  # Post to IG Story (9:16, no caption, customScheduled)
  from ig_story_poster import post_story
  result = post_story("/path/to/image.jpg", caption="")
  
  # Post to IG Feed (1:1, with caption, customScheduled)
  from ig_story_poster import post_feed
  result = post_feed("/path/to/image.jpg", caption="...", schedule_minutes=2)
  
  # Get URLs only (for manual upload)
  from ig_story_poster import upload_to_freeimage
  url = upload_to_freeimage("/path/to/image.jpg")
"""

import json
import urllib.request
import urllib.error
import os
import datetime

# ===== CONFIG (full keys, never truncate) =====
FREEIMAGE_KEY = "6d207e02198a847aa98d0a2a901485a5"
BUFFER_TOKEN = "zydRgAv3px5-5dxumTcP-whSEctLlVDTtiawT5IbNw8"
BUFFER_CHANNEL_ID = "69a927c13f3b94a12119779f"

FREEIMAGE_API = "https://freeimage.host/api/1/upload"
BUFFER_API = "https://api.buffer.com"


def upload_to_freeimage(image_path):
    """Upload image to freeimage.host, return public URL.
    
    Returns:
        str: image URL on success
        None: on failure
    """
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return None
    
    boundary = "----openclaw" + str(os.getpid())
    with open(image_path, 'rb') as f:
        img_data = f.read()
    
    body = []
    body.append(f"--{boundary}".encode())
    body.append(b'Content-Disposition: form-data; name="key"')
    body.append(b'')
    body.append(FREEIMAGE_KEY.encode())
    body.append(f"--{boundary}".encode())
    body.append(b'Content-Disposition: form-data; name="format"')
    body.append(b'')
    body.append(b'json')
    body.append(f"--{boundary}".encode())
    body.append(f'Content-Disposition: form-data; name="source"; filename="{os.path.basename(image_path)}"'.encode())
    body.append(b'Content-Type: image/jpeg')
    body.append(b'')
    body.append(img_data)
    body.append(f"--{boundary}--".encode())
    body.append(b'')
    data = b'\r\n'.join(body)
    
    req = urllib.request.Request(
        FREEIMAGE_API,
        data=data,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            result = json.loads(r.read())
            if result.get("status_code") == 200 and "image" in result and "url" in result.get("image", {}):
                return result["image"]["url"]
            else:
                print(f"❌ Freeimage error: {result.get('error', result)}")
                return None
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="ignore")
        print(f"❌ Freeimage HTTP {e.code}: {body_text[:300]}")
        return None
    except Exception as e:
        print(f"❌ Freeimage exception: {e}")
        return None


def _post_buffer(image_url, due_at, text, post_type="post", share_to_feed=True):
    """Internal: post to Buffer with given config.
    
    post_type: "post" (Feed) or "story"
    share_to_feed: for story, whether to also share to Feed
    """
    if post_type == "story":
        metadata = {"instagram": {"type": "story", "shouldShareToFeed": share_to_feed}}
    else:  # "post" = Feed
        metadata = {"instagram": {"type": "post", "shouldShareToFeed": True}}
    
    query = """mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id text dueAt status } }
    ... on MutationError { message }
  }
}"""
    
    variables = {
        "input": {
            "schedulingType": "automatic",
            "mode": "customScheduled",
            "dueAt": due_at,
            "text": text,
            "channelId": BUFFER_CHANNEL_ID,
            "assets": [{"image": {"url": image_url}}],
            "metadata": metadata
        }
    }
    
    payload = {"query": query, "variables": variables}
    
    req = urllib.request.Request(
        BUFFER_API,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BUFFER_TOKEN}"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            result = json.loads(r.read())
            data = result.get("data", {}).get("createPost", {})
            if "post" in data:
                return {"success": True, "post": data["post"]}
            else:
                return {"success": False, "error": data.get("message", data)}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        return {"success": False, "error": f"HTTP {e.code}: {body[:300]}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def post_story(image_path, caption="", schedule_minutes=2):
    """Post to IG Story (9:16, no caption needed).
    
    Args:
        image_path: local path to image
        caption: optional caption (rarely used for stories)
        schedule_minutes: how many minutes from now to schedule
    
    Returns:
        dict with success/post or success/error
    """
    url = upload_to_freeimage(image_path)
    if not url:
        return {"success": False, "error": "freeimage upload failed"}
    
    now = datetime.datetime.now(datetime.UTC)
    due_at_dt = now + datetime.timedelta(minutes=schedule_minutes)
    due_at = due_at_dt.strftime("%Y-%m-%dT%H:%M:00.000Z")
    
    return _post_buffer(url, due_at, caption, post_type="story", share_to_feed=False)


def post_feed(image_path, caption="", schedule_minutes=2):
    """Post to IG Feed (1:1, with caption).
    
    Args:
        image_path: local path to image
        caption: full IG caption with hashtags
        schedule_minutes: how many minutes from now to schedule
    
    Returns:
        dict with success/post or success/error
    """
    url = upload_to_freeimage(image_path)
    if not url:
        return {"success": False, "error": "freeimage upload failed"}
    
    now = datetime.datetime.now(datetime.UTC)
    due_at_dt = now + datetime.timedelta(minutes=schedule_minutes)
    due_at = due_at_dt.strftime("%Y-%m-%dT%H:%M:00.000Z")
    
    return _post_buffer(url, due_at, caption, post_type="post")


if __name__ == "__main__":
    # Self-test: verify config
    print("Freeimage Key:", FREEIMAGE_KEY[:10] + "..." + FREEIMAGE_KEY[-5:])
    print("Buffer Token:", BUFFER_TOKEN[:10] + "..." + BUFFER_TOKEN[-5:])
    print("Channel ID:", BUFFER_CHANNEL_ID)
    print("\nAll keys are FULL (not truncated).")
