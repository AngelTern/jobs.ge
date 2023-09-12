import scrapy
from jobscraper.items import JobscraperItem
from scrapy.exceptions import CloseSpider


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["jobs.ge"]
    start_urls = ["https://jobs.ge/?page=1&q=&cid=0&lid=0&jid=0&in_title=0&has_salary=0&is_ge=0&for_scroll=yes"]
    page_number = 1
    prev_page_number = 0
    #custom_settings = {
    #    'DOWNLOAD_DELAY': 1,  # Initial delay between requests (in seconds)
    #    'CONCURRENT_REQUESTS': 1,  # Number of concurrent requests (set to 1)
    #    'AUTOTHROTTLE_ENABLED': True,  # Enable autothrottle
    #} 
    last_page_reached = 0

    def parse(self, response):
        
        #შემოწმება რომ პირველი ელემენტი არ უდრის წინა გვერდის ელემენტს სავარაუდოდ ჰრეფებით
        #სიგრძეებით დროებითია მარა მუშაობს თუმცა 1/300 შანსია რო გაჭედავს და უსასროლო გახდება :)
        #jobs = response.css('tr')
        #if len(jobs)!= 300:
        #    self.last_page_reached += 1
        #    
        #if self.last_page_reached == 2:
        #    raise CloseSpider('მეტი აღარაა')
       # 
        item = JobscraperItem()
        jobs = response.css('tr')
        for job in jobs:
            job_title = job.css('td:nth-of-type(2) a:nth-of-type(1) ::text').get()
            company_name = job.css('td:nth-of-type(4) a ::text').get()
            start_date = job.css('td:nth-of-type(5) ::text').get()
            end_date = job.css('td:nth-of-type(6) ::text').get()
            item['job_title'] = job_title
            item['company_name'] = company_name
            item['start_date'] = start_date
            item['end_date'] = end_date
            yield item
        
        
        
        
        
        
        
            
        if self.page_number == 18:
            raise CloseSpider('vso')
        else:    
            self.page_number += 1
        next_page_url = f"https://jobs.ge/?page={self.page_number}&q=&cid=0&lid=0&jid=0&in_title=0&has_salary=0&is_ge=0&for_scroll=yes"
        yield response.follow(next_page_url, callback = self.parse)