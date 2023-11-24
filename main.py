import json
import openai
import streamlit as st

st.set_page_config(
    page_title="cpGPT",
    page_icon="📈",
    layout="wide"
)

openai.api_key = st.secrets['API_KEY_OPENAI']

def create_prompt(transcript):
    # content = 'Pretend you are an expert in every subject and you have best skills to find key points of the text and summarize text. '
    prompt = f"""First summarise the story of the following into a short problem statement(just focus on mathematical part while summarizing, ignore the proper nouns and story around them).
                Next, suggest 3 different algorithms for this problem in decreasing order of time complexity.\
                Next, for each of the 3 algorithms calculate numeric value of the number of operations needed to compute the result at maximum values of all the variables in problem statement.\
                Next, for each of the 3 algorithms mention the space complexity as well.\
                Next, suggest 3-4 general problems which makes use of similar concept.\
                Next, suggest 3-4 similar problems on any competitive programming platforms.\
                Only provide a compliant JSON response following this format without deviation.
            """
    json_prompt = """ {"algorithms": ["3 different algorithms"], "simprobs": "similar problems"}"""

    final = prompt + json_prompt + "Here is the full story of the problem: "

    return final

def openai_create(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "system", "content": 'Imagine you are a mathematician and a competitive programmer who will explain topics of competitive programming for complete beginners.'}, 
                {"role": "user", "content": prompt}], 
        temperature=0.4, 
        max_tokens=2048,
        frequency_penalty=3, 
        stop=None
    )

    return response['choices'][0]['message']['content']

st.markdown("<h1 style='text-align: center;'>🤖 From Zero-to-Hero in Competitive Programming</h1>", unsafe_allow_html=True)
st.write("""---""")

with st.sidebar.expander("ℹ️ - About App", expanded=True):
    st.write(
            """
    -   **cpGPT** - Competitive programming problem solving assistant using AlphaCode, GPT-4.
    -    Generates hints and references when you browse a problem on a competitive programming website.
    	    """
    )
 
st.sidebar.write("""---""")   

st.markdown("<h3 style='text-align: left;'> 🚀 Start Now</h3>", unsafe_allow_html=True)
c1, c2 = st.columns([6, 2])                       

with c1:
    query = st.text_area("Enter the topic, problem or code you would like to be explained:", height=170)

with c2:
    st.markdown('#')
    topic = st.button('Explain Topic', use_container_width=True)
    code = st.button('Explain Code', use_container_width=True)
    prob = st.button('Solve and Explain Problem', use_container_width=True)

st.write("""---""")  

if topic:
    with st.expander("ℹ️ - Topic Explanation", expanded=True):
        tpc_prmpt = f"""Briefly explain what this code {query} do that related only to competitive programming and nothing else. 
        Answer properly that any beginner in competitive programming would understand explanation. 
        Only provide a compliant and correct JSON response following this format without deviation."""
        
        json_prompt = """{"summary": "brief explanation"}, "steps": ["steps of topic"]"""

        tpc_ans = json.loads(openai_create(tpc_prmpt + json_prompt).replace('”', '"'))

        summ = tpc_ans['summary']
        steps = tpc_ans['steps']

        # st.write(f'{tpc_ans}'
        st.markdown("<h3 style='text-align: left;'> Brief Summary</h3>", unsafe_allow_html=True)
        st.info(summ)

        st.markdown("<h3 style='text-align: left;'> Steps</h3>", unsafe_allow_html=True)
        for step in steps:
            st.success(step)

if code:
    with st.expander("ℹ️ - Code Explanation & Assist", expanded=True):
        tpc_prmpt = f"""Briefly explain what this code {query} do, and what explain what is wrong with it and it should that related only to competitive programming and nothing else. 
                    Answer properly that any beginner in competitive would understand explanation. 
                    Only provide a compliant and correct JSON response following this format without deviation."""
            
        json_prompt = """{"explanation": "brief explanation", "wrong": "what is wrong"}"""

        tpc_ans = json.loads(openai_create(tpc_prmpt + json_prompt).replace('”', '"'))

        exp = tpc_ans['explanation']
        wr = tpc_ans['wrong']

            # st.write(f'{tpc_ans}'
        st.markdown("<h3 style='text-align: left;'> Brief Explanation</h3>", unsafe_allow_html=True)
        st.info(exp)

        st.markdown("<h3 style='text-align: left;'> What is wrong?</h3>", unsafe_allow_html=True)
        st.success(wr)

if prob:
    pass
    # with st.expander("ℹ️ - Problem Explanation & Solving", expanded=True):
    #     tpc_prmpt = f"""First summarise the story of the following into a short problem statement(just focus on mathematical part while summarizing, ignore the proper nouns and story around them).
    #                 Next, suggest 3 different algorithms for this problem in decreasing order of time complexity on this problem "{query}" that related only to competitive programming and nothing else. 
    #                 Answer properly that any beginner in competitive would understand explanation. 
    #                 Only provide a compliant and correct JSON response following this format without deviation."""
            
    #     json_prompt = """{"summary": "brief explanation", "algorithms": "algorithms"}"""

    #     tpc_ans = json.loads(openai_create(tpc_prmpt + json_prompt).replace('”', '"'))

    #     summ = tpc_ans['summary']
    #     algos = tpc_ans['algorithms']

    #         # st.write(f'{tpc_ans}'
    #     st.markdown("<h3 style='text-align: left;'> Brief Summary</h3>", unsafe_allow_html=True)
    #     st.info(summ)

    #     st.markdown("<h3 style='text-align: left;'> Hints for the Solution</h3>", unsafe_allow_html=True)
    #     for algo in algos:
    #         st.success(algo)            
