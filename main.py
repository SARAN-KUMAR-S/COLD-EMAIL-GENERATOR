import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from auth import initialize_db, authentication_page

# Cold Email Generator Interface
def interface(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", placeholder="https://example.com")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"Error occurred: {e}")

# Main Function
def main():
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

    conn, cursor = initialize_db()

    if not st.session_state.authenticated:
        authentication_page(cursor, conn)
    else:
        # Once authenticated, show the cold email generator interface
        chain = Chain()
        portfolio = Portfolio()
        st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon='📧')
        interface(chain, portfolio, clean_text)

if __name__ == "__main__":
    main()
