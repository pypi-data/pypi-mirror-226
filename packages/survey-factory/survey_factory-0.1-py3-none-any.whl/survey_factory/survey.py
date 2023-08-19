import sequence_data as sd
import random


class Survey:
    def __init__(self):
        self.issues = sd.issues
        self.devices = sd.devices
        self.positive_sequences = sd.positive_sequences
        self.neutral_sequences = sd.neutral_sequences
        self.negative_sequences = sd.negative_sequences
        self.positive_templates = sd.positive_templates
        self.neutral_templates = sd.neutral_templates
        self.negative_templates = sd.negative_templates

    def _generate_survey(self, templates, sequences, label):
        template = random.choice(templates)
        sequence = random.choice(sequences)
        device = random.choice(self.devices)
        issue = random.choice(self.issues)

        text = template.format(device=device, issue=issue, positive_sequence=sequence,
                               neutral_sequence=sequence, negative_sequence=sequence)

        survey = {
            "text": text,
            "label": label
        }

        return survey

    def generate_positive_survey(self):
        return self._generate_survey(self.positive_templates, self.positive_sequences, "positive")

    def generate_neutral_survey(self):
        return self._generate_survey(self.neutral_templates, self.neutral_sequences, "neutral")

    def generate_negative_survey(self):
        return self._generate_survey(self.negative_templates, self.negative_sequences, "negative")

    def append_survey_to_dict(self, survey, existing_surveys):
        existing_surveys["surveys"].append(survey)
        return existing_surveys

    @staticmethod
    def convert_for_create_ml():
        with open('surveys.json', 'r') as file:
            content = file.read()

        start_pos = content.find('[')

        new_content = content[start_pos:-1]

        with open('surveys.json', 'w') as file:
            file.write(new_content)

    @staticmethod
    def survey_max_possibilities():
        lissue = len(sd.issues)
        ldevice = len(sd.devices)
        lpositive_sequences = len(sd.positive_sequences)
        lneutral_sequences = len(sd.neutral_sequences)
        lnegative_sequences = len(sd.negative_sequences)
        lpositive_templates = len(sd.positive_templates)
        lneutral_templates = len(sd.neutral_templates)
        lnegative_templates = len(sd.negative_templates)
        lpossibilities = lissue * ldevice * (lpositive_templates * lpositive_sequences +
                                             lneutral_templates * lneutral_sequences +
                                             lnegative_templates * lnegative_sequences)
        return lpossibilities

    @staticmethod
    def debug():
        return 'zebi'
