import streamlit as st
import parsing
from custom_prompt import TexRestructureTemplate,MetadataTemplate
import ast
# from gpt import get_chat_completion
import openai
openAiKey = st.text_input(label="Input the openai key", type="password")
openai.api_key = openAiKey
def get_chat_completion(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return str(e)
def main():
    st.sidebar.markdown("""
    <style>
    [data-testid=stImage]{
        display: block;
        margin-top: -20px;
        margin-left: auto;
        margin-right: auto;  
    }            
    </style>
    """, unsafe_allow_html=True)
    st.sidebar.image(image="physigen.png", width=100)
    st.sidebar.title('Demo Links')
    st.sidebar.markdown("[Link-1](https://www.shaalaa.com/question-bank-solutions/a-particle-mass-100-g-kept-surface-uniform-sphere-mass-10-kg-radius-10-cm-newton-s-universal-law-of-gravitation_66992#ref=chapter&id=53499)")
    st.sidebar.markdown("[Link-2](https://www.shaalaa.com/question-bank-solutions/a-block-mass-2-kg-pushed-against-rough-vertical-wall-force-40-n-coefficient-static-friction-being-05-static-and-kinetic-friction_66797#ref=chapter&id=53300)")
    st.sidebar.markdown("[Link-3](https://www.shaalaa.com/question-bank-solutions/the-average-separation-between-proton-electron-hydrogen-atom-ground-state-53-10-11-m-a-calculate-coulomb-force-between-them-this-separation-work-done-by-a-constant-force-and-a-variable-force_66339#ref=chapter&id=52831)")
    st.sidebar.markdown("""
        <style>
            .sidebar-text {
                text-align: justify;
                font-size: 14px;
                padding-bottom: 16px;
            }
            .list {
                font-size: 14px !important;
            }
           
        </style>
                        
        <div class="sidebar-text">
            This versatile tool accommodates inputs from URLs.         
        </div>

        <div class="sidebar-text">
            Contributors:
        </div>
        <ul>
            <li class="list">MR PRADIPTA PATTANAYAK</li>
            <li class="list">MR LIKHIT NAYAK</li>
            <li class="list">MR ASHUTOS SAHOO</li>
            <li class="list">SK SHAHID</li>
        </ul>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(
    """
        <style>
            .copyright {
                text-align: center;
                font-size: 14px;
            }
        </style>
        <div class="copyright">
            © 2023 Physigen
        </div>
    """,unsafe_allow_html=True
    )
    
    st.title("JEE Main Physics Question Parser")

    # Get the link input from the user
    link = st.text_input("Enter the link to the JEE Main physics question:")
    if st.button("Submit"):
        if link:
            try:
                ques,ans = parsing.parse(link)
                print("Checkpoint-1")
                restructure_prompt = TexRestructureTemplate()
                q_restruct_prompt = restructure_prompt.format(content=ques)
                question = get_chat_completion(q_restruct_prompt)
                print(question)
                print("Checkpoint-2")
                meta_data_prompt = MetadataTemplate()
                metadata_prompt = meta_data_prompt.format(answers=ans)
                meta_data = get_chat_completion(metadata_prompt)
                print(meta_data)
                print("Checkpoint-3")
                restructure_prompt = TexRestructureTemplate()
                explanation_restruct_prompt = restructure_prompt.format(content=ans)
                explanation = get_chat_completion(explanation_restruct_prompt)
                # print(explanation)
                # print("Checkpoint-4")
                meta_data=ast.literal_eval(meta_data)
                instruction=f'''Generate a {meta_data['metadata']["difficulty"]} difficulty physics question on the topic of {meta_data['metadata']["topic"]},subtopic {meta_data['metadata']["subtopic"]}, that tests {meta_data['metadata']["question_type"]} skills, and test the skills of {' and '.join(meta_data['metadata']["skills_tested"])}'''
                answer=meta_data['answer']
                metadata=meta_data['metadata']
                # print(instruction)
                # print("--"*20)
                # print(question)
                # print("--"*20)
                # print(answer)
                # print("--"*20)
                # print(explanation)
                # print("--"*20)
                # print(metadata)
                output_data = {
                                "instruction": instruction,
                                "question": question,
                                "answer": answer,
                                "explanation": explanation,
                                "metadata": metadata
                            }

                # Display the combined data as JSON
                st.subheader("Link Result")
                st.json(output_data)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid link.")




if __name__ == "__main__":
    main()

