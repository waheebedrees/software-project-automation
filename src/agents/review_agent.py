from crewai import Agent, Task
class ReviewAgent:
    @staticmethod
    def create(llm):
        return Agent(
            role="Senior Code Reviewer",
            goal="Review and provide feedback on generated code",
            backstory=(
                "You are an experienced software engineer with a talent for "
                "ensuring code quality, maintainability, and adherence to best practices. "
                "You know how to guide teams toward high quality implementations through detailed reviews."
            ),
            verbose=False,
            llm=llm
        )

    @staticmethod
    def create_task(agent, code, output_file=None):
        if output_file is None:
            output_file = "src/report.txt"
        return Task(
            description=(
                "Review the following generated code for maintainability, design, error handling and style:\n\n"
                f"{code}\n\n"
                "If the code is acceptable, output a plain text response that includes 'Approved'. "
                "If improvements are needed, output a response containing 'Revisions required' along with a list of suggestions. "
                "Do not include markdown formatting in your response."
                # This line added to default to Revisions required
                "If you are unable to determine, please output 'Revisions required'"

            ),
            agent=agent,
            expected_output=(
                "A detailed review of the code. It should include the word 'Approved' if acceptable, "
                "or 'Revisions required' if improvements are needed."
            ),
            output_file=output_file
        )
