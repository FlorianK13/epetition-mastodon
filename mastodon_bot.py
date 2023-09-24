from mastodon import Mastodon
from download_petition import get_10k_post

mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
status = get_10k_post()[0]
if status is not None:
    print(status)
    mastodon.status_post(status, visibility="public")