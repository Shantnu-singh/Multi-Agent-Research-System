import ast
import asyncio
import streamlit as st
from gemini import give_relevant_link , summerise_text , generate_final_report
from browser import view_websites, get_organic_results
from youtube import GetTranscripts



def main():
    st.title("Web Agent for Research")
    
    query = st.text_input("Enter your topic:")
    search_option = st.radio("Select Search Method:", ("Google Organic Results", "LLM-generated Results"))

    if st.button("Search"):
        
        if query.strip():
            final_content = " "
            links = {"webpages": [], "youtube": ""}
            
            if search_option == "LLM-generated Results":
                links = give_relevant_link(query)
                links = links.replace("python" , '')
                links = links.replace("json" , '')
                links = links.replace("```" , '')
                links = ast.literal_eval(links.strip())
            
            else:
                links = get_organic_results(query)
            
            st.write(links)
            st.subheader("Top Webpages:")
            website_links = links["webpages"]
            
            st.write(links["webpages"])
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            content_dict = asyncio.run(view_websites(query , website_links))

            for link, content in content_dict.items():
                final_content += summerise_text(content)
                st.markdown(f"- [{link}]({link})")
            
            st.subheader("YouTube Video:")
            st.markdown(links['youtube'])
            content = f"Youtube video on the topic {query}"
            content += GetTranscripts(links['youtube'])
            final_content += summerise_text(content)
            st.markdown(f"[Watch here]({links['youtube']})")
            st.markdown(generate_final_report(final_content))

        else:
            st.warning("Please enter a topic to search.")



if __name__ == "__main__":
    main()
