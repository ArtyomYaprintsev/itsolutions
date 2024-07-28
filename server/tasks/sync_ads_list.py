import logging
from urllib.parse import urljoin

from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup, ResultSet, Tag
from httpx import Client
from pydantic_core import Url

from server.core.settings import settings
from server.repositories.ad import save_actual_ads
from server.schemas import ad as schema_ad
from server.worker import app

logger = logging.getLogger(__name__)


request_params = {
    'headers': {
        'User-Agent': settings.REQUEST_USER_AGENT,
    },
    'cookies': {},
}


def _fetch_page(url: str) -> str | None:
    logger.info(f'Fetching {url}')

    with Client() as client:
        response = client.get(
            url,
            headers=request_params['headers'],
            cookies=request_params['cookies'],
        )

        logger.debug(f'COOKIES: {response.cookies}')
        logger.debug(f'HEADERS: {response.headers}')

        if response.status_code == 200:
            return response.text

        if response.status_code == 301:
            redirect = response.headers.get('Location')

            if redirect:
                logger.warning(
                    'Received response with 301 status code. Try to fetch: '
                    f'{redirect}',
                )
                return _fetch_page(redirect)

        return None


def _get_ad_author(ad_id: str) -> schema_ad.AdAuthor | None:
    url = urljoin(
        settings.SOURCE_HOST,
        settings.RETRIEVE_AD_PATH_PATTERN.format(ad_id=ad_id),
    )

    response = _fetch_page(url=url)

    if not response:
        raise ValueError('Response is None')

    soup = BeautifulSoup(response, 'html.parser')

    author_container = soup.find('span', {'class': 'userNick'})

    if not author_container:
        return None

    author_data = author_container.find('a')

    if not isinstance(author_data, Tag):
        return None

    author_href = author_data.get('href') or ''

    if isinstance(author_href, list):
        author_href = author_href[0]

    return schema_ad.AdAuthor(
        author=author_data.text,
        author_link=urljoin(settings.SOURCE_HOST, author_href),  # type: ignore
    )


def _get_ads_list() -> ResultSet[Tag]:
    url = urljoin(settings.SOURCE_HOST, settings.LIST_ADS_PATH)

    response = _fetch_page(url=url)

    if not response:
        raise ValueError('Response is None')

    soup = BeautifulSoup(response, 'html.parser')

    ads_list = soup.find_all(
        'tr',
        {'class': 'bull-list-item-js'},
        limit=settings.SYNC_ADS_SIZE,
    )

    return ads_list


def _parse_ad_tag_to_schema_ad(ad_as_tag: Tag) -> schema_ad.Ad:
    ad_tag_a = ad_as_tag.find('a')

    if not isinstance(ad_tag_a, Tag):
        raise ValueError('Provided ad tag has not contain `<a>` tag with id')

    ad_id = ad_tag_a.get('name') or ''

    if isinstance(ad_id, list):
        ad_id = ad_id[0]

    header = ad_as_tag.find('a', {'class': 'bull-item__self-link'})
    address = ad_as_tag.find('div', {'class': 'address'})
    views_count = ad_as_tag.find('span', {'class': 'views'})

    ad_author = _get_ad_author(ad_id)

    return schema_ad.Ad(
        id=ad_id,
        header=header.text if header else '',
        is_archived=False,
        address=address.text if address else '',
        views_count=int(views_count.text) if views_count else 0,
        **ad_author.model_dump() if ad_author else {},
    )


@app.task(name='sync_ads_list')
def sync_ads_list():
    """Sync actual ads list with source."""
    ads_list = _get_ads_list()

    result: list[schema_ad.Ad] = []

    for index, ad in enumerate(ads_list):
        parsed_ad = _parse_ad_tag_to_schema_ad(ad)
        parsed_ad.position = index + 1
        result.append(parsed_ad)

    async_to_sync(save_actual_ads)(result)
