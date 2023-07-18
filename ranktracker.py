import requests
import streamlit as st
import urllib.parse
from urllib.parse import urlparse

class SearchEngineRankTracker:
    API_KEY = '871a09e5c981848880b9563ce55a2eb0307cdde9d5f69dbb1db3cef0f8a5da6d'
    BASE_URL = 'https://serpapi.com/search.json?engine=google&'

    COUNTRY_DOMAINS = {
        'United States': 'us',
        'United Kingdom': 'uk',
        'Canada': 'ca',
        'Australia': 'au'
    }

    def __init__(self):
        st.title('Search Engine Rank Tracker')
        self.query = st.text_input('Enter a search query')
        self.country = st.selectbox('Select a country', list(self.COUNTRY_DOMAINS.keys()))
        self.url = st.text_input('Enter the website URL with HTTPS', value='https://www.example.com')

    def fetch_search_results(self):
        google_domain = 'google.com'
        params = {
            'q': self.query,
            'location': self.country,
            'hl': 'en',
            'google_domain': google_domain,
            'api_key': self.API_KEY,
        }
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def print_params(self):
        params = {
            'q': self.query,
            'location': self.country,
            'hl': 'en',
            'google_domain': 'google.com',
            'api_key': self.API_KEY,
        }
        query_string = urllib.parse.urlencode(params)
        st.write(self.BASE_URL + query_string)

    def validate_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.scheme == 'https' and parsed_url.netloc != ''

    def run(self):
        if self.query and self.country and self.url and self.validate_url(self.url):
            if st.button('Submit'):
                results = self.fetch_search_results()
                if results:
                    organic_results = results.get('organic_results', [])
                    position = None
                    target_domain = urlparse(self.url).netloc
                    for index, result in enumerate(organic_results):
                        if 'link' in result:
                            result_domain = urlparse(result['link']).netloc
                            if result_domain == target_domain:
                                position = index + 1
                                ranking_url = result['link']
                                break
                    if position:
                        st.write(f"The website '{target_domain}' is found at position {position} for the search query '{urllib.parse.unquote_plus(self.query)}'")
                        st.write(f"The ranking URL is: {ranking_url}")
                        st.write(f"The code is available at: https://github.com/ansarianas33/serptracker")
                        self.print_params()
                    else:
                        st.write(f"The website '{target_domain}' is not found in the search results for the query '{urllib.parse.unquote_plus(self.query)}'")
                        st.write(f"The code is available at: https://github.com/ansarianas33/serptracker")
                        self.print_params()
                else:
                    st.error('Error fetching search results')
        elif self.query and self.country and not self.url:
            st.warning('Please enter a website URL')
        elif self.query and not self.country and self.url:
            st.warning('Please select a country')
        elif not self.query and self.country and self.url:
            st.warning('Please enter a search query')
        elif not self.validate_url(self.url):
            st.warning('Please enter a valid URL with HTTPS')
        else:
            st.warning('Please fill in all the fields')

if __name__ == '__main__':
    tracker = SearchEngineRankTracker()
    tracker.run()
