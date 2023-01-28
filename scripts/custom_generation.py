# SPDX-FileCopyrightText: 2020 Carl Schwan <carl@carlschwan.eu>
# SPDX-FileCopyrightText: 2021-2022 Phu Hung Nguyen <phu.nguyen@kdemail.net>
# SPDX-License-Identifier: LGPL-2.0-or-later

import concurrent.futures
import configparser
import importlib.resources as pkg_resources
import logging
import os
import re
import socket
import time
import unicodedata
from importlib.metadata import version

import feedparser
# from hugoi18n import command_line, generation
from yaml import safe_load, dump


def parameterize(string, sep='-'):
    """
    Mimic Ruby String#parameterize function
    :param string:
    :param sep:
    :return:
    """
    parameterized = unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode()
    parameterized = re.sub(r'[^a-zA-Z\d\-_]+', sep, parameterized)
    parameterized = re.sub(rf'{sep}{{2,}}', sep, parameterized)
    return parameterized.strip(sep).lower()


def render_post(file_path, feed_fields, site_link, entry):
    published = entry.published_parsed if 'published_parsed' in entry else entry.updated_parsed
    published_date = time.strftime('%Y-%m-%d', published)
    file_name = f"{parameterize(feed_fields['author'])}-{published_date}-{parameterize(entry.title)}"
    content = entry.content[0]['value'] if 'content' in entry else entry.summary if 'summary' in entry else ''

    # Make absolute links with site url
    cut_url = re.search(r'//.*?(?=/|$)', site_link).group(0) + '/'
    content = re.sub(r'(?<=src=[\"\'])/(?!/)', cut_url, content)
    content = re.sub(r'(?<=href=[\"\'])/(?!/)', cut_url, content)
    # Make browsers not report page as having non-HTTPS elements
    content = re.sub(r'(?<=src=[\"\'])http:', 'https:', content)
    content = re.sub(r'(?<=href=[\"\'])http:', 'https:', content)
    # Open links in new tabs
    content = re.sub(r'(href=[\"\']//)', r'target="_blank" \1', content)
    # Make page style consistent
    content = re.sub(r'<link [^>]*rel=[\"\']stylesheet[^>]+>', '', content)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.M | re.S)
    # Replace iframe elements with a message telling users to look for them in original posts
    content = re.sub(r'<iframe[^>]*/>', '<i>An iframe has been removed to ensure Planet works properly. '
                                        'Please find it in the original post.</i>', content, flags=re.M)
    # Escaping braces make scripts inside content invalid. Let's remove scripts altogether
    content = re.sub(r'<script[^>]*>.*?</script>',
                     '<i>A script element has been removed to ensure Planet works properly. '
                     'Please find it in the original post.</i>', content, flags=re.M | re.S)  # dot matches all
    # After including date in each post file name, some posts appear with shortcode snippets in the content
    content = re.sub('{', '&#123;', content)
    # Site specifics
    # https://outsideofinfinity.wordpress.com/2020/05/04/what-is-krita-up-to-now/
    content = re.sub(r'(id[:=] ?)[\'"]atatags-[^"\']*[\'"]', r'\1""', content)
    # https://labplot.kde.org/2022/03/22/labplot-2-9-beta/ and others on https://labplot.kde.org
    content = re.sub(r'data-rel="lightbox-gallery-[^"]*"', '', content)

    post_fields = feed_fields.copy()
    post_fields['title'] = entry.title
    post_fields['date'] = time.strftime('%Y-%m-%dT%H:%M:%S%z', published)
    post_fields['lastmod'] = time.strftime('%Y-%m-%dT%H:%M:%S%z', entry.updated_parsed)
    post_fields['post_url'] = entry.link
    post_fields['guid'] = entry.id
    return {'path': f'{file_path}/{file_name}.html',
            'updated': entry.updated_parsed,
            'fm': post_fields,
            'content': content}


def process_feed(feed_id, feed_config) -> list:
    if 'feed_url' not in feed_config:
        logging.warning(f'{feed_id} has no feed_url')
        return []
    logging.info(f'processing feed {feed_id}')
    feed_url = feed_config['feed_url']
    # all HTTP libraries work with sockets, so we set timeout for each socket operation
    socket.setdefaulttimeout(120)

    feed_data = feedparser.parse(feed_url, resolve_relative_uris=False, sanitize_html=False)
    if feed_data.bozo:
        exception = feed_data.bozo_exception
        if type(exception) not in {feedparser.exceptions.CharacterEncodingOverride}:
            logging.warning(f'feed {feed_id}: {type(exception)}, {exception}')
            return []
    site_link = feed_data.feed.get('link', '/'.join(feed_url.split('/')[:3]))
    site_url = feed_config.get('site_url', site_link)
    site_tags = feed_config.get('tags', '').split(';')
    feed_fields = {'feed_url': feed_url,
                   'site_url': site_url,
                   'avatar': feed_config.get('avatar', '')}
    if (len(site_tags) > 0):
        feed_fields['tags'] = site_tags
    for flair in feed_config.get('flairs', ';').split():
        if ':' in flair:
            parts = flair.split(':', 1)
            feed_fields[parts[0]] = parts[1]
        else:
            feed_fields[flair] = True
    feed_title = feed_config.get('title', '')
    in_feed_title = feed_data.feed.get('title', '')
    logging.info(f'title in config: {feed_title}; title in feed: {in_feed_title}')
    feed_fields['author'] = feed_title or in_feed_title
    feed_fields['feed_summary'] = feed_data.feed.get('subtitle', '')
    feed_fields['format'] = feed_data.version
    feed_lang = feed_config.get('lang', 'en')
    file_path = 'content' # if feed_lang == 'en' else f'content-trans/{feed_lang}'
    os.makedirs(file_path, exist_ok=True)
    return [render_post(file_path, feed_fields, site_link, entry) for entry in feed_data.entries]


def generate_posts():
    config = configparser.RawConfigParser()
    config.read('planet.ini')
    config.read('sig.ini')
    feed_ids = list(config.keys())
    try:
        feed_ids.remove('DEFAULT')
    except KeyError:
        pass
    entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # Mark each future with its feed id
        future_to_feed = {executor.submit(process_feed, feed_id, config[feed_id]): feed_id for feed_id in feed_ids}
        for future in concurrent.futures.as_completed(future_to_feed):
            feed_id = future_to_feed[future]
            try:
                feed_entries = future.result()
                entries.extend(feed_entries)
            except Exception as e:
                logging.warning('Feed %r generated an exception (%s): %s' % (feed_id, type(e), e))
            else:
                logging.info(f'Processed feed {feed_id}')
    entries.sort(key=lambda x: x['updated'], reverse=True)
    for e in entries[:1300]:
        logging.info(f"{e['path']}: {time.strftime('%Y-%m-%dT%H:%M:%S%z', e['updated'])}")
        with open(e['path'], 'w') as post_file:
            post_file.write('---\n')
            post_file.write(dump(e['fm'], default_flow_style=False, allow_unicode=True))
            post_file.write('---\n')
            post_file.write(e['content'])


domain_name = "planet-kde-org"


def generate():
    generate_posts()

    if not (os.path.isdir('content') and len(os.listdir('content')) > 0):
        return

    # en_strings, configs, original_configs, _ = generation.read_sources()

    # content_lang_codes = ['en']
    # for lang in os.listdir('content-trans'):
    #     if len(os.listdir(f'content-trans/{lang}')) > 0:
    #         content_lang_codes.append(lang)
    # lang_config = list(configs['languages'].keys())
    # with pkg_resources.open_text('hugoi18n.resources', 'languages.yaml') as f_langs:
    #     lang_names = safe_load(f_langs)
    # for config_lang_code in lang_config:
    #     if config_lang_code not in content_lang_codes:
    #         del configs['languages'][config_lang_code]

    # os.environ["PACKAGE"] = 'websites-planet-kde-org'
    # po_dir = 'pos'
    # command_line.fetch_langs(content_lang_codes, False, po_dir)
    # command_line.compile_po_in(po_dir)

    # for hugo_lang_code in content_lang_codes:
    #     if hugo_lang_code in ['en']:
    #         continue
    #     else:
    #         lang_code = generation.revert_lang_code(hugo_lang_code)
    #         os.environ["LANGUAGE"] = lang_code
    #         tr = generation.gettext_func(domain_name)

    #         strings_result = generation.render_strings(en_strings, tr)
    #         target_strings = strings_result[0] if hugoi18n_version == '0.4' else strings_result.localized
    #         generation.write_strings(target_strings, hugo_lang_code)
    #         generation.generate_languages(configs, lang_names, lang_code, hugo_lang_code)
    #         configs['languages'][hugo_lang_code]['contentDir'] = f'content-trans/{hugo_lang_code}'
    #         generation.generate_menu(configs, hugo_lang_code, tr)
    #         generation.generate_description(configs, hugo_lang_code, tr)
    #         generation.generate_title(configs, hugo_lang_code, tr)

    # generation.write_target(configs, original_configs)


if __name__ == "__main__":
    level = logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=level)
    # hugoi18n_version = version('hugoi18n')
    # logging.info(f'Using hugoi18n v{hugoi18n_version}')
    generate()
