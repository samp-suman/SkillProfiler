import streamlit as st
import openai


def main():

    # Override Tab key behavior in the text area
    st.markdown("""
    <style>
    .block-container .stTextArea { resize: none; }
    </style>
    """, unsafe_allow_html=True)

    st.title("SkillProfiler - Tech Stack Interview")

    skills = []
    proficiency_levels = []

    st.subheader("Enter Skills and Proficiency Levels")
    Primary_skill = st.text_input("Primary Skill", key=f'skill-primary     ')
    Primary_proficiency_level = st.selectbox(
        "Proficiency Level",
        ["Beginner", "Intermediate", "Advanced"],
        key=f'profiency-primary'
    )
    # Secondary_skill = st.text_input("Secondary Skill", key=f'skill-secondary')
    # Secondary_proficiency_level = st.selectbox(
    #     "Proficiency Level",
    #     ["Beginner", "Intermediate", "Advanced"],
    #     key=f'profiency-secondary'
    # )
    skills.append(Primary_skill)
    proficiency_levels.append(Primary_proficiency_level)
    # skills.append(Secondary_skill)
    # proficiency_levels.append(Secondary_proficiency_level)
    # def skills_add():
    #     index = len(skills)
    #     skill = st.text_input("Skill", key=f'skill-{index}')
    #     proficiency_level = st.selectbox(
    #         "Proficiency Level",
    #         ["Beginner", "Intermediate", "Advanced"],
    #         key=f'profiency-{index}'
    #     )
    #     skills.append(skill)
    #     proficiency_levels.append(proficiency_level)
    # if st.button('Add Skills+', key=f'skill-btn-{len(skills)}'):
    #     skills_add()

    # skills_add()

    # Display input fields for skills and proficiency levels
    print()
    if st.button("Start Interview"):

        # Generate questions based on skills
        questions = generate_questions(skills, proficiency_levels)

        total_score = 0

        # Iterate through each question
        for i, question in enumerate(questions):
            openai_answer = generate_openai_answer(question)
            with st.form(f"my_form-q-{i}"):
                st.subheader(f"Question {i+1}")
                st.write(question)
                user_answer = st.text_area(
                    "Your Answer", key=f'text-area-q-{i}')

                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                if submitted:
                    st.write("Score processing")
                    # with st.spinner("Processing..."):
                    #     # Make API call

                    #     score = evaluate_answer(user_answer, openai_answer)
                    #     st.success(score)
                    #     total_score += score
            # st.write("OpenAI Answer:", openai_answer)
        st.write("Your Score:", total_score)
        if st.button('Submit', key='final-submit'):
            st.subheader("Total Score")
            st.write(total_score)


def generate_questions(skills, proficiency):
    questions = []
    for skill, prof in zip(skills, proficiency):
        # Define the prompt and the model to use
        prompt = f"Generate a situation based question  on the following skill: {skill} with profiency level {prof}. Question :\n"

        # Call the OpenAI API to generate the question
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=32,
            n=1,
            stop=None,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        print(response)
    # Retrieve and return the generated question from the API response
        questions.append(response.choices[0].text.strip())
    return questions


@st.cache
def generate_openai_answer(question):
    # Placeholder function to generate answer using OpenAI
    # You need to replace this with the actual OpenAI API call
    # and retrieve the answer for the given question

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=32,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    print(response)
    # Retrieve and return the generated question from the API response

    answer = response.choices[0].text.strip()
    return answer


@st.cache
def evaluate_answer(user_answer, openai_answer):
    # Placeholder function to evaluate the user answer
    # against the OpenAI answer and assign a score
    # You can define your own evaluation logic here
    prompt = f'Evaluate my Answer with GPT answer and give a score out pf 10. just give me a score in number nothing else.\nMy answer : \n {user_answer}\nGPT Answer:\n{openai_answer}'

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    print(response)
    # Retrieve and return the generated question from the API response

    score = response.choices[0].text.strip()
    print(score, type(score))
    return score


if __name__ == "__main__":
    openai.api_key = "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"
    main()
