import ast
import streamlit as st
from gemini import give_relevant_link


def main():
    st.title("Web Agent for Relevant Links")
    
    query = st.text_input("Enter your topic:")
    if st.button("Search"):
        
        if query.strip():
            links = give_relevant_link(query)
            links = links.replace("python" , '')
            links = links.replace("json" , '')
            links = links.replace("```" , '')
            links = ast.literal_eval(links.strip())
            
            st.subheader("Top Webpages:")
            for link in links["webpages"]:
                st.markdown(f"- [{link}]({link})")
            
            st.subheader("YouTube Video:")
            st.markdown(f"[Watch here]({links['youtube']})")
        else:
            st.warning("Please enter a topic to search.")

if __name__ == "__main__":
    main()
