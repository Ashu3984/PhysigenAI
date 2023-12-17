from typing import List
import langchain
from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel
from pydantic import v1 as pydantic_v1

class TexRestructureTemplate(StringPromptTemplate,pydantic_v1.BaseModel):
    """A custom prompt template for Restructuring mathematical content with LLM readable."""
    input_variables: List[str] = ["content"]

    template = '''I have a technical text containing mathematical content that needs to be reformatted for fine-tuning a language model. The text includes mathematical expressions, some embedded HTML tags, and potential typographical errors. Please perform the following tasks to ensure the text is clear, concise, and suitable for fine-tuning:

1. Remove all HTML tags and present the content in a clean, plain text format.
2. Standardize the mathematical notations to be clear and precise. Retain any complex mathematical expressions in a simplified but accurate plain text format. Please ensure that any LaTeX-style notations or complex mathematical symbols are clearly represented in a format that balances readability with technical accuracy.
3. Clarify any ambiguous symbols and equations. Ensure all mathematical expressions, especially those involving calculus or advanced mathematics, are correctly represented and easy to interpret in plain text.
4. Correct any typographical or formatting errors to maintain the integrity of the mathematical content.

Here is the text that needs reformatting:{content}

The reformatted text should be presented directly without additional commentary. It should maintain the technical accuracy of the content, especially the mathematical expressions, for a language model trained on technical and scientific texts.
'''

    template_format = "f-string"
    def format(self, **kwargs):
        """Format the prompt."""
        return self.template.format(**kwargs)


class MetadataTemplate(StringPromptTemplate,pydantic_v1.BaseModel):
    """A custom prompt template for getting metadata of the input mathematical content (answers)."""

    input_variables: List[str] = ["answers"]

    template = ''' I have a series of answers to physics questions involving mathematical calculations and concepts. For each answer, I need you to analyze the text, extract the final answer, and categorize the key elements of the question it addresses. Specifically, I require:

1. Identification and extraction of the final answer from the input text.
2. Determination of the physics topic and subtopic based on the content of the answer.
3. Assessment of the difficulty level of the question.
4. Specification of the question type (e.g., calculation, conceptual understanding).
5. Listing of the skills tested and key concepts involved in the question.
6. Identification of the key formulae involved in solving the question.
7. Classification of the answer type (e.g., numerical, descriptive).

Please format the output for each answer as follows:
- A separate line for the final answer.
- A JSON structured output for the metadata, including fields for topic, subtopic, difficulty, question type, skills tested, and key concepts.

Here are examples to guide you:

EXAMPLE 1:
Input answer text: Given the following: Resistivity of copper, ρ_cu = 1.7 × 10^-8 Ωm, Area of cross-section, A = 0.01 mm^2 = 0.01 × 10^-6 m^2, Required resistance, R = 1 kΩ = 10^3 Ω... l = 0.58 × 10^3 m = 0.6 km.
Response: {{"answer": " 0.6 km", "metadata": {{"topic": "Electricity", "subtopic": "Resistivity and Resistance", "difficulty": "Intermediate", "question_type": "Calculation", "skills_tested": ["Problem-solving", "Application of Ohm's Law"], "key_concepts": ["Resistivity", "Ohm's Law", "Calculation of Length"],"formulae_involved": ["Ohm's Law", "Resistivity Formula"],"answer_type": "Numerical"}}


EXAMPLE 2:
Input answer text: As per the question, the initial current is denoted as i = i_0 * exp(-t / tau)... i_rms = i_0 / exp(1) * sqrt [(exp(2) - 1) / 2].
Response: {{"answer": "i_rms = i_0 / e * sqrt((e^2 - 1) / 2)", "metadata": {{"topic": "Electrodynamics", "subtopic": "LR Circuits", "difficulty": "Medium", "question_type": "Calculation", "skills_tested": ["Analytical Skills", "Mathematical Application"], "key_concepts": ["RMS Current", "Exponential Decay", "Integration"],"formulae_involved": ["Root Mean Square (RMS) Calculation", "Exponential Decay Formula"],"answer_type": "Numerical"}}

Now, here is the input answer text for analysis: {answers}

'''

    template_format = "f-string"
    def format(self, **kwargs):
        """Format the prompt."""
        return self.template.format(**kwargs)