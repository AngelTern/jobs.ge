import scrapy
from jobscraper.items import JobscraperItem
from scrapy.exceptions import CloseSpider


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["jobs.ge"]
    start_urls = ["https://jobs.ge/?page=1&q=&cid=0&lid=0&jid=0&in_title=0&has_salary=0&is_ge=0&for_scroll=yes"]
    page_number = 1
    #custom_settings = {
    #    'DOWNLOAD_DELAY': 1,  # Initial delay between requests (in seconds)
    #    'CONCURRENT_REQUESTS': 1,  # Number of concurrent requests (set to 1)
    #    'AUTOTHROTTLE_ENABLED': True,  # Enable autothrottle
    #} 
    last_page_reached = 0

    def parse(self, response):
        
        #შემოწმება რომ პირველი ელემენტი არ უდრის წინა გვერდის ელემენტს სავარაუდოდ ჰრეფებით
        
        jobs = response.css('tr')
        if len(jobs)!= 300:
            self.last_page_reached += 1
            
        if self.last_page_reached == 2:
            raise CloseSpider('მეტი აღარაა')
        
        
        
        for job in jobs:
            relative_url = job.css('a ::attr(href)').get()
            job_url = response.urljoin(relative_url)
            
            yield response.follow(job_url, callback = self.parse_job_page)
            
            
        self.page_number += 1
        next_page_url = f"https://jobs.ge/?page={self.page_number}&q=&cid=0&lid=0&jid=0&in_title=0&has_salary=0&is_ge=0&for_scroll=yes"
        yield response.follow(next_page_url, callback = self.parse)
        
    def parse_job_page(self, response):


        
        job_title = response.css('body #wrapper div.content #job table tr td:nth-of-type(1) table:nth-of-type(2) tr:nth-of-type(1) td b ::text').get()
        company_link = response.urljoin(response.css('body #wrapper div.content #job table tr td:nth-of-type(1) table:nth-of-type(2) tr:nth-of-type(2) td b a::attr(href)').get())
        company_name = response.css('body #wrapper div.content #job table tr td:nth-of-type(1) table:nth-of-type(2) tr:nth-of-type(2) td b a ::text').get()
        start_date = response.css('body #wrapper div.content #job table tr td:nth-of-type(1) table:nth-of-type(2) tr:nth-of-type(3) td b:nth-of-type(1) ::text').get()
        end_date = response.css('body #wrapper div.content #job table tr td:nth-of-type(1) table:nth-of-type(2) tr:nth-of-type(3) td b:nth-of-type(2) ::text').get()
        
        item = JobscraperItem()
        item['job_title'] = job_title
        item['company_link'] = company_link
        item['company_name'] = company_name
        item['start_date'] = start_date
        item['end_date'] = end_date
        yield item
        