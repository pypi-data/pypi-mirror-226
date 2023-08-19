import json
import survey
import time

survey_instance = survey.Survey()
print(survey_instance.debug())

existing_surveys = {"surveys": []}


def generate(mood, nbr):
    for i in range(0, nbr):
        match mood:
            case 'positive':
                survey = survey_instance.generate_positive_survey()
            case 'neutral':
                survey = survey_instance.generate_neutral_survey()
            case 'negative':
                survey = survey_instance.generate_negative_survey()
        survey_instance.append_survey_to_dict(survey, existing_surveys)

    with open('surveys.json', 'w') as file:
        json.dump(existing_surveys, file, indent=4)
    survey_instance.convert_for_create_ml()



start_time = time.time()
generate('positive', 2)
generate('neutral', 2)
generate('negative', 2)
end_time = time.time()
execution_time = end_time - start_time

print(len(existing_surveys['surveys']), "survey(s) generated.")
print(survey.Survey().survey_max_possibilities(), "possibilities.")
print(execution_time, "to execute.")
