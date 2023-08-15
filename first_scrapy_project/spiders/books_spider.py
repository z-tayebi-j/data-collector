import csv
import scrapy
import os



class booksSpider(scrapy.Spider):
    name = 'books'

    def start_requests(self):
        for i in range(1, 7):
            yield scrapy.Request(
                url=f'https://www.ketabrah.ir/book-category/%DA%A9%D8%AA%D8%A7%D8%A8-%D8%A7%D8%AF%D8%A8%DB%8C%D8%A7%D8%AA-%D9%BE%D8%A7%D8%B1%D8%B3%DB%8C/page-{i}?bt=books&sort=populars',
                callback=self.parse)

    def parse(self, response, **kwargs):
        urls = response.css('a[class="title"]::attr(href)').getall()
        for url in urls:
            yield response.follow(url, callback=self.parse_each_book)


    def parse_each_book(self, response):
        field_names = ['موضوع کتاب', 'نام کتاب', 'نویسنده', 'ناشر چاپی', 'سال انتشار', 'فرمت کتاب', 'تعداد صفحات',
                       'زبان', 'شابک', 'قیمت']
        price = response.css('span[class="discounted-price"]::text').get()
        book = {'قیمت': price}
        table = response.xpath('//table/tbody/tr')
        for row in table:
            key = row.xpath('td[1]/text()').get()
            if key == 'شابک':
                value = row.xpath('td[2]/span/text()').get()
            elif key == 'نویسنده' or key == 'ناشر چاپی':
                value = row.xpath('td[2]/a/span/text()').get()
            elif key == 'موضوع کتاب':
                value = ''
                a_tags = row.xpath('td[2]/a')
                for tag in a_tags:
                    value += tag.xpath('text()').get() + ', '
                value = value[:-2]
            else:
                value = row.xpath('td[2]/text()').get()
            book[key] = value

        with open('/home/zahra/Jadi/s4/project/first_scrapy_project/first_scrapy_project/spiders/books.csv',
                  'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writerow(book)

        # def start_requests(self):
        #     url = 'https://quera.org/problemset?tag=78&tag=88'
        #     # yield scrapy.Request(url=url, callback=self.parse)
        #     for i in range(2, 16):
        #         url = f'https://quera.org/problemset?tag=78&tag=88&page={i}'
        #         yield scrapy.Request(url=url, callback=self.parse)
        #
        # def parse(self, response, **kwargs):
        #     urls = response.xpath('/html/body/div[5]/div[2]/main/section/div[2]/div/table/tbody/tr').getall()
        #     next_page_disabled = response.xpath('/html/body/div[5]/div[2]/main/section/div[3]/button[3]/@disabled').get()
        #
        #     with open(os.path.join(os.getcwd(), 'test.txt'), 'a') as file:
        #         self.i += 1
        #         file.write(f'{self.i}: {len(urls)} \n')
