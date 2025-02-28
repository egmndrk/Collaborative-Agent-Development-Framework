import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.model = genai.GenerativeModel('gemini-1.5-flash',
                                         system_instruction=role)
        self.total_tokens_used = 0

    def generate_response(self, prompt):
        response = self.model.generate_content(prompt)

        token_count = response.usage_metadata.total_token_count
        self.total_tokens_used += token_count

        return response.text

requirements_analyst_role = """
    # GOAL:
    As a Requirements Analyst, your aim is to gather information about the 
    software requirements and generate a comprehensive Software Requirements 
    Specification (SRS).

    # GENERAL RULES:
    Communicate with the user and investigate their software requirements through 
    structured questions. Ask one question at a time and provide options when possible.

    Always ask about:
    - Main purpose/objective
    - Key features needed
    - Performance requirements
    - Any constraints or limitations

    # ACTING RULES:
    1. Ask necessary questions to understand the specific requirements and 
    expectations for the software.

    2. If you are not sure that you have enough information, keep asking 
    one question at a time.

    3. If you think that you have enough information, stop asking questions 
    and provide a summary in the following format:

    SRS_DOCUMENT:
    Purpose: [Main purpose]
    Features: [List of key features]

    **It's crucial that your summary must begin with SRS_DOCUMENT keyword in 
    capital letters.**
"""

coder_role = """
    # GOAL:
    As a Software Developer, your goal is to write Python code based on 
    the provided Software Requirements Specification (SRS) and then improve 
    it according to tester's feedback.

    # GENERAL RULES:
    - Code must be clean and well-documented
    - Include docstrings and comments
    - Follow PEP 8 style guidelines
    - Include error handling where appropriate
    - Code must be complete and runnable

    # ACTING RULES:
    1. You will be given an SRS document.
    2. Generate complete Python code that fulfills all requirements.
    3. When you receive test feedback, revise the code accordingly.
    4. Always provide the complete updated code, not just the changes.

    Your response must start with:
    CODE_START
    [Your complete code here]
    CODE_END
"""

tester_role = """
    # GOAL:
    As a Software Tester, your goal is to review the given code based on 
    the original SRS document.

    # GENERAL RULES:
    - Verify all requirements are implemented
    - Check for potential bugs and issues
    - Validate error handling
    - Ensure code follows Python best practices
    - Test edge cases where appropriate

    # ACTING RULES:
    Review the code against the SRS and select one of these actions:

    A. If issues are found, respond with:
    TEST_FAILED:
    [List of specific issues and suggestions]

    B. If code meets all requirements:
    TEST_PASSED:
    [What tests did the code pass and brief confirmation message]
"""

class RequirementsAnalyst(Agent):
    def __init__(self):
        super().__init__("Requirements Analyst", requirements_analyst_role)
    
    def gather_requirements(self, max_interactions=5):
        msg = """Hello! I'm your Requirements Analyst.
        Let's discuss your software requirements.
        What's the main purpose of the software you want to build?\n"""
        conversation = [f"RA: {msg}"]

        purpose = input(msg)
        conversation.append(f"User: {purpose}")

        for i in range(max_interactions):
            prompt = f"""
            Current conversation:
            {' '.join(conversation)}
            """

            response = self.generate_response(prompt)

            if response.startswith("SRS_DOCUMENT:"):
                return response

            if i < max_interactions - 1:
                
                print(f"\nRA: {response}")
                conversation.append(f"RA: {response}")
                user_input = input("\nYour response: ")
                conversation.append(f"User: {user_input}")

        # Generate SRS if max interactions reached
        summary_prompt = f"""We've reached maximum interactions. Please generate 
        an SRS document based on this conversation:
        {' '.join(conversation)}
        Provide the SRS document in the following format:

        SRS_DOCUMENT:
        Purpose: [Main purpose]
        Features: [List of key features]
        """

        response = self.generate_response(summary_prompt)
        print(f"\nRA: {response}")
        return response

class Coder(Agent):
    def __init__(self):
        super().__init__("Coder", coder_role)

    def generate_code(self, srs):
        prompt = f"Generate Python code based on this SRS:\n{srs}"
        return self.generate_response(prompt)

    def revise_code(self, original_code, test_feedback, srs):
        prompt = f"""Revise this code based on the test feedback and original SRS:

        Original SRS:
        {srs}

        Original code:
        {original_code}

        Test feedback:
        {test_feedback}

        Please provide the complete revised code."""
        return self.generate_response(prompt)

class Tester(Agent):
    def __init__(self):
        super().__init__("Tester", tester_role)

    def test_code(self, code, srs):
        prompt = f"""Test this code against the SRS requirements:

        SRS:
        {srs}

        Code to test:
        {code}
        """
        return self.generate_response(prompt)

def generate_software():
    print("\n=== Starting Software Development Process ===\n")

    # Initialize agents
    analyst = RequirementsAnalyst()
    coder = Coder()
    tester = Tester()

    # Step 1: Gather requirements
    srs = analyst.gather_requirements()
    print("\n=== Requirements Gathered ===")

    # Step 2: Generate initial code
    print("\n=== Generating Code ===")
    code = coder.generate_code(srs)
    print(code)

    # Step 3-4: Testing and revision cycle
    max_iterations = 3
    
    for i in range(max_iterations):
        print(f"\n=== Testing Iteration {i+1}/{max_iterations} ===")
        
        test_result = tester.test_code(code, srs)
        print(f"\nTest Results:\n{test_result}")

        if "TEST_PASSED:" in test_result:
            print("\n=== Development Successfully Completed ===")
            break
        elif i < max_iterations - 1:
            print(f"\n=== Revising Code (Iteration {i+1}) ===")
            code = coder.revise_code(code, test_result, srs)
            print(code)
    else:
        print("\n=== Maximum iterations reached. Final version may need manual review ===")

    print("\n=== Token Usage ===")
    print(f"RequirementsAnalyst token usage: {analyst.total_tokens_used}")
    print(f"Coder token usage: {coder.total_tokens_used}")
    print(f"Tester token usage: {tester.total_tokens_used}")

    return code

if __name__ == "__main__":
    final_code = generate_software()