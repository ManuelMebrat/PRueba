# WE use streamlit to create a website, real quick 

from parse import parse_with_ollama
import streamlit as st
from scrape import (scrape_website,
                     split_dom_content,
                     clean_body_content, 
                     extract_body_content, )



st.title('Ai_web_scraper')

url = st.text_input('Enter a Website url')


if st.button('Crape Site'):
    st.write('Scrapping website')

    result = scrape_website(url)
    body_content = extract_body_content(result)
    clean_contect = clean_body_content(body_content)

    st.session_state.dom_content = clean_contect

    with st.expander("View dom content"):
        st.text_area('DOm contect', clean_contect,height=300)


if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to do")

    if st.button('Parse content'):
        if parse_description:
            st.write('parsing the content')


            dom_chunk = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunk,parse_description)
            st.write(result)
            
