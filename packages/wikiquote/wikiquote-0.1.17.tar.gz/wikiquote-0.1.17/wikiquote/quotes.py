from typing import Any, Dict, List, Text

import lxml.html

from . import langs, utils
from .constants import DEFAULT_LANG, DEFAULT_MAX_QUOTES, PAGE_URL, RANDOM_URL, SRCH_URL


def _is_disambiguation(categories: List[Dict[Text, Any]]) -> bool:
    # Checks to see if at least one category includes 'Disambiguation_pages'
    return not categories or any(
        [category["*"] == "Disambiguation_pages" for category in categories]
    )


@utils.validate_lang
def search(s: Text, lang: Text = DEFAULT_LANG) -> List[Text]:
    if not s:
        return []

    local_srch_url = SRCH_URL.format(lang=lang)
    data = utils.json_from_url(local_srch_url, s)
    results = [entry["title"] for entry in data["query"]["search"]]
    return results


@utils.validate_lang
def random_titles(
    lang: Text = DEFAULT_LANG, max_titles: int = DEFAULT_MAX_QUOTES
) -> List[Text]:
    local_random_url = RANDOM_URL.format(lang=lang, limit=max_titles)
    data = utils.json_from_url(local_random_url)
    results = [entry["title"] for entry in data["query"]["random"]]
    return results


@utils.validate_lang
def quotes(
    page_title: Text, max_quotes: int = DEFAULT_MAX_QUOTES, lang: Text = DEFAULT_LANG
) -> List[Text]:
    local_page_url = PAGE_URL.format(lang=lang)
    data = utils.json_from_url(local_page_url, page_title)
    if "error" in data:
        raise utils.NoSuchPageException("No pages matched the title: " + page_title)

    if _is_disambiguation(data["parse"]["categories"]):
        raise utils.DisambiguationPageException("Title returned a disambiguation page.")

    html_content = data["parse"]["text"]["*"]
    html_tree = lxml.html.fromstring(html_content)
    return langs.extract_quotes_lang(lang, html_tree, max_quotes)
