from crewai import Agent, Task
import json, re
class ManifestAgent:

    @staticmethod
    def create(llm):
        return Agent(
            role='Project Architect',
            goal='Determine project structure and file organization',
            backstory="""You are a software architect specialized in analyzing project
            requirements and determining optimal file structure. You excel at identifying
            appropriate file names and organization based on project specifications.""",
            tools=[],
            verbose=False,
            llm=llm
        )

    @staticmethod
    def create_task(agent, project_spec):
        """Create a task for determining project file structure."""
        return Task(
            description=f"Analyze the following project specification and determine appropriate file structure:{project_spec}"
                        "Your task is to process this specification and return a JSON string with file structure information that"
                        "1. Generate requisite application files."
                        "2. Include a dependencies file:"
                        "   - For Node.js projects, create a `package.json` file with necessary dependencies."
                        "   - For Python projects, create a `pyproject.toml` file with necessary dependencies."
                        "3. Ensure all files are correctly formatted and include basic metadata."
                        "        Return only the JSON string output from this Python code"
                        "        Do not include any additional text or formatting in your response.",
            agent=agent,
            expected_output="A valid JSON string containing file paths and language information with the following keys:"
                            "name,language,implementation_file,test_file,docs_file,interface_file,run_script, "
                            "and file-mapping.  file-mapping needs to contain instructions that describes what goes "
                            "into the file. An example file-mapping for html/javascript would look like this: "
                            "{\"name\": \"Asteroids Game\", \"language\": \"JavaScript\", \"implementation_file\": "
                            "\"src/index.html\", \"review_file\": \"src/review.txt\","
                            "\"test_file\": \"tests/game.test.js\", \"docs_file\": \"docs/README.md\", "
                            "\"interface_file\": \"src/idf.js\", \"run_script\": \"build_and_run.sh\","
                            "\"file-mapping\": {\"src/index.html\": \"contains html with css and javascript\", "
                            " \"docs/README.md\":\"contains markdown\","
                            " \"build_and_run.sh\":\"contains a bash script to install dependencies and run\","
                            " \"src/idf.js\":\"contains commented javascript\","
                            " \"tests/game.test.js\":\"contains javascript\","
                            " }} The file-mapping will differ between languages and will identify what a language a "
                            "file contains",
            output_file='src/manifest.json'
        )

    @staticmethod
    def determine_language(spec):
        """Analyze specification to determine primary programming language."""
        spec = spec.lower() if isinstance(spec, str) else ""
        language_patterns = {
            'python': r'\b(python|flask|django|fastapi)\b',
            'cpp': r'\b(c\+\+|cpp|gcc)\b',
            'javascript': r'\b(javascript|node|express|react)\b',
            'java': r'\b(java|spring|maven)\b',
            'go': r'\b(go|golang)\b',
        }

        for lang, pattern in language_patterns.items():
            if re.search(pattern, spec):
                return lang
        return 'python'  # Note: Default to Python if no specific language is detected

    @staticmethod
    def get_file_names(language, spec):
        """Generate appropriate file names based on language and specification."""
        base_name = ManifestAgent._extract_base_name(spec)

        extensions = {
            'python': {'impl': '.py', 'test': '_test.py', 'docs': '.md', 'interface': '.idl'},
            'cpp': {'impl': '.cpp', 'test': '_test.cpp', 'docs': '.md', 'interface': '.idl'},
            'javascript': {'impl': '.js', 'test': '.test.js', 'docs': '.md', 'interface': '.idl'},
            'java': {'impl': '.java', 'test': 'Test.java', 'docs': '.md', 'interface': '.idl'},
            'go': {'impl': '.go', 'test': '.test.go', 'docs': '.md', 'interface': '.idl'},
        }

        ext = extensions.get(language, extensions['python'])
        return {
            'language': language,
            'implementation_file': f"src/{base_name}{ext['impl']}",
            'test_file': f"tests/{base_name}{ext['test']}",
            'docs_file': f"docs/README{ext['docs']}",
            'interface_file': f"src/{base_name}{ext['interface']}",
            'review_file': f"src/review.txt",
        }

    @staticmethod
    def _extract_base_name(spec):
        """Extract a base name for files from the specification."""
        if not isinstance(spec, str):
            return 'app'

        words = spec.lower().split()
        key_indicators = ['calculator', 'server', 'api', 'service', 'app']

        for word in words:
            if word in key_indicators:
                return word

        return 'app'  # Default base name if no specific indicator is found

    @staticmethod
    def process_specification(spec):
        """Process the specification and return file structure as JSON string."""
        try:
            if not spec or not isinstance(spec, str):
                raise ValueError("Invalid specification provided")

            language = ManifestAgent.determine_language(spec)
            file_structure = ManifestAgent.get_file_names(language, spec)
            return json.dumps(file_structure, indent=2)
        except Exception as e:
            # Return a default structure on error
            default_structure = {
                'language': 'python',
                'implementation_file': 'src/app.py',
                'test_file': 'tests/test_app.py',
                'docs_file': 'docs/README.md',
                'interface_file': 'src/app.idl'
            }
            return json.dumps(default_structure, indent=2)
