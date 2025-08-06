from crewai import Agent, Task


class RunAgent:
    @staticmethod
    def create(llm):
        return Agent(
            role='Senior Software Developer',
            goal='Create a script that will compile and run',
            backstory="""You are an experienced software developer specializing in
            making sure the code can be run easily from a shell script, a makefile,
            or a batch script..""",
            verbose=False,
            llm=llm
        )

    @staticmethod
    def create_task(agent, project_spec, idl_spec, output_file=None):
        if output_file is None:
            output_file = 'build_and_run.sh'

        return Task(
            description=f"""Based on the following IDL specification and project specification, implement a complete application:
            Project Spec:
            {project_spec}

            IDL specification
            {idl_spec}

            Create a script that:
            0. installs the dependencies
            1. compiles the project if necessary, for example C++ and go need to be compiled
            2. creates a script that will run the unit tests""",
            agent=agent,
            expected_output="""A script that installs, compiles, and runs unit tests.  This script has no markdown and is plain text only.""",
            output_file=output_file
        )
