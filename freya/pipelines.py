# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime

def calculate_job_age(first_seen, last_seen):
    date_format = "%Y-%m-%d %H:%M:%S"
    first_seen_date = datetime.strptime(first_seen, date_format)
    last_seen_date = datetime.strptime(last_seen, date_format)
    diff_days = abs((last_seen_date - first_seen_date).days)

    print(f"First seen: {first_seen}, Last seen: {last_seen}, Difference in days: {diff_days}")

    if diff_days <= 7:
        return 'new'
    elif 8 <= diff_days <= 15:
        return 'recent'
    elif 16 <= diff_days <= 30:
        return 'stale'
    else:
        return 'expired'

class FreyaPipeline:
    def process_item(self, item, spider):
        first_seen = item.get('first_seen', '')
        last_seen = item.get('last_seen', '')

        if first_seen and last_seen:
            item['job_age'] = calculate_job_age(first_seen, last_seen)
        else:
            item['job_age'] = 'unknown'

        return item