from bs4 import BeautifulSoup
import httpx

def scrape_asic_notices():
    response = httpx.get('https://publishednotices.asic.gov.au/browsesearch-notices/')
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    liquidations = []
    for notice in soup.find_all('tr'):
        status_tag = notice.find('dt', string='Status:')
        if status_tag:
            status = status_tag.find_next_sibling('dd').get_text(strip=True)
            if status == 'In Liquidation':
                # Find the published date
                published_date_div = notice.find('div', class_='published-date')
                if published_date_div:
                    published_date_span = published_date_div.find('span', string='Published: ')
                    if published_date_span:
                        published_date = published_date_span.next_sibling.strip()
                    else:
                        published_date = "Published date not found"
                else:
                    published_date = "Published date not found"

                # Find the company name
                company_name_tag = notice.find('p')
                if company_name_tag:
                    company_name = company_name_tag.get_text(strip=True)
                    # Clean the company name if it includes ACN and Status
                    company_name = company_name.split('ACN:')[0].strip()
                else:
                    company_name = "Company name not found"

                # Find the ACN
                acn_dt = notice.find('dt', string='ACN:')
                if acn_dt:
                    acn = acn_dt.find_next_sibling('dd').get_text(strip=True)
                else:
                    acn = "ACN not found"

                liquidations.append({
                    'company_name': company_name,
                    'acn': acn,
                    'date_published': published_date
                })

    return liquidations
