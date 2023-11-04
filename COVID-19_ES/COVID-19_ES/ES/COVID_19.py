from pyknow import *

class Covid19(Fact):
    """Fact: Signs and risk factors related to COVID-19."""
    pass

class Covid19RiskAssessment(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.assessment = []
    
    @Rule(Covid19(symptoms=MATCH.symptoms),
          TEST(lambda symptoms: 'fever' in symptoms and 'cough' in symptoms and 'shortness of breath' in symptoms))
    def symptom_high_risk(self):
        self.assessment.append("High risk of COVID-19. Seek medical attention.")

    @Rule(Covid19(symptoms=MATCH.symptoms),
          TEST(lambda symptoms: 'loss of taste' in symptoms or 'loss of smell' in symptoms))
    def symptom_moderate_risk(self):
        self.assessment.append("Moderate risk of COVID-19. Monitor and consult a healthcare professional if symptoms worsen.")

    @Rule(Covid19(age=MATCH.age),
          TEST(lambda age: age >= 60))
    def age_high_risk(self):
        self.assessment.append("Higher risk due to age. Take precautions and consult a healthcare professional.")

    @Rule(Covid19(underlying_conditions=MATCH.conditions),
          TEST(lambda conditions: 'diabetes' in conditions or 'chronic lung disease' in conditions))
    def condition_high_risk(self):
        self.assessment.append("High risk due to underlying health conditions. Seek medical advice.")

    @Rule(Covid19(vaccination_status='unvaccinated'))
    def unvaccinated_high_risk(self):
        self.assessment.append("Unvaccinated individuals are at a higher risk. Consider getting vaccinated and seek medical advice if showing symptoms.")

    @Rule(Covid19(symptoms=MATCH.symptoms),
          TEST(lambda symptoms: 'fatigue' in symptoms and 'muscle aches' in symptoms))
    def symptom_general(self):
        self.assessment.append("General symptoms of COVID-19 detected. Stay vigilant and consider testing.")

    @Rule(Covid19(symptoms=MATCH.symptoms),
          TEST(lambda symptoms: 'sore throat' in symptoms and 'runny nose' in symptoms))
    def symptom_cold_like(self):
        self.assessment.append("Cold-like symptoms detected. Monitor for any additional symptoms of COVID-19.")

    @Rule(Covid19(symptoms=MATCH.symptoms),
          TEST(lambda symptoms: 'nausea' in symptoms or 'vomiting' in symptoms or 'diarrhea' in symptoms))
    def symptom_gastrointestinal(self):
        self.assessment.append("Gastrointestinal symptoms detected. These can be associated with COVID-19.")

    @Rule(Covid19(symptoms=MATCH.symptoms),
          TEST(lambda symptoms: len(symptoms) > 3))
    def multiple_symptoms(self):
        self.assessment.append("Multiple symptoms detected. Higher risk of COVID-19. Consider self-isolation and testing.")

    @Rule(Covid19(underlying_conditions=MATCH.conditions),
          TEST(lambda conditions: 'heart disease' in conditions or 'chronic kidney disease' in conditions))
    def condition_very_high_risk(self):
        self.assessment.append("Very high risk due to serious underlying conditions. Strictly follow COVID-19 precautions and consult healthcare provider.")

    @Rule(Covid19(occupation='healthcare_worker'),
          Covid19(exposure_to_known_case=True))
    def healthcare_worker_exposed(self):
        self.assessment.append("You are a healthcare worker and have been exposed to a known case. High risk of infection, follow protocols and get tested.")

    @Rule(Covid19(occupation='essential_worker'),
          Covid19(symptoms=MATCH.symptoms),
          TEST(lambda symptoms: len(symptoms) > 0))
    def essential_worker_with_symptoms(self):
        self.assessment.append("As an essential worker with symptoms, there's a risk of having and spreading COVID-19. Consider immediate testing and self-isolation.")

    @Rule(Covid19(living_condition='high_density'),
          Covid19(symptoms=MATCH.symptoms),
          TEST(lambda symptoms: 'fever' in symptoms or 'cough' in symptoms))
    def high_density_living_with_symptoms(self):
        self.assessment.append("Living in high-density areas with symptoms increases the risk of spread. Exercise caution, isolate, and consider getting tested.")

    @Rule(AND(Covid19(travel_history=True),
              Covid19(symptoms=MATCH.symptoms),
              TEST(lambda symptoms: 'fever' in symptoms or 'cough' in symptoms or 'shortness of breath' in symptoms)))
    def travel_history_with_major_symptoms(self):
        self.assessment.append("Recent travel history with major COVID-19 symptoms detected. High likelihood of infection. Self-isolate and seek testing.")

    @Rule(AND(Covid19(age=MATCH.age),
          TEST(lambda age: age >= 65),
          Covid19(travel_history=True),
          Covid19(symptoms=MATCH.symptoms),
          TEST(lambda symptoms: 'difficulty breathing' in symptoms or 'chest pain' in symptoms)))
    def older_adult_severe_symptoms_with_travel(self):
        self.assessment.append("Older adult with travel history and severe symptoms. High risk for serious COVID-19 complications. Seek emergency medical care immediately.")

    @Rule(Covid19(symptoms_duration=MATCH.days),
      TEST(lambda days: days > 10),
      Covid19(symptoms=MATCH.symptoms),
      TEST(lambda symptoms: 'fever' in symptoms or 'cough' in symptoms))
    def prolonged_symptoms(self):
        self.assessment.append("Symptoms lasting more than 10 days. Risk of complications. Consult a healthcare professional.")

    @Rule(AND(Covid19(occupation=MATCH.occupation),
              OR(Covid19(occupation='healthcare_worker'), Covid19(occupation='essential_worker')),
              Covid19(underlying_conditions=MATCH.conditions),
              TEST(lambda conditions: 'hypertension' in conditions or 'obesity' in conditions),
              Covid19(symptoms=MATCH.symptoms),
              TEST(lambda symptoms: 'headache' in symptoms or 'sore throat' in symptoms)))
    def mild_symptoms_high_risk_occupation_and_conditions(self):
        self.assessment.append("Mild symptoms, but at higher risk due to occupation and underlying health conditions. Monitor symptoms closely and consider testing.")
        
    @Rule(AND(Covid19(vaccination_status='vaccinated'),
              Covid19(exposure_to_known_case=True),
              Covid19(symptoms=MATCH.symptoms),
              TEST(lambda symptoms: 'fatigue' in symptoms or 'loss of appetite' in symptoms)))
    def vaccinated_exposed_mild_symptoms(self):
        self.assessment.append("Vaccinated individual with exposure and mild symptoms. Risk of breakthrough infection. Consider testing and stay isolated.")

    @Rule(AND(Covid19(age=MATCH.age),
              TEST(lambda age: 45 <= age <= 64),
              Covid19(symptoms=MATCH.symptoms),
              TEST(lambda symptoms: 'sudden onset of confusion' in symptoms or 'difficulty breathing' in symptoms)))
    def middle_aged_sudden_worsening(self):
        self.assessment.append("Middle-aged adult with sudden worsening of symptoms. Possible severe COVID-19 case. Seek medical attention immediately.")

    @Rule(AND(Covid19(symptoms=MATCH.symptoms),
              TEST(lambda symptoms: 'diarrhea' in symptoms and 'cough' in symptoms),
              Covid19(public_gathering_history=True)))
    def gastro_and_respiratory_symptoms_with_public_gathering(self):
        self.assessment.append("Gastrointestinal and respiratory symptoms after attending a public gathering. Higher risk of COVID-19. Consider testing and self-isolation.")

    def get_assessment(self):
        return '\n'.join(self.assessment) if self.assessment else "No specific risk identified."



def get_assessment(symptoms, age, underlying_conditions, vaccination_status, occupation, living_condition, travel_history):
    engine = Covid19RiskAssessment()
    engine.reset()
    engine.declare(Covid19(symptoms=symptoms, age=age, underlying_conditions=underlying_conditions, vaccination_status=vaccination_status, occupation=occupation, living_condition=living_condition, travel_history=travel_history))
    engine.run()
    return engine.get_assessment()


