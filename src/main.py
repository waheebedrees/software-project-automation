import os
import sys
import json

from crewai import  Crew, LLM
from httpx import HTTPStatusError
from openai import RateLimitError
from tenacity import retry, wait_random_exponential, stop_after_attempt


from agents import CodeAgent,  DocsAgent, ManifestAgent, IDLAgent, ReviewAgent, RunAgent, TestAgent
from tools.file_hanler import ProjectValidator, FileHandler
from utils.custom_logger import get_logger
from utils.utils import extract_json, extract_json_to_str


from dotenv import load_dotenv

load_dotenv()


logger = get_logger(__name__)



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



class ProjectWorkflow:
    def __init__(self, project_spec, llm):
        self.project_spec = project_spec
        self.validator = ProjectValidator()
        self.file_handler = FileHandler()

        # Initialize agents
        logger.info("Initializing agents...")
        self.manifest_agent = ManifestAgent.create(llm)
        self.idl_agent = IDLAgent.create(llm)
        self.code_agent = CodeAgent.create(llm)
        self.run_agent = RunAgent.create(llm)
        self.test_agent = TestAgent.create(llm)
        self.docs_agent = DocsAgent.create(llm)
        self.review_agent = ReviewAgent.create(llm)
        logger.info("Agents initialized successfully")
        
        
        

    @retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def execute_with_retry(self, crew):
        """Executes the crew tasks with retry logic."""
        try:
            # Ensure the input is a Crew object before calling kickoff
            if not isinstance(crew, Crew):
                raise TypeError("execute_with_retry expects a Crew object")
            return crew.kickoff()
        except (RateLimitError, HTTPStatusError) as e:
            logger.warning(
                f"Rate limit or HTTP error encountered: {e}. Retrying...")
            raise  # Re-raise to trigger retry
        except Exception as e:
            # Catch other potential errors during kickoff and log them
            logger.error(
                f"An error occurred during crew kickoff: {e}", exc_info=True)
            raise  # Re-raise to allow tenacity to handle retries if configured

    def execute(self):
        """
        Executes the complete project generation workflow.
        """
        try:
            logger.info("Starting project generation workflow")
            logger.info(f"Processing specification:\n{self.project_spec}")

            # Validate initial specification
            logger.info("Validating project specification")
            self.validator.validate_specification(self.project_spec)
            logger.info("Project specification validated")

            # Create and execute manifest task first
            logger.info("Creating manifest task")
            manifest_task = ManifestAgent.create_task(
                self.manifest_agent, self.project_spec)

            # Create a Crew for the manifest task
            manifest_crew = Crew(
                agents=[self.manifest_agent],
                tasks=[manifest_task],
                verbose=False
            )

            logger.info("Executing manifest crew")
            # Pass the Crew object to execute_with_retry
            manifest_result = self.execute_with_retry(manifest_crew)
            logger.debug(f"manifest_result {type(manifest_result)}")
            manifest_result = extract_json(manifest_result.raw)
            logger.debug(f"manifest_result {type(manifest_result)}")

            logger.info("Manifest crew executed")

            # Parse manifest output with proper error handling
            try:
                # Crew kickoff returns a list of results, one per task.
                # We expect the manifest task to be the only one here.
                manifest_output = manifest_result[0] if isinstance(
                    manifest_result, list) and manifest_result else manifest_result
                print(
                    f"---------------->manifest {manifest_output} <----------------")
                if not manifest_output:
                    raise ValueError("Manifest task returned no output")

                # Ensure the output is treated as a string before json.loads
                manifest_output = json.dumps(manifest_output)
                manifest_data = json.loads(manifest_output)
                logger.info(f"Manifest data: {manifest_data}")

            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Error parsing manifest output: {str(e)}")
                # Provide a robust default manifest data structure
                manifest_data = {
                    "implementation_file": "src/app.py",
                    "test_file": "tests/test_app.py",
                    "docs_file": "docs/README.md",
                    "interface_file": "src/app.idl",
                    "run_script": "build_and_run.sh",
                }
                logger.info(f"Using default manifest data: {manifest_data}")

            # Extract file paths from manifest
            implementation_file = manifest_data.get(
                'implementation_file', 'src/app.py')
            test_file = manifest_data.get(
                'test_file', 'tests/test_app.py')  # Corrected default path
            docs_file = manifest_data.get(
                'docs_file', 'docs/README.md')    # Corrected default path
            interface_file = manifest_data.get('interface_file', 'src/app.idl')
            run_script_file = manifest_data.get(
                'run_script', 'build_and_run.sh')

            relative_project_directory = "./src"
            
        
            # These paths are expected to be relative to the generated project root,
            # but they are being prefixed with ./src, which might lead to paths like ./src/src/app.py
            # Let's adjust this to keep the paths as intended by the manifest agent.
            # The file_handler.save_project_files will handle placing them correctly
            # within the timestamped directory under generated_projects.

            # Create required directories based on the raw manifest paths
            os.makedirs(os.path.dirname(os.path.join(
                './src', implementation_file)), exist_ok=True)
            os.makedirs(os.path.dirname(os.path.join(
                './src', test_file)), exist_ok=True)
            os.makedirs(os.path.dirname(os.path.join(
                './src', docs_file)), exist_ok=True)
            os.makedirs(os.path.dirname(os.path.join(
                './src', interface_file)), exist_ok=True)
            os.makedirs(os.path.dirname(os.path.join(
                './src', run_script_file)), exist_ok=True)

            logger.info(f"--------------------------------------------")
            logger.info(f"Implementation file: {implementation_file}")
            logger.info(f"Test file: {test_file}")
            logger.info(f"Docs file: {docs_file}")
            logger.info(f"Interface file: {interface_file}")
            logger.info(f"Run script file: {run_script_file}")

            # IDL Task
            idl_task = IDLAgent.create_task(
                self.idl_agent,
                self.project_spec,
                # Save to temporary ./src directory
                output_file=os.path.join('./src', interface_file)
            )
            
            
            logger.info("IDL task created")

            # Code Task
            code_task = CodeAgent.create_task(
                self.code_agent,
                self.project_spec,
                # Access the output of the task object, not a potential list result
                extract_json_to_str(idl_task.row) if hasattr( idl_task, "raw") else "",
                # Save to temporary ./src directory
                output_file=os.path.join('./src', implementation_file)
            )
            logger.info("Code task created")

            # Run Task
            run_task = RunAgent.create_task(
                self.run_agent,
                self.project_spec,
                # Access the output of the task object
                idl_task.raw if hasattr(idl_task, 'raw') else "",
                # Save to temporary ./src directory
                output_file=os.path.join('./src', run_script_file)
            )
            logger.info("run task created")

            # Test Task
            test_task = TestAgent.create_task(
                self.test_agent,
                # Access the output of the task object
                code_task.raw if hasattr(code_task, 'raw') else "",
                # Save to temporary ./src directory
                output_file=os.path.join('./src', test_file)
            )
            logger.info("Test task created")

            # Documentation Task
            docs_task = DocsAgent.create_task(
                self.docs_agent,
                f"""Project Documentation:
                Specification: {self.project_spec}
                Implementation: {code_task.raw if hasattr(code_task, 'raw') else ""}
                Testing: {test_task.raw if hasattr(test_task, 'raw') else ""}""",
                output_file=os.path.join(
                    './src', docs_file)  # Save to temporary ./src directory
            )
            logger.info("Documentation task created")

            # Create crew for remaining tasks
            crew = Crew(
                agents=[self.idl_agent, self.code_agent,
                        self.test_agent, self.docs_agent, self.run_agent],
                tasks=[idl_task, code_task, test_task, docs_task, run_task],
                verbose=False

            )

            # Introduce a review loop (i.e. iterative review until approved or a maximum iteration count)
            max_review_iterations = 1
            review_iteration = 0
            review_approved = False

            while review_iteration < max_review_iterations and not review_approved:
                # Execute the workflow and get results
                logger.info("Executing crew tasks")
                # Pass the Crew object to execute_with_retry
                results = self.execute_with_retry(crew)
                logger.debug(f"execute_with_retry {type(results)}")
                logger.debug(f"execute_with_retry {results}")
                # The results from crew.kickoff() are directly available as a string or list of strings
                # Let's process these results directly as they are output by the tasks.
                generated_files = {
                    interface_file: idl_task.raw if hasattr(idl_task, 'raw') else '',
                    implementation_file: code_task.output if hasattr(code_task, 'raw') else '',
                    test_file: test_task.raw if hasattr(test_task, 'raw') else '',
                    docs_file: docs_task.raw if hasattr(docs_task, 'raw') else '',
                    run_script_file: run_task.raw if hasattr(run_task, 'raw') else '',
                }

                logger.warning(f"output by the tasks. {type(idl_task)}")
                logger.debug(f"output by the tasks. {idl_task}")
                logger.debug(f"output by the tasks. {generated_files}")
                
                # Read the actual content from the output files written by the tasks
                # CrewAI agents write directly to files if output_file is specified.
                # So, we should read from these files to get the actual generated content for review.
                actual_generated_files = {}
                for file_key, relative_path in manifest_data.items():
                    if file_key in ['implementation_file', 'test_file', 'docs_file', 'interface_file', 'run_script']:
                        full_path = os.path.join('./src', relative_path)
                        if os.path.exists(full_path):
                            with open(full_path, 'r') as f:
                                actual_generated_files[relative_path] = f.read(
                                )
                        else:
                            logger.warning(
                                f"Output file not found: {full_path}")
                            # Provide an empty string if file not found
                            actual_generated_files[relative_path] = ""

                logger.info("Crew tasks completed")

                # Using the generated code—here we review the main implementation file.
                generated_code = actual_generated_files.get(
                    implementation_file, "")  # Get code from the actual file
                if not generated_code:
                    logger.warning("No generated code was found to review.")

                # Create and execute the review task
                review_task = ReviewAgent.create_task(
                    self.review_agent, generated_code)
                review_crew = Crew(
                    agents=[self.review_agent],
                    tasks=[review_task],
                    verbose=0
                )
                # Pass the Crew object to execute_with_retry
                review_result = self.execute_with_retry(review_crew)
                review_output = review_result[0] if isinstance(
                    review_result, list) else review_result.raw
                logger.info(f"Review output:\n{review_output}")

                if "Approved" in review_output:
                    review_approved = True
                    logger.info("Code review approved the generated code.")
                else:
                    logger.info(
                        "Code review requested revisions. Re-running generation tasks with feedback...")
                    # (Optionally, you could incorporate the review feedback in subsequent iterations.)
                    review_iteration += 1

                if not review_approved:
                    logger.warning(
                        "Maximum review iterations reached. Proceeding with the last generated files.")

                # Process and save generated files
                logger.info("Processing and saving generated files")
                generated_files = self._process_results(results)
                output_dir = self.file_handler.save_project_files(
                    generated_files)

                logger.info(
                    f"Project generation completed. Output directory: {output_dir}")
                return results

        except Exception as e:
          logger.error(f"Error in project generation: {str(e)}", exc_info=True)
          raise

    def _process_results(self, results):
        """
        Process the results from the crew execution into file contents.
        """
        try:
            generated_files = {}

            # Process IDL output
            if hasattr(results, 'idl_task') and results.idl_task:
                generated_files['src/specification.idl'] = results.idl_task
                logger.info("Processed IDL output")

            # Process code output
            if hasattr(results, 'code_task') and results.code_task:
                generated_files['src/app.py'] = results.code_task
                logger.info("Processed code output")

            # Process test output
            if hasattr(results, 'test_task') and results.test_task:
                generated_files['tests/test_app.py'] = results.test_task
                logger.info("Processed test output")

            # Process documentation output
            if hasattr(results, 'docs_task') and results.docs_task:
                generated_files['docs/README.md'] = results.docs_task
                logger.info("Processed documentation output")

            return generated_files

        except Exception as e:
            logger.error(f"Error processing results: {str(e)}", exc_info=True)
            raise

    def add_feature(self, feature_desc):
        """
        Handles the addition of new features to the existing project.
        """
        try:
            logger.info(f"Starting feature addition: {feature_desc}")

            # Create feature-specific tasks
            code_task = CodeAgent.create_task(
                self.code_agent,
                f"Add this feature to the existing implementation: {feature_desc}"
            )
        

            test_task = TestAgent.create_task(
                self.test_agent,
                f"""New Implementation: {code_task.output if hasattr(code_task, 'output') else ''}
                Feature Description: {feature_desc}
                Write tests for the new feature"""
            )

            run_task = RunAgent.create_task(
                self.run_agent,
                self.project_spec,
            )

            docs_task = DocsAgent.create_task(
                self.docs_agent,
                f"""Update documentation with:
                1. New Feature: {feature_desc}
                2. Implementation: {code_task.output if hasattr(code_task, 'output') else ''}
                3. Test Coverage: {test_task.output if hasattr(test_task, 'output') else ''}"""
            )

            # Create crew for feature addition
            crew = Crew(
                agents=[self.code_agent, self.test_agent,
                        self.docs_agent, self.run_agent],
                tasks=[code_task, test_task, docs_task, run_task],
                verbose=True
            )

            # Execute and process results
            results = crew.kickoff()
            generated_files = self._process_results(results)
            output_dir = self.file_handler.save_project_files(generated_files)

            logger.info(
                f"Feature addition completed. Output directory: {output_dir}")
            return results

        except Exception as e:
            logger.error(f"Error in feature addition: {str(e)}", exc_info=True)
            raise


llm = LLM(
    model='gemini/gemini-2.0-flash',
    api_key=os.environ["GOOGLE_API_KEY"]
)

file_path = 'config/project_spec.txt'
file_handler = FileHandler()
project_spec = file_handler.read_specification(file_path)

print(project_spec)


if __name__ == "__main__":
    
    # Initialize and run the project workflow
    workflow = ProjectWorkflow(project_spec, llm=llm)
    result = workflow.execute()
    print(result)
