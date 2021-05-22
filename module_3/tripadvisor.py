#!/usr/bin/env python3.7

import time
import asyncio
import aiohttp
from numpy.core.numeric import full
import pandas as pd
from lxml import html
from lxml import etree


def get_review_ratings_from(tree):
    ratings = []
    user_choices = tree.xpath('//*[@class="choices"]')
    if len(user_choices) == 0:
        return []

    user_choices = user_choices[0]
    checkboxes = user_choices.xpath('./*[@class="ui_checkbox item"]')
    for box in checkboxes:
        value = box.xpath('./*[@class="row_num  is-shown-at-tablet"]')
        if len(value) > 0 :
            ratings.append((box.get('data-value'), value[0].text))
    return ratings

def get_rating(node):
  for i, k in enumerate((10, 20, 30, 40, 50)):
    rate = node.xpath(f'.//*[@class="ui_bubble_rating bubble_{k}"]')
    if len(rate) > 0:
      return i+1

def get_review_from(tree):
    review_list = []
    reviews = tree.xpath('//*[@class="review-container"]')
    for review in reviews:
        id = review.get('data-reviewid')
        review_text = None
        summary = review.xpath('./*/*/*/*/*[@class="prw_rup prw_reviews_text_summary_hsx"]')
        if len(summary) > 0 :
            summary = summary[0]
            textcont = summary.xpath('./div/p')
            if len(textcont) > 0 :
                review_text = textcont[0].text

        visit_date = None
        visit = review.xpath('./*/*/*/*/*[@class="prw_rup prw_reviews_stay_date_hsx"]')
        if len(visit) > 0 :
            visit = visit[0].text_content().split(":")
            if len(visit) == 2 :
                visit_date = visit[1]

        rating = get_rating(review)

        usefull_count = None
        usefull = review.xpath('.//*[@class="numHelp "]')
        if len(usefull) > 0:
            usefull = usefull[0].text
            if usefull:
                usefull_count = usefull.split()[0]

        review_list.append((id, visit_date, review_text, rating, usefull_count))
    return review_list


async def get(i, url, session):
    try:
        async with session.get(url=url) as response:
            resp = await response.read()
            htmltext = resp.decode('utf-8')
            # print("Successfully got url {} with resp of length {}.".format(url, len(htmltext)))
            parser = html.HTMLParser(recover=True, encoding='utf-8')
            tree = etree.fromstring(htmltext, parser)
            res = (url, get_review_ratings_from(tree), get_review_from(tree))
            print(f'{i} completed')
            return res

    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))

async def process(k, urls):
    print(f"processing batch {k}")
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(i, 'https://www.tripadvisor.com' + url, session) for i, url in enumerate(urls)])

        # print(ret)
        res = pd.DataFrame(ret, columns=['url', 'rating', 'reviews'])
        res.to_csv(f"ta_parsing_results_{k}.csv", encoding='utf-8')


def batches(list, batch_size):
    full_batch_count = len(list) // batch_size
    for i in range(full_batch_count):
        yield (i, list[i*batch_size : (i+1)*batch_size])
    if batch_size * full_batch_count < len(list):
        yield (full_batch_count, list[batch_size * full_batch_count])



df = pd.read_csv('ta_all_data.csv', sep=',')

for k, batch in batches(df['URL_TA'], 5000):
    asyncio.run(process(k, batch))
    time.sleep(60)

