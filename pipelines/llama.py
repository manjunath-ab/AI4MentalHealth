import torch
import transformers
from transformers import AutoTokenizer
from  langchain import LLMChain, HuggingFacePipeline, PromptTemplate

model = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    max_length=3000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id
)

llm = HuggingFacePipeline(pipeline = pipeline, model_kwargs = {'temperature':0})

template = """
              Write a summary of the following text delimited by triple backticks.
              Return your response which covers the key points of the text.
              ```{text}```
              SUMMARY:
           """
prompt = PromptTemplate(template=template, input_variables=["text"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

text = """
Patient Name: John Doe
Date of Birth: January 15, 1975
Gender: Male
Medical Record Number: 123456789
Date of Assessment: August 18, 2023

I. Chief Complaint:
The patient presents with complaints of persistent fatigue, unexplained weight loss, and intermittent abdominal pain over the past few months. He reports a gradual decrease in appetite and occasional nausea. The patient is seeking medical evaluation to determine the underlying cause of his symptoms.

II. Medical History:
The patient has a history of hypertension managed with medication for the past five years. He underwent an appendectomy in his late twenties and had a hernia repair surgery a decade ago. The patient reports a family history of diabetes on his maternal side.

III. Review of Systems:

General: The patient reports fatigue, unexplained weight loss of approximately 10 pounds over three months, and a decreased appetite.

Gastrointestinal: The patient experiences intermittent abdominal pain, predominantly in the right upper quadrant, without a clear trigger. He reports occasional nausea, and denies vomiting, diarrhea, or changes in bowel habits.

Cardiovascular: The patient's blood pressure has been well controlled with medication. He denies chest pain, palpitations, or shortness of breath.

Respiratory: The patient denies cough, wheezing, or shortness of breath.

Musculoskeletal: No significant joint pain or limitations in mobility reported.

Neurological: The patient denies headaches, dizziness, or changes in vision.

Psychological: The patient mentions occasional stress due to work-related factors but denies symptoms of depression or anxiety.

IV. Physical Examination:

Vital Signs: Blood pressure is 130/80 mmHg, heart rate is 78 beats per minute, respiratory rate is 16 breaths per minute, and temperature is 98.6°F (37°C).

General: The patient appears fatigued but alert and oriented to person, place, and time. He appears to have lost weight since his last visit.

Abdominal Examination: There is tenderness on palpation in the right upper quadrant of the abdomen. No palpable masses or organomegaly noted. Bowel sounds are normal.

Cardiovascular Examination: Regular rate and rhythm with no murmurs or abnormal sounds.

Respiratory Examination: Clear breath sounds bilaterally, no wheezing or crackles noted.

Neurological Examination: No focal neurological deficits observed.

V. Diagnostic Investigations:

Complete Blood Count (CBC): Within normal limits.
Comprehensive Metabolic Panel (CMP): Slight decrease in albumin levels.
Liver Function Tests (LFTs): Mild elevation in liver enzymes (AST and ALT).
Abdominal Ultrasound: No evidence of gallstones or other abnormalities. Liver appears slightly enlarged.
CT Scan of the Abdomen: Reveals a mass in the liver, approximately 5 cm in diameter. The mass appears to be enhancing on contrast.
VI. Assessment and Plan:

Based on the patient's symptoms, physical examination, and diagnostic investigations, the following assessment and plan have been formulated:

Assessment:

Unexplained weight loss and fatigue.
Right upper quadrant abdominal pain.
Elevated liver enzymes and an enlarging liver mass.
Plan:

Further Evaluation: Given the presence of an enlarging liver mass and elevated liver enzymes, the patient will be referred to a gastroenterologist for further evaluation, including possible liver biopsy.
Oncology Consultation: Given the possibility of malignancy, an oncology consultation will be sought to determine the nature of the liver mass and develop an appropriate treatment plan.
Symptom Management: The patient's abdominal pain will be managed with pain relievers as needed. Anti-nausea medication will be prescribed to alleviate nausea symptoms.
Nutritional Support: The patient's decreased appetite and weight loss will be addressed with dietary counseling and nutritional support to ensure adequate calorie intake.
Psychological Support: Given the patient's stress and anxiety related to his symptoms, psychological support and counseling will be offered to address emotional well-being.
VII. Follow-Up:

The patient is scheduled for a follow-up appointment in two weeks to discuss the results of further investigations, consultations, and to address any ongoing symptoms. The patient is advised to monitor his symptoms and report any significant changes or new symptoms before the next visit.

VIII. Prognosis and Discussion:

The presence of an enlarging liver mass raises concerns about potential malignancy. Further diagnostic testing and consultations with specialists are essential to determine the nature of the mass and develop an appropriate treatment plan. The patient's overall prognosis will be influenced by the nature of the liver mass and the success of treatment interventions. Close collaboration between the patient, medical team, and specialists will guide the management of his condition and optimize his chances of recovery.

IX. Patient Education:

The patient and his family will receive comprehensive education about the diagnostic process, potential treatment options, and the importance of adhering to medical recommendations. Emphasis will be placed on the need for regular follow-up appointments and open communication with the medical team to ensure the best possible outcomes.

X. Conclusion:

This patient report outlines the comprehensive health assessment of John Doe, a male patient presenting with unexplained weight loss, fatigue, and abdominal pain. The assessment encompasses a thorough medical history, review of systems, physical examination findings, diagnostic investigations, assessment, and a detailed plan for further evaluation and management. The collaboration between healthcare professionals and specialists will be crucial in guiding the patient's journey toward an accurate diagnosis, effective treatment, and optimal health outcomes.
"""

print(llm_chain.invoke(text))