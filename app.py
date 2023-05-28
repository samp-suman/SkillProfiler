from flask import Flask, render_template, request, redirect
import json
import openai

# Initialize the OpenAI API with your API key
openai.api_key = "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"

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_skills', methods=['GET', 'POST'])
def add_skills():

    return render_template('add_skill.html')


@app.route('/get_skills', methods=['GET', 'POST'])
def get_skills():
    skills_data = {}

    if request.method == 'POST':
        device_id = request.remote_addr

        skills = request.form.getlist('skill')

        proficiency_levels = request.form.getlist('proficiency')
        skills_data = dict(zip(skills, proficiency_levels))

        # Process the skills_data dictionary here
        with open('skills_data.json', 'r') as file:
            existing_data = json.load(file)
            if device_id in existing_data:
                # Update the existing data for the device ID
                existing_data[device_id].update(skills_data)
            else:
                # Create a new entry for the device ID
                existing_data[device_id] = skills_data

        with open('skills_data.json', 'w') as file:
            json.dump(existing_data, file)
        print(existing_data)
        return redirect('/interview')
    return render_template('add_skill.html')


@app.route('/interview', methods=['GET'])
def interview():
    device_id = request.remote_addr
    print('Device ID-', device_id)
    skills_data, generated_questions = generate_questions(device_id)
    print("generated_questions")
    return render_template('interview.html', device_id=device_id, skills_data=skills_data, questions_data=generated_questions)


def generate_questions(device_id):
    # Retrieve the skills data for the device ID from the JSON file
    with open('skills_data.json', 'r') as file:
        skills_data = json.load(file).get(device_id, {})
    # print("generat call-", skills_data)
    # Retrieve the questions for each skill from the questions.json file
    with open('questions.json', 'r') as file:
        questions_data = json.load(file)

    # Generate questions for each skill and proficiency level
    generated_questions = {}
    for skill, proficiency in skills_data.items():
        try:
            if questions_data[skill+'-'+proficiency]:
                generated_questions = {
                    skill+'-'+proficiency: questions_data[skill+'-'+proficiency]}
        except:
            # Retrieve the prompt for generating questions
            prompt = f"Give one unique question on {skill} with proficiency level {proficiency}. Give scenario-based questions. Don't provide Answers"
            generated_questions[skill+'-'+proficiency] = []
            for i in range(3):
                # Make API call to generate questions
                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=prompt,
                    max_tokens=60,
                    n=1  # Number of questions to generate
                )

                # Extract the generated questions from the API response
                generated_questions[skill+'-'+proficiency].append(
                    response.choices[0].text.strip())

    # Save the generated questions in the questions.json file
    questions_data.update(generated_questions)
    with open('questions.json', 'w') as file:
        json.dump(questions_data, file)
    return skills_data, questions_data


@app.route('/save_answers', methods=['POST'])
def save_answers():
    device_id = request.args.get('device_id')
    answers = {}

    for key, value in request.form.items():
        skill, question_no = key.split('_')
        if skill not in answers:
            answers[skill] = {}
        answers[skill][question_no] = [
            questions_data[skill][int(question_no) - 1], value]

    # Load existing responses from the JSON file
    with open('response.json', 'r') as file:
        response_data = json.load(file)

    # Update the responses with the new answers
    response_data[device_id] = answers

    # Save the updated responses to the JSON file
    with open('response.json', 'w') as file:
        json.dump(response_data, file)

    return redirect('/result')


@app.route('/result')
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
