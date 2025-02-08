import ast
import asyncio
import streamlit as st
from gemini import give_relevant_link , summerise_text , generate_final_report
from browser import view_websites
from youtube import GetTranscripts


def main():
    st.title("Web Agent for Research")
    
    query = st.text_input("Enter your topic:")
    if st.button("Search"):
        
        if query.strip():
            links = give_relevant_link(query)
            links = links.replace("python" , '')
            links = links.replace("json" , '')
            links = links.replace("```" , '')
            links = ast.literal_eval(links.strip())
            
            final_content = " "
            
            st.subheader("Top Webpages:")
            website_links = links["webpages"]

            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            content_dict = asyncio.run(view_websites(query , website_links))

            for link, content in content_dict.items():
                final_content += summerise_text(content)
                st.markdown(f"- [{link}]({link})")
            
            st.subheader("YouTube Video:")
            st.markdown(links['youtube'])
            content = f"Youtube video on the topic {query}"
            content += GetTranscripts("https://www.youtube.com/watch?v=RuwFDrljlmY")
            final_content += summerise_text(content)
            st.markdown(f"[Watch here]({links['youtube']})")
            st.markdown(generate_final_report(final_content))

        else:
            st.warning("Please enter a topic to search.")



if __name__ == "__main__":
    main()
