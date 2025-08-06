from crewai import Agent, Task


class DocsAgent:
    @staticmethod
    def create(llm):
        return Agent(
            role='Technical Writer',
            goal='Create application documentation',
            backstory="""You are a technical writer specialized in creating user-friendly
            documentation for any software project using command-line tools. You excel at explaining any
            concepts and software usage clearly.""",
            tools=[],
            verbose=False,
            llm=llm
        )

    @staticmethod
    def create_task(agent, project_info, output_file=None):
        if output_file is None:
            output_file = 'docs/README.md'

        return Task(
            description=f"""Create comprehensive documentation for the application:
            {project_info}

            Documentation should include:
            1. Installation and setup
            2. Available operations
            3. Usage examples
            4. Error handling guide
            5. History feature usage""",
            agent=agent,
            expected_output="""Complete documentation including:
            - Clear installation instructions
            - Detailed operation guide
            - Example calculations
            - Troubleshooting section
            - History feature explanation""",
            output_file=output_file
        )


