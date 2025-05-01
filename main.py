import tweepy
import os

# 環境変数からAPIキーを取得（GitHub Secretsから読み込まれる）
API_KEY = os.environ["API_KEY"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

# Tweepyの認証
auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# 最新メンションからチェック
mentions = api.mentions_timeline(count=5)

for mention in mentions:
    text = mention.text
    tweet_id = mention.id
    screen_name = mention.user.screen_name
    reply_to_status_id = mention.in_reply_to_status_id

    # 「@共感チェック」が含まれ、返信元ツイートがあるものだけ処理
    if "共感チェック" in text and reply_to_status_id:
        # 返信元ツイートを取得
        try:
            target = api.get_status(reply_to_status_id)
            target_url = f"https://x.com/{target.user.screen_name}/status/{target.id}"
            diagnosis_url = f"https://kyoukan-checker.jp/?url={target_url}"

            # Botがリプライ送信
            reply_text = f"🔍 共感率診断はこちら！👇\n{diagnosis_url}"
            api.update_status(
                status=reply_text,
                in_reply_to_status_id=tweet_id,
                auto_populate_reply_metadata=True
            )
            print(f"Replied to @{screen_name}")
        except Exception as e:
            print(f"エラー: {e}")
