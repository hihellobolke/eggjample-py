script({
    title: "SAST security issues fixer",
    files: ["main.py"],
})


async function runCodePrompt(role, message, code) {
    const answer = await runPrompt(
        (_) => {
            _.def("ROLE", role);
            _.def("REQUEST", message);
            _.def("CODE", code);   
            _.$`Your role is <ROLE>.
            The request is given by <REQUEST> 
            original code:
            <CODE>.`
        }
    )
    console.log(answer.text);
    return answer.text;
}

async function invokeLLMUpdate(code, inputFile) {
    
    let role = `You are a highly experienced secure python developer engineer with over 10 years of expertise in programming.
        You have a deep understanding of secure coding practices, software design patterns and follow best practices in software development.
        You have deep knowledge of best coding practices 
        and software engineering principles enables you to produce robust, efficient, and 
        maintainable code in any scenario.`;

    let userMessage = `Your goal is following:

        - check if code is relevant to the ERROR
        - and do not modify the original code unless it is necessary to fix the ERROR
        - only modify the code if it is necessary to fix the ERROR
        - ensure that the code passes all tests
        - ensure that the code compiles
        - explain the changes you made in the code as comment in the code in clear and concise manner. 
        - Make sure comments start are in english and start with #
        - Always make sure comments start are in english and start with #
        - And the code is generated within \`\`\`

        <ERROR>
            Secret detected
            SHA1:5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8

            Detected in test_main.py, Line 19
        </ERROR>
    
        
        <SUGGESTION>
            What's the issue?
            When a secret, or API token is leaked, it poses a significant security risk, as it can be exploited by malicious actors to gain unauthorized access to systems, data, or services. Developers managing the source code repository must act swiftly and follow a structured process to mitigate the risk.

            Revoke the Leaked Secret or Token
            Immediately revoke the compromised secret or token in the respective service
            Generate a new secret or token and update any systems or applications that rely on it
            Remove the Secret from the Repository
            Locate and delete the secret from the codebase to fix the finding
            If necessary and viable, rewrite the Git history to remove the key entirely (using tools like git filter-repo) and force push the cleaned history to the remote repository
            Rotate Exposed Credentials
            Assume that other credentials (e.g., secrets, API keys, or passwords) stored in the repository may also be compromised
            Rotate all sensitive credentials and update them in the relevant systems
            Audit for Unauthorized Activity
            Use logs and monitoring tools to check for unauthorized actions performed using the leaked secret
            If suspicious activity is detected, take immediate action to secure affected resources
            Strengthen Repository Security
            Use secrets management tools to handle secrets and credentials
            Implement pre-commit hooks and secret scanning tools
            Enforce Access Controls: Restrict repository access to authorized personnel only
            Notify Stakeholders
            Inform your team, security team, and management about the incident
            Follow your organizations incident response protocols to notify affected parties if necessary
            Review and Improve
            Conduct a post-incident review to identify how the token was leaked and address gaps in your processes
            Update policies and procedures to prevent similar incidents in the future
            Train developers on secure coding practices and the importance of not hardcoding secrets
            Monitor for Abuse
        </SUGGESTION>
    `;

    return runCodePrompt(role, userMessage, code);
}



for (const file of env.files) {


    if (!file.filename.endsWith(".py")) {
        throw new Error(`File ${file.filename} is not a Python file.`);
    }

    console.log(`Processing file: ${file.filename}`);
    const fileContent = await workspace.readText(file.filename);
    // const inputFile = await workspace.readFile(file.filename);
    const fileText = await workspace.readText(fileContent);
    const answer = await invokeLLMUpdate(fileText.content, fileContent);
    // Extract the code from the answer by removing ```python and ```:
    let code = answer.replace(/```python/g, "").replace(/```/g, "");
    const outputFile = fileContent.filename;
    await workspace.writeText(outputFile, code);
}
