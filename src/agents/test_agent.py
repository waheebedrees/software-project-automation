from crewai import Agent, Task


class TestAgent:
    @staticmethod
    def create(llm):
        return Agent(
            role='Testing Specialist',
            goal='Create comprehensive tests for the generated code',
            backstory="""You are a QA engineer specialized in creating thorough test
            suites. You ensure code reliability through comprehensive test coverage
            and edge case handling for any programming language.""",
            tools=[],
            verbose=False,
            llm=llm
        )

    @staticmethod
    def create_task(agent, code, output_file):
        return Task(
            description=f"""Create comprehensive unit tests in the target language for the generated code:
            {code}

            Test suite must cover:
            0. Be written in the same language as the code
            1. All public interfaces and methods
            2. Error handling scenarios
            3. Edge cases and boundary conditions
            4. Integration tests where applicable
            5. Input validation""",
            agent=agent,
            expected_output="""Complete test suite in the specified language including:
            - Unit tests for all public methods
            - Error handling verification
            - Edge case coverage
            - Integration tests
            - Documentation of test scenarios
            - The file is plain text, it isn't markdown
            - Plain Text, remove Markdown""",
            output_file=output_file
        )
