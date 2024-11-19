
import pandas as pd

def zero_shot_prompt(rubric, contract):
    return f"""
    You are a contract reviewer tasked with evaluating a contract based on a provided [RUBRIC]. The contract should include and reflect each section of the rubric.
    
    Annotate the following contract. Provide the annotations in markdown format. Provide an overall score of how well the contract reflects the rubric (out of 100). 
    
    The annotation should highlight any missing section/information, any grammatical issue, any information that isn't clear and concise, and Any potential risks


    Here's an example of the desired format:
    # Results 

    ## Score [SCORE]

    ### Page number, section name and [score] (out of 5)
        * [annotations]
        * [annotations]
    ### Page number, section name and [score] (out of 5)
        * [annotations]
        * [annotations]
    ### Other annotations
        *[annotations]
        *[annotations]


    [CONTRACT]
    {contract}

    [RUBRIC]
    {rubric}
    """.strip()

def one_shot_prompt(rubric, contract):
    return f"""
    You are a contract reviewer tasked with evaluating a contract based on a provided [RUBRIC]. The contract should include and reflect each section of the rubric.
    
    Annotate the following contract. Provide the annotations in markdown format. Provide an overall score of how well the contract reflects the rubric (out of 100). 
    
    The annotation should highlight any missing section/information, any grammatical issue, any information that isn't clear and concise, and Any potential risks


    Here's an example of the desired format:
    # Results 

    ## Score [SCORE]

    ### Page number, section - score 
        * [annotations]
        * [annotations]
    ### Page number, section - score 
        * [annotations]
        * [annotations]
    ### Other annotations
        *[annotations]
        *[annotations]


    [CONTRACT]
    {contract}

    [RUBRIC]
    {rubric}
        

    Follow the example below: 

    # Results 

    ## Score 65/100

    ### Page 1, Cover Page - 2/5
            * The cover page is missing crucial elements like a Confidentiality Notice or a clear indication that this is a "Draft" or "Final" version. 
            * The engagement type, DAF, is not mentioned on the cover page. 
            * The document needs a version number and date for easy tracking.
            * **Risk**: The lack of version control and confidentiality statement can lead to confusion and potential legal issues.

    ### Page 2-3, Executive Summary - 4/5
            * The executive summary provides a decent overview of the project.
            * It mentions the key aspects like the client, vendor, and the purpose of the PoC.
            * However, it could benefit from a clearer articulation of the business value and potential ROI for COGEP Inc.
            * **Risk**: Without a strong business value proposition, COGEP might not be fully convinced about the PoC's benefits.

    ### Page 3-4, Requirements and Solution, Scope of Services - 3/5
            * The document outlines the scope of services for the PoC. 
            * It details the activities involved in each phase: Assessment and Planning, Environment Setup, and Migration Execution.
            * However, it lacks clarity on the specific solutions being proposed. 
            * It should explicitly state how SE Cloud Experts plans to leverage Google Cloud technologies and best practices to meet COGEP's requirements.
            * **Risk**: The absence of a well-defined solution can lead to misunderstandings and potential scope creep during the project.

    ### Page 3-4, Activities and Deliverables - 3/5
            * The document lists the deliverables, but it could be more detailed. 
            * For instance, instead of just stating "Migration Plan," it should outline the key components of the plan. 
            * Similarly, for "Documentation," it should specify the types of documents that will be delivered.
            * **Risk**: Without detailed deliverables, COGEP might not receive comprehensive documentation and guidance, making it challenging to transition to a full-scale migration.

    ### Page 5-6, Timeline with Start and End Dates - 4/5
            * The timeline provides a clear start and end date for the PoC.
            * The breakdown of activities by week is helpful. 
            * However, it could benefit from a visual representation like a Gantt chart to illustrate the project schedule better.
            * **Risk**: A lack of a visual timeline might make it difficult to track progress and dependencies between tasks effectively.

    ### Page 6-7, Responsibilities -3/5
            * The document outlines the roles of both SE Cloud Experts and COGEP Inc. 
            * However, it lacks specific responsibilities assigned to each role. 
            * It should clearly state who is accountable for each task and decision.
            * **Risk**: Unclear responsibilities can lead to confusion and potential delays in project execution.

    ### Page 2, Success Criteria 2/5
            * The success criteria are too generic. 
            * Instead of just mentioning the completion of deliverables and client acceptance, it should define measurable and specific outcomes. 
            * For example, it could state the target number of users to be migrated, the desired migration speed, or the acceptable data loss threshold.
            * **Risk**: Vague success criteria can lead to disputes and disagreements about whether the PoC has achieved its intended objectives.

    ### Page 7, Pricing - 2/5
            * The pricing section is confusing. 
            * It mentions "Google Partner Funds Investment" but doesn't explain it clearly. 
            * The calculation of the "Total Services Cost" seems inaccurate, and the asterisk (*) next to "DAF" needs further clarification.
            * **Risk**: An ambiguous pricing model can lead to financial disagreements and erode trust between the parties involved.

    ### Page 8, Signature Block - 4/5
            * The signature block is present.
            * However, it needs a more formal structure with designated spaces for signatures, printed names, titles, and dates for both parties. 
            * Additionally, including a clause acknowledging the binding nature of the signatures would strengthen the contract.
            * **Risk**: A poorly formatted signature block might raise legal concerns about the enforceability of the contract.

    ### Other Annotations
            * **Grammatical Errors:** There are noticeable grammatical errors throughout the document (e.g., "conﬁgured" instead of "configured," "wrien" instead of "written").
            * **Clarity and Conciseness:** The writing style could be improved to be more concise and to the point. Some sentences are unnecessarily wordy.
            * **Technical Jargon:** While technical terms are expected, the document should strive to explain them or use simpler language to ensure clarity for all stakeholders.
            * **Missing MSA Reference:** The document mentions an MSA (Master Services Agreement) but doesn't provide a copy or a clear reference to its terms and conditions.
            * **Overall Risk:** The contract lacks clarity and comprehensiveness in several areas, potentially leading to misinterpretations, disputes, and financial risks for both COGEP Inc. and SE Cloud Experts.
            """.strip()