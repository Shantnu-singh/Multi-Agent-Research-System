import ast
import asyncio
import streamlit as st
from gemini import give_relevant_link , summerise_text
from browser import view_websites
from youtube import GetTranscripts


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
            
            final_content = " "
            
            st.subheader("Top Webpages:")
            for link in links["webpages"]:
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                content = asyncio.run(view_websites(link))
                final_content += summerise_text(content)
                st.markdown(f"- [{link}]({link})")
                # st.write(content)
            
            
            st.subheader("YouTube Video:")
            st.markdown(links['youtube'])
            content = f"Youtube video on the topic {query}"
            content += GetTranscripts("https://www.youtube.com/watch?v=RuwFDrljlmY")
            final_content += summerise_text(content)
            st.markdown(f"[Watch here]({links['youtube']})")
            st.markdown(final_content)
        else:
            st.warning("Please enter a topic to search.")

if __name__ == "__main__":
    main()
