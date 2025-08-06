from crewai import Agent, Task


class CodeAgent:
    @staticmethod
    def create(llm):
        return Agent(
            role='Senior Software Developer',
            goal='Implement high-quality, maintainable code based on specifications',
            backstory="""You are an experienced software developer specializing in
            writing clean, efficient code. You excel at translating technical
            specifications into working implementations while following best practices.""",
            verbose=False,
            llm=llm
        )

    @staticmethod
    def create_task(agent, project_spec, idl_spec, output_file=None):
        if output_file is None:
            output_file = 'src/app.py'

        return Task(
            description=f"""Based on the following IDL specification and project specification, implement a complete application:
            Project Spec:
            {project_spec}

            IDL specification
            {idl_spec}

            Ensure the implementation:
            0. Is written in the specified language
            1. Follows object-oriented principles
            2. Includes proper error handling
            3. Is well-documented with type hints
            4. Follows proper style guidelines
            5. Implements all specified interfaces and data structures""",
            agent=agent,
            expected_output="""Complete implementation including:
            - All classes and methods defined in IDL
            - Proper error handling mechanisms
            - Type hints and docstrings
            - Clean code structure following OOP principles
            - Implementation of all required functionality
            - The output is in plain text with no markdown formatting""",
            output_file=output_file
        )
