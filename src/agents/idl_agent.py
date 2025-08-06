from crewai import Agent, Task


class IDLAgent:
    @staticmethod
    def create(llm):
        return Agent(
            role='IDL Specification Expert',
            goal='Convert project specifications into detailed Interface Definition Language',
            backstory="""You are an expert in creating Interface Definition Language (IDL)
            specifications from project requirements. You excel at translating business
            requirements into technical interfaces and data structures.""",
            verbose=False,
            llm=llm
        )

    @staticmethod
    def create_task(agent, specification, output_file=None):
        if output_file is None:
            output_file = 'src/app.idl'

        return Task(
            description=f"""Analyze the following project specification and create a detailed IDL:
            {specification}

            If the language does not support IDL the following IDL will appear as comments:
            Your task is to create a comprehensive IDL specification following this template:

            // Data Structures
            struct [StructName] {{
                // Properties with types
            }}

            // Interface Definitions
            interface [InterfaceName] {{
                // Method signatures with parameters and return types
            }}

            // Type Definitions
            typedef [NewType] [BaseType];

            // Error Specifications
            exception [ErrorName] {{
                // Error properties
            }}

            The IDL should cover:
            1. All required data structures
            2. Complete interface definitions
            3. Necessary type definitions
            4. Error specifications""",
            agent=agent,
            expected_output="""If the language supports IDL A complete IDL specification document containing:
            - Clearly defined data structures for the project
            - Well-documented interface definitions
            - Appropriate type definitions
            - Comprehensive error specifications
            - The output is in plain text with no markdown formatting
            If the language does not support IDL, the IDL will appear commented""",
            output_file=output_file
        )
