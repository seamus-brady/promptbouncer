
# Overview of Scanners in Prompt Bouncer

| **Scanner**                    | **Description**                                                                                                                                             | **Threat Level**          |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| **PromptInjectionScanner**     | Scans for any prompt injection attempts in a prompt. Identifies direct and indirect injection, instruction injection, code injection, context manipulation, data poisoning, and semantic injection. | Critical                  |
| **PromptLeakageScanner**       | Checks for prompt leakage. Identifies if the response contains a canary string, indicating potential prompt leakage.                                          | Critical                  |
| **PromptHijackScanner**        | Checks for prompt hijacking. Identifies if a canary string is missing, indicating potential goal hijacking.                                                   | Critical                  |
| **CodeScanner**                | Scans for code fragments in a prompt. Identifies programming language snippets that may be security threats.                                                   | Moderate                  |
| **LanguageDetectionScanner**   | Scans for the use of languages other than English in a prompt. Detects multiple language usage to prevent hidden instructions.                                | Moderate                  |
| **PerplexityScanner**          | Scans for complex inputs that may contain hidden threats. Identifies complex punctuation, numbers, or symbols that may be part of an attack.                  | Moderate                  |
| **InappropriateContentScanner**| Scans for inappropriate content in a prompt. Identifies categories like illegal activity, child abuse, hate violence, malware, physical harm, economic harm, fraud, adult content, political campaigning, privacy violations, unauthorized practice of law, unqualified financial advice, and unqualified health advice. | Serious                   |
| **ToxicityScanner**            | Scans for toxic language in a prompt. Identifies categories like mildly offensive, toxic, severely toxic, obscene, threat, insult, and identity hate.         | Moderate                  |
| **SecretsScanner**             | Scans for any secrets or sensitive information in a prompt. Identifies passwords, API keys, and other sensitive information.                                  | Moderate                  |

### Descriptions for Each Scanner

1. **PromptInjectionScanner**:
   - **Description**: This scanner identifies various types of prompt injection attacks, including direct injection, indirect injection, instruction injection, code injection, context manipulation, data poisoning, and semantic injection.
   - **Threat Level**: Critical

2. **PromptLeakageScanner**:
   - **Description**: This scanner checks for prompt leakage by detecting the presence of a canary string in the response, indicating potential leakage of the initial instructions or prompt.
   - **Threat Level**: Critical

3. **PromptHijackScanner**:
   - **Description**: This scanner checks for prompt hijacking by identifying the absence of a canary string in the response, indicating potential goal hijacking.
   - **Threat Level**: Critical

4. **CodeScanner**:
   - **Description**: This scanner detects code fragments in a prompt, identifying programming language snippets that may pose a security threat.
   - **Threat Level**: Moderate

5. **LanguageDetectionScanner**:
   - **Description**: This scanner detects the use of languages other than English in a prompt, aiming to prevent hidden instructions in multiple languages.
   - **Threat Level**: Moderate

6. **PerplexityScanner**:
   - **Description**: This scanner identifies complex inputs that may contain hidden threats, focusing on complex punctuation, numbers, or symbols used in conjunction with complex language.
   - **Threat Level**: Moderate

7. **InappropriateContentScanner**:
   - **Description**: This scanner identifies inappropriate content in a prompt, classifying it into categories like illegal activity, child abuse, hate violence, malware, physical harm, economic harm, fraud, adult content, political campaigning, privacy violations, unauthorized practice of law, unqualified financial advice, and unqualified health advice.
   - **Threat Level**: Serious

8. **ToxicityScanner**:
   - **Description**: This scanner detects toxic language in a prompt, categorizing it as mildly offensive, toxic, severely toxic, obscene, threat, insult, or identity hate.
   - **Threat Level**: Moderate

9. **SecretsScanner**:
   - **Description**: This scanner identifies secrets or sensitive information in a prompt, such as passwords, API keys, and other sensitive data.
   - **Threat Level**: Moderate
