# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from datetime import datetime

current_year = datetime.now().year

class JobscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name in ['company_name', 'end_date']:
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()
            
            if field_name in ['start_date', 'end_date']:
                date_string = adapter.get(field_name)
                split_date_string = date_string.split(' ')
                month_text = split_date_string[1]
                if month_text == 'იანვარი':
                    month_text = '.01'
                elif month_text == 'თებერვალი':
                    month_text = '.02'
                elif month_text == 'მარტი':
                    month_text = '.03'
                elif month_text == 'აპრილი':
                    month_text = '.04'
                elif month_text == 'მაისი':
                    month_text = '.05'
                elif month_text == 'ივნისი':
                    month_text = '.06'
                elif month_text == 'ივლისი':
                    month_text = '.07'
                elif month_text == 'აგვისტო':
                    month_text = '.08'
                elif month_text == 'სექტემბერი':
                    month_text = '.09'
                elif month_text == 'ოქტომბერი':
                    month_text = '.10'
                elif month_text == 'ნოემბერი':
                    month_text = '.11'
                elif month_text == 'დეკემბერი':
                    month_text = '.12'
                
                adapter[field_name] = split_date_string[0] + month_text + '.' + str(current_year)
                
                
        
                
        return item
