script({
    // user interface
    title: "Readme Generator",
    description: "Review and generate documentation for your project.",
    group: "documentation",
    // model configuration
    model: "large",
    temperature: 0,
})

const pys = await workspace.findFiles("**/*.py")
def("FILES", pys)

$`
You are a Developer with Years of Experience. Your task is to write all the documentation of the project you are developing. You will have to read all the code that makes up the project and write an introduction to the purpose of the project followed by a definition of the structure of the code to which you will attach the purpose of that specific component

Create README_AI.md file for the project. Here are few things to include:

- Project title and description
- Installation instructions
- Usage examples
- Testing instructions

Ensure that the README is well-structured, clear, and easy to understand at accurate. 

If the README is factually incorrect or is not clear, then the LLM/agent retry until it produces a correct and clear README.
`

