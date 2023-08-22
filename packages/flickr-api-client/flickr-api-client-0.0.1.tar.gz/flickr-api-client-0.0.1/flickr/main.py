import asyncio
import logging.config
import platform
import re
from logging import getLogger, Logger

import httpx
import pandas as pd
import reqx
from httpx import Client, Response

try:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        import nest_asyncio

        nest_asyncio.apply()
except:
    ...

if platform.system() in {'Darwin', 'Linux'}:
    try:
        import uvloop

        uvloop.install()
    except ImportError as e:
        ...

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {'standard': {'format': '%(asctime)s.%(msecs)03d [%(levelname)s] :: %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}},
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'standard', 'stream': 'ext://sys.stdout'},
        'file': {'class': 'logging.FileHandler', 'level': 'DEBUG', 'formatter': 'standard', 'filename': 'log.log', 'mode': 'a'},
    },
    'loggers': {'my_logger': {'handlers': ['console', 'file'], 'level': 'DEBUG'}}
})
logger = getLogger(list(Logger.manager.loggerDict)[-1])

PRIMARY_PHOTO_EXTRAS = {
    'needs_interstitial', 'can_share', 'url_3k', 'url_4k', 'url_5k', 'url_6k', 'url_c', 'url_h', 'url_k', 'url_l', 'url_m', 'url_n', 'url_o', 'url_q',
    'url_s', 'url_sq', 'url_t', 'url_w', 'url_z'
}
EXTRAS = PRIMARY_PHOTO_EXTRAS | {
    'can_addmeta', 'can_comment', 'can_download', 'can_print', 'can_share', 'contact', 'content_type', 'count_comments',
    'count_faves', 'count_views', 'date_activity', 'date_activity_detail', 'date_taken', 'date_upload', 'datecreate',
    'description', 'eighteenplus', 'icon_urls', 'icon_urls_deep', 'invitation_only', 'isfavorite', 'ispro', 'license', 'media',
    'member_pending_count', 'muted', 'non_members_privacy', 'o_dims', 'owner_datecreate', 'owner_name', 'path_alias', 'perm_print',
    'pool_pending_count', 'privacy', 'publiceditability', 'realname', 'rotation', 'safety_level', 'secret_h', 'secret_k', 'sizes',
    'system_moderation', 'visibility', 'visibility_source'
}


class Flickr:
    def __init__(self, login_config: dict = None):
        self.base_url = 'https://api.flickr.com/services/rest'
        # "csrf" is found in request params
        self.client = self._init_client(login_config)

    def _init_client(self, login_config: dict):
        x = 'root.YUI_config.flickr-api-client.api.site_key'
        api_key = re.findall(f'{x}\s?=\s?"(.*)";?', httpx.get('https://flickr.com/', headers={"user-agent": "Mozilla/5.0"}).text)[0]
        return Client(
            http2=True,
            follow_redirects=True,
            timeout=30,
            verify=False,
            base_url=self.base_url,
            cookies=login_config['cookies'] if login_config else None,
            headers={
                "user-agent": "Mozilla/5.0",
            },
            params=(login_config['params'] if login_config else {}) | {
                "api_key": api_key,
                "format": "json",
                "hermes": "1",
                "hermesClient": "1",
                "nojsoncallback": "1",
            }
        )

    async def _process(self, params: dict, **kwargs) -> tuple[Response]:
        return await reqx.process(
            reqx.send(
                'GET',
                [self.client.base_url],
                headers=self.client.headers,
                cookies=self.client.cookies,
                params=dict(self.client.params) | params
            ),
            http2=True,
            follow_redirects=True,
            timeout=60,
            **kwargs
        )

    def user_ids(self, usernames: list[str], **kwargs) -> dict:
        res = asyncio.run(self._process({
            'method': 'flickr-api-client.people.findByUsername',
            'username': usernames
        }, **kwargs))
        return {r.json().get('user', {}).get('username', {}).get('_content'): r.json().get('user', {}).get('id') for r in res}

    def popular(self, user_ids: list[str], pages: int, per_page: int = 1000, sort: str = '', **kwargs) -> pd.DataFrame:
        res = asyncio.run(self._process({
            'page': range(1, pages + 1),
            'method': 'flickr-api-client.photos.getPopular',
            'nsid': user_ids,
            'user_id': user_ids,
            'per_page': per_page,
            'sort': sort,  # {'views', 'interesting', 'comments'} 'favorites'?
            'view_as': 'ff',
        }, **kwargs))
        return pd.json_normalize(y for x in res for y in x.json()['photos']['photo'])

    def photosets(self, photoset_ids: list[int], pages: int, per_page: int = 1000, **kwargs) -> pd.DataFrame:
        res = asyncio.run(self._process({
            'extras': ','.join(EXTRAS),
            'per_page': per_page,
            'page': range(1, pages + 1),
            'get_user_info': 1,
            'primary_photo_extras': ','.join(PRIMARY_PHOTO_EXTRAS),
            'jump_to': '',
            'photoset_id': photoset_ids,
            'method': 'flickr-api-client.photosets.getPhotos',
        }, **kwargs))
        return pd.json_normalize(filter(len, (y for x in res for y in x.json().get('photoset', {}).get('photo', []))))

    def profiles(self, user_ids: list[str], **kwargs) -> pd.DataFrame:
        res = asyncio.run(self._process({
            'method': ['flickr-api-client.profile.getProfile', 'flickr-api-client.people.getInfo'],
            'user_id': user_ids
        }, **kwargs))
        return (
            pd.json_normalize(r.json().get('profile') or r.json().get('person') for r in res)
            .assign(join_date=lambda x: pd.to_datetime(x['join_date'], unit='s'))
            .groupby('id', as_index=False).first()
        )

    def sizes(self, photo_ids: list[int], hq_only: bool = True, **kwargs) -> pd.DataFrame:
        res = asyncio.run(self._process({
            'method': 'flickr-api-client.photos.getSizes',
            'photo_id': photo_ids
        }, **kwargs))
        df = (
            pd.json_normalize(y for x in res for y in x.json()['sizes']['size'])
            .dropna(subset=['width', 'height'])
            .assign(width=lambda x: x['width'].astype(int), height=lambda x: x['height'].astype(int))
        )
        df['id'] = df['source'].str.split('live.staticflickr.com/\d+/(\d+)_', expand=True, regex=True)[1]
        if hq_only:
            df['px'] = df['width'] * df['height']
            return df.sort_values('px', ascending=False).groupby('id').first().reset_index()
        return df

    def favoriters(self, photo_ids: list[int], pages: int, per_page: int = 1000, **kwargs) -> pd.DataFrame:
        res = asyncio.run(self._process({
            'method': 'flickr-api-client.photos.getFavorites',
            'photo_id': photo_ids,
            'per_page': per_page,
            'page': range(1, pages + 1),
            'sort': 'date_desc',
        }, **kwargs))
        important_cols = {
            'nsid',
            'dbid',
            'username',
            'realname',
            'favedate',
        }
        df = (
            pd.json_normalize(y for x in res for y in x.json()['photo']['person'])
            .drop_duplicates(subset=['nsid'])
            .assign(favedate=lambda x: pd.to_datetime(x['favedate'], unit='s'))
        )
        return df[[*important_cols, *set(df.columns) - important_cols]]

    def favorites(self, *, user_ids: list[str] = None, usernames: list[str] = None, pages: int, per_page: int = 1000, **kwargs):
        if user_ids is None:
            user_ids = list(self.user_ids(usernames).values())
        res = asyncio.run(self._process({
            'method': 'flickr-api-client.favorites.getList',
            'user_id': user_ids,
            'per_page': per_page,
            'page': range(1, pages + 1),
        }, **kwargs))
        data = (y['photo'] for x in res if (y := x.json().get('photos')))
        return pd.json_normalize(y for x in data for y in x)
