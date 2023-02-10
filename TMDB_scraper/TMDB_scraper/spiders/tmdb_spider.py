# to run 
# scrapy crawl tmdb_spider -o results.csv

import scrapy
import re

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/752-v-for-vendetta']
    
    def parse(self, response):
        cast_page = response.url + "/cast"
        yield scrapy.Request(cast_page, callback = self.parse_full_credits)
        
    def parse_full_credits(self, response):
        url_additions = response.css("ol.people.credits:not(.crew) div.info a::attr(href)").getall()
        for i in range(len(url_additions)):
            url = "https://www.themoviedb.org" + url_additions[i]
            yield scrapy.Request(url, callback = self.parse_actor_page)
            
    def parse_actor_page(self, response):
        actor_name = response.css(".title a::text").get()
        movie_or_TV_name = response.css(".tooltip bdi::text").getall()
        for i in range(len(movie_or_TV_name)):
            yield {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name[i]}